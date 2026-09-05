#!/usr/bin/env python3
"""Render the profile 'mission control' stats panel as a self-hosted SVG.

Fetches live numbers from the GitHub REST/GraphQL API with the workflow's
GITHUB_TOKEN (no third-party stat services), then writes
assets/mission-control.svg.
"""
import json
import os
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
USER = os.environ["USER"]
OUT = "assets/mission-control.svg"

HDR = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "profile-stats",
    "Accept": "application/vnd.github+json",
}


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}", headers=HDR)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={**HDR, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]


user = api(f"/users/{USER}")
followers = user["followers"]

repos = []
page = 1
while True:
    batch = api(f"/users/{USER}/repos?per_page=100&page={page}")
    if not batch:
        break
    repos.extend(batch)
    page += 1

stars = sum(r["stargazers_count"] for r in repos)
public_repos = user["public_repos"]

# all-time commit count across public repos (paginated)
total_commits = 0
for r in repos:
    page = 1
    while True:
        req = urllib.request.Request(
            f"https://api.github.com/repos/{USER}/{r['name']}/commits?per_page=100&page={page}",
            headers=HDR,
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        if not batch:
            break
        total_commits += len(batch)
        if len(batch) < 100:
            break
        page += 1

data = gql(
    "query($u:String!){ user(login:$u){ contributionsCollection "
    "{ contributionCalendar { totalContributions } } } }",
    {"u": USER},
)
contribs = data["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

lang_bytes = {}
for r in repos:
    for k, v in api(f"/repos/{USER}/{r['name']}/languages").items():
        lang_bytes[k] = lang_bytes.get(k, 0) + v

top = sorted(lang_bytes.items(), key=lambda kv: -kv[1])[:5]
total_bytes = sum(v for _, v in top) or 1

COLORS = {
    "TypeScript": "#3178C6", "JavaScript": "#f1e05a", "Astro": "#ff5a03",
    "Python": "#3572A5", "Go": "#00ADD8", "Java": "#b07219",
    "CSS": "#663399", "HTML": "#e34c26", "Shell": "#89e051",
    "MDX": "#fcb32c", "Dockerfile": "#2496ED", "Vue": "#41b883",
}

tiles = [
    ("Total commits", total_commits),
    ("Stars", stars),
    ("Repos", public_repos),
    ("Contribs (1y)", contribs),
]

parts = [
    '<svg width="840" height="340" viewBox="0 0 840 340" '
    'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="mission control">',
    '<defs><linearGradient id="mbg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#0b1020"/><stop offset="1" stop-color="#140b26"/>'
    "</linearGradient>"
    '<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#6D28D9"/><stop offset="1" stop-color="#f0abfc"/>'
    "</linearGradient>"
    '<filter id="mglow" x="-30%" y="-30%" width="160%" height="160%">'
    '<feGaussianBlur stdDeviation="3" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    "</filter></defs>",
    '<rect x="2" y="2" width="836" height="336" rx="14" fill="url(#mbg)" '
    'stroke="#7c6cf055" stroke-width="1.5"/>',
    '<text x="26" y="40" font-family="Menlo, monospace" font-size="15" '
    'font-weight="700" fill="#f0abfc" filter="url(#mglow)">&#9656; MISSION CONTROL</text>',
    '<text x="814" y="40" text-anchor="end" font-family="Menlo, monospace" '
    'font-size="12" fill="#475569">live &#183; auto-updated</text>',
]

x = 26
for label, value in tiles:
    delay = round(0.1 + len(parts) * 0.001, 3)
    parts.append(
        f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur="0.5s" '
        f'begin="{delay}s" fill="freeze"/>'
        f'<rect x="{x}" y="62" width="190" height="76" rx="10" fill="#111834" '
        f'stroke="#7c6cf033"/>'
        f'<text x="{x + 95}" y="94" text-anchor="middle" font-family="Menlo, monospace" '
        f'font-size="12" fill="#64748b">{label}</text>'
        f'<text x="{x + 95}" y="122" text-anchor="middle" font-family="Menlo, monospace" '
        f'font-size="22" font-weight="700" fill="#e2e8f0">{value}</text></g>'
    )
    x += 200

parts.append(
    '<text x="26" y="178" font-family="Menlo, monospace" font-size="13" '
    'font-weight="700" fill="#67e8f9">&#9656; LANGUAGES (by bytes, public repos)</text>'
)

y = 210
bar_i = 0
for lang, b in top:
    pct = round(b / total_bytes * 100, 1)
    width = max(2, int(b / total_bytes * 300))
    color = COLORS.get(lang, "#a78bfa")
    parts.append(
        f'<text x="26" y="{y + 4}" font-family="Menlo, monospace" font-size="12" '
        f'fill="#94a3b8">{lang}</text>'
        f'<rect x="130" y="{y - 7}" width="300" height="10" rx="5" fill="#1e293b"/>'
        f'<rect x="130" y="{y - 7}" width="0" height="10" rx="5" fill="{color}">'
        f'<animate attributeName="width" from="0" to="{width}" dur="0.7s" '
        f'begin="{round(0.2 + bar_i * 0.15, 2)}s" fill="freeze"/></rect>'
        f'<text x="440" y="{y + 4}" font-family="Menlo, monospace" font-size="12" '
        f'fill="#64748b">{pct}%</text>'
    )
    y += 28
    bar_i += 1

parts.append("</svg>")

os.makedirs("assets", exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(parts))
print(f"rendered {OUT}: followers={followers} stars={stars} repos={public_repos} "
      f"contribs={contribs}")

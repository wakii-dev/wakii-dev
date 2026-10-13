#!/usr/bin/env python3
"""Render the profile 'mission control' stats panel as a self-hosted SVG.

Fetches live numbers from the GitHub REST/GraphQL API with the workflow's
GH_TOKEN (no third-party stat services), then writes assets/mission-control.svg.

Stats mirror what GitHub itself shows on the profile: per-type contributions
come from contributionsCollection (same source as the profile contribution
summary), so the panel always matches the real numbers. Reviews are shown
as the PR count per owner spec (PR reviews are not calendar-countable).
"""
import datetime as dt
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

# per-type contributions for the last year — the exact numbers GitHub's own
# profile summary shows (PRs, calendar total)
data = gql(
    "query($u:String!){ user(login:$u){ contributionsCollection { "
    "totalPullRequestContributions "
    "contributionCalendar { totalContributions } } } }",
    {"u": USER},
)
cc = data["user"]["contributionsCollection"]
prs = cc["totalPullRequestContributions"]
contribs = cc["contributionCalendar"]["totalContributions"]

# real commit volume: all commits landed on default branches of the public
# repos in the last 12 months, any author (the work is committed from
# personal + agent accounts, so GitHub's per-account
# totalCommitContributions undercounts badly); CI/bot commits excluded
SINCE = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)).strftime(
    "%Y-%m-%dT%H:%M:%SZ")
commits_1y = 0
for r in repos:
    page = 1
    while True:
        batch = api(f"/repos/{USER}/{r['name']}/commits?per_page=100"
                    f"&since={SINCE}&page={page}")
        if not batch:
            break
        for c in batch:
            login = ((c.get("author") or {}).get("login")) or ""
            if not login.endswith("[bot]"):
                commits_1y += 1
        if len(batch) < 100:
            break
        page += 1

# owner spec: reviews shown as the PR count (GitHub does not expose
# review contributions through the calendar)
reviews = prs

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
    ("Commits (1y)", commits_1y),
    ("Pull requests", prs),
    ("Reviews", reviews),
    ("Stars", stars),
    ("Repos", public_repos),
    ("Contribs (1y)", contribs),
]

parts = [
    '<svg width="840" height="340" viewBox="0 0 840 340" '
    'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="mission control">',
    "<style>"
    ":root{--bg1:#0b1020;--bg2:#140b26;--panel:#111834;--stroke:#7c6cf055;"
    "--stroke-soft:#7c6cf033;--accent:#f0abfc;--cyan:#67e8f9;"
    "--t1:#e2e8f0;--t2:#94a3b8;--t3:#64748b;--t4:#475569;--track:#1e293b}"
    "@media (prefers-color-scheme:light){:root{--bg1:#f8f7fc;--bg2:#f2ecfb;"
    "--panel:#ffffff;--stroke:#a78bfa66;--stroke-soft:#a78bfa40;"
    "--accent:#C026D3;--cyan:#0369a1;"
    "--t1:#1e293b;--t2:#475569;--t3:#64748b;--t4:#94a3b8;--track:#e2e8f0}}"
    ".bg1{stop-color:var(--bg1)}.bg2{stop-color:var(--bg2)}"
    ".panel{fill:var(--panel)}.frame{stroke:var(--stroke)}"
    ".title{fill:var(--accent)}.live{fill:var(--t4)}.sect{fill:var(--cyan)}"
    ".val{fill:var(--t1)}.lbl{fill:var(--t3)}"
    ".lang{fill:var(--t2)}.pct{fill:var(--t3)}.track{fill:var(--track)}"
    ".corner{stroke:var(--accent);fill:none;stroke-width:2;opacity:.5}"
    ".divider{stroke:var(--stroke-soft)}.ldot{fill:var(--ok)}"
    "</style>",
    '<defs><linearGradient id="mbg" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" class="bg1"/><stop offset="1" class="bg2"/>'
    "</linearGradient>"
    '<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#6D28D9"/><stop offset="1" stop-color="#f0abfc"/>'
    "</linearGradient>"
    '<filter id="mglow" x="-30%" y="-30%" width="160%" height="160%">'
    '<feGaussianBlur stdDeviation="3" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    "</filter></defs>",
    '<rect x="2" y="2" width="836" height="336" rx="14" fill="url(#mbg)" '
    'class="frame" stroke-width="1.5"/>',
    '<text x="26" y="40" font-family="Menlo, monospace" font-size="15" '
    'font-weight="700" class="title" filter="url(#mglow)">&#9656; MISSION CONTROL</text>',
    '<text x="814" y="40" text-anchor="end" font-family="Menlo, monospace" '
    'font-size="12" class="live">live &#183; auto-updated</text>',
    # HUD corner brackets
    '<path class="corner" d="M2 18 V9 Q2 2 9 2 H18"/>',
    '<path class="corner" d="M822 2 H831 Q838 2 838 9 V18"/>',
    '<path class="corner" d="M2 322 V331 Q2 338 9 338 H18"/>',
    '<path class="corner" d="M822 338 H831 Q838 338 838 331 V322"/>',
    # header divider + live pulse dot
    '<line x1="26" y1="54" x2="814" y2="54" class="divider"/>',
    '<circle cx="694" cy="36" r="3.5" class="ldot">'
    '<animate attributeName="opacity" values="1;0.25;1" dur="2.2s" repeatCount="indefinite"/></circle>',
]

# 6 tiles across: 26px side margins, 8px gaps
TILE_W, GAP, X0 = 124, 8, 26

x = X0
for label, value in tiles:
    delay = round(0.1 + len(parts) * 0.001, 3)
    # static-first: the real value renders without SMIL; the count-up frames
    # (base opacity 0, one short opacity window each, frozen back to 0) are
    # pure progressive enhancement for viewers that animate
    frames = sorted(set([0] + [int(value * i / 7) for i in range(1, 7)] + [int(value)]))
    m = len(frames)
    dur = 2.8
    stack = [
        f'<text x="{x + TILE_W // 2}" y="122" text-anchor="middle" '
        f'font-family="Menlo, monospace" font-size="20" font-weight="700" '
        f'class="val">{value:,}</text>'
    ]
    for i, v in enumerate(frames[:-1]):
        t0, t1 = round(i / m, 3), round((i + 1) / m, 3)
        if t1 >= 1.0:
            kts, vals = f"0;{t0};1", "0;1;0"
        else:
            kts, vals = f"0;{t0};{t1};1", "0;1;0;0"
        stack.append(
            f'<text x="{x + TILE_W // 2}" y="122" text-anchor="middle" '
            f'font-family="Menlo, monospace" font-size="20" font-weight="700" '
            f'class="val" opacity="0">{v:,}'
            f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" '
            f'calcMode="linear" dur="{dur}s" begin="{delay}s" fill="freeze" '
            f'repeatCount="1"/></text>'
        )
    parts.append(
        f'<g>'
        f'<rect x="{x}" y="62" width="{TILE_W}" height="76" rx="10" class="panel" '
        f'style="stroke:var(--stroke-soft)"/>'
        f'<text x="{x + TILE_W // 2}" y="94" text-anchor="middle" font-family="Menlo, monospace" '
        f'font-size="11" class="lbl">{label}</text>'
        + "".join(stack)
        + "</g>"
    )
    x += TILE_W + GAP

parts.append(
    '<text x="26" y="178" font-family="Menlo, monospace" font-size="13" '
    'font-weight="700" class="sect">&#9656; LANGUAGES (by bytes, public repos)</text>'
)

y = 210
bar_i = 0
for lang, b in top:
    pct = round(b / total_bytes * 100, 1)
    width = max(2, int(b / total_bytes * 300))
    color = COLORS.get(lang, "#a78bfa")
    parts.append(
        f'<text x="26" y="{y + 4}" font-family="Menlo, monospace" font-size="12" '
        f'class="lang">{lang}</text>'
        f'<rect x="130" y="{y - 7}" width="300" height="10" rx="5" class="track"/>'
        f'<rect x="130" y="{y - 7}" width="{width}" height="10" rx="5" fill="{color}">'
        f'<animate attributeName="width" from="0" to="{width}" dur="0.7s" '
        f'begin="{round(0.2 + bar_i * 0.15, 2)}s" fill="freeze"/></rect>'
        f'<text x="440" y="{y + 4}" font-family="Menlo, monospace" font-size="12" '
        f'class="pct">{pct}%</text>'
    )
    y += 28
    bar_i += 1

parts.append("</svg>")

os.makedirs("assets", exist_ok=True)
with open(OUT, "w") as f:
    f.write("\n".join(parts))
print(f"rendered {OUT}: commits(1y)={commits_1y} prs={prs} reviews={reviews} "
      f"stars={stars} repos={public_repos} contribs={contribs}")

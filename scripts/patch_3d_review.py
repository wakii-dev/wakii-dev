#!/usr/bin/env python3
"""Set the Review axis of the 3d-contrib radar chart to the PR count.

github-profile-3d-contrib plots the radar's Review axis from
totalPullRequestReviewContributions, which stays near zero when reviews
come from bot/agent runs (GitHub does not count them). Per owner spec the
Review axis mirrors the PR count instead: rescale the radar polygon's
Review vertex to the same radius as the PullReq vertex (the radar is
log-scale, so equal values get equal radii) and rewrite the axis label.

Runs on every profile-3d-contrib/profile-*.svg right after the action,
before the dark-patch step.
"""
import json
import math
import os
import re
import urllib.request

TOKEN = os.environ["GH_TOKEN"]
USER = os.environ["USER"]

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({
        "query": "query($u:String!){ user(login:$u){ contributionsCollection "
                 "{ totalPullRequestContributions } } }",
        "variables": {"u": USER},
    }).encode(),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "User-Agent": "profile-stats",
        "Content-Type": "application/json",
    },
)
with urllib.request.urlopen(req, timeout=30) as r:
    prs = json.load(r)["data"]["user"]["contributionsCollection"][
        "totalPullRequestContributions"]

PT = re.compile(r"-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?")
POLY = re.compile(r'<polygon[^>]*?points="((?:\s*-?[\d.]+,-?[\d.]+){5})\s*"')

patched = []
for name in sorted(os.listdir("profile-3d-contrib")):
    if not name.endswith(".svg"):
        continue
    path = os.path.join("profile-3d-contrib", name)
    with open(path) as f:
        svg = f.read()

    m = re.search(r">Review<title>-?\d+</title>", svg)
    if not m:
        continue  # variant without the radar

    # data polygon = the 5-vertex polygon nearest after the Review label
    polys = [p for p in POLY.finditer(svg) if p.start() > m.end()]
    if not polys:
        continue
    poly = polys[0]
    pts = [complex(*map(float, s.split(","))) for s in PT.findall(poly.group(1))]
    pr_vertex, review_vertex = pts[2], pts[3]

    # Review axis direction from its axis line's outer endpoint
    ax = re.search(
        r'<g class="axis"><line x1="-?[\d.]+" y1="-?[\d.]+" '
        r'x2="(-?[\d.]+)" y2="(-?[\d.]+)"[^>]*></line>'
        r'<text[^>]*>Review<title>', svg)
    if not ax:
        continue
    ux, uy = float(ax.group(1)), float(ax.group(2))
    norm = math.hypot(ux, uy)
    ux, uy = ux / norm, uy / norm

    radius = abs(pr_vertex)  # same value => same radius on the log scale
    new = complex(round(radius * ux, 2), round(radius * uy, 2))
    old_str = f"{review_vertex.real:.2f},{review_vertex.imag:.2f}"
    new_str = f"{new.real:.2f},{new.imag:.2f}"
    if old_str == new_str and f">Review<title>{prs}</title>" in svg:
        continue  # already up to date

    seg_start, seg_end = poly.start(), svg.find("</polygon>", poly.start())
    seg = svg[seg_start:seg_end].replace(old_str, new_str)
    svg = svg[:seg_start] + seg + svg[seg_end:]
    svg = re.sub(r"(>Review<title>)-?\d+(</title>)", rf"\g<1>{prs}\g<2>", svg)

    with open(path, "w") as f:
        f.write(svg)
    patched.append(name)

print(f"radar Review axis set to PR count ({prs}) in {len(patched)} files: "
      + ", ".join(patched))

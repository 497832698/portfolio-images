#!/usr/bin/env python3
"""Generate portfolio index.html from data.json"""
import json
from pathlib import Path

BASE = "https://raw.githubusercontent.com/497832698/portfolio-images/main/img"

def e(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_card(item):
    img = item.get("主图","")
    detail = item.get("详情图","")
    img_tag = f'<img src="{BASE}/{img}" alt="{e(item["描述"])}" loading="lazy"/>' if img else '<div class="img-placeholder"></div>'
    detail_attr = f' data-img="{BASE}/{detail}"' if detail and len(detail) < 80 else ""
    rating = item.get("评分", 5)
    stars = "★" * int(rating) + ("☆" if rating != int(rating) else "")
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in item.get("标签",[]))
    return f'''      <div class="work-card" onclick="openDetail('{e(item["描述"])}', ''{detail_attr})">
        {img_tag}
        <div class="work-card-body">
          <div class="work-name">{e(item["名称"])}</div>
          <div class="work-desc">{e(item["描述"])}</div>
          <div class="work-rating">{stars}</div>
          {tags}
        </div>
      </div>'''

def build_works_js(data):
    lines = []
    for cat in data.get("作品集",[]):
        cat_key = cat["分类键"]
        items = cat.get("作品",[])
        cards = "\n".join(build_card(it) for it in items)
        lines.append(f"    {cat_key}: [\n{cards}\n    ]")
    return "{\n  " + ",\n  ".join(l.split("{")[0].rstrip(", ") + "{" if i > 0 else l for i, l in enumerate(lines)) + "\n  }"

# Fix: build properly
works_parts = []
for cat in data.get("作品集",[]):
    cat_key = cat["分类键"]
    cards = "\n".join(build_card(it) for it in cat.get("作品",[]))
    works_parts.append(f"    {cat_key}: [\n{cards}\n    ]")
works_js = "{\n  " + ",\n  ".join(works_parts) + "\n  }"

cats_js_parts = []
for cat in data.get("作品集",[]):
    key = cat["分类键"]
    cats_js_parts.append(f'    {key}: {{title: "{e(cat["分类名"])}", count: "{e(cat["职位"])}"}}')
cats_js = "{\n  " + ",\n    ".join(cats_js_parts) + "\n  }"

print(f"Works parts: {len(works_parts)} categories")
print(cats_js)

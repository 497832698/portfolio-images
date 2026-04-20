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
    detail_img_attr = f' data-img="{BASE}/{detail}"' if detail and len(detail) < 80 else ''
    rating = item.get("评分", 5)
    half = "" if rating == int(rating) else ".5"
    stars = "★" * int(rating) + ("☆" if rating != int(rating) else "")
    tags = "".join(f'<span class="tag">{e(t)}</span>' for t in item.get("标签",[]))
    name = e(item["名称"])
    desc = e(item["描述"])
    return f'''      <div class="work-card" onclick="openDetail('{desc}', ''{detail_img_attr})">
        {img_tag}
        <div class="work-card-body">
          <div class="work-name">{name}</div>
          <div class="work-desc">{desc}</div>
          <div class="work-rating">{stars}</div>
          {tags}
        </div>
      </div>'''

def generate():
    data = json.loads(Path("data.json").read_text())
    info = data.get("个人信息", {})
    works_data = {}
    cats_data = {}

    for cat in data.get("作品集", []):
        key = cat["分类键"]
        cats_data[key] = {"title": cat["分类名"], "count": cat["职位"]}
        cards = [build_card(item) for item in cat.get("作品", [])]
        works_data[key] = "\n".join(cards)

    # Read template
    html = Path("template.html").read_text()

    # Replace CATEGORIES
    cats_lines = []
    for k, v in cats_data.items():
        cats_lines.append(f'    {k}: {{title: "{v["title"]}", count: "{v["count"]}"}}')
    cats_js = "{\n  " + ",\n  ".join(cats_lines) + "\n  }"
    html = html.replace("{{CATEGORIES}}", cats_js)

    # Replace WORKS_DATA
    works_lines = []
    for k, cards in works_data.items():
        works_lines.append(f"    {k}: [\n{cards}\n    ]")
    works_js = "{\n  " + ",\n  ".join(works_lines) + "\n  }"
    html = html.replace("{{WORKS_DATA}}", works_js)

    # Replace personal info
    html = html.replace("{{PERSONAL_INFO}}", json.dumps(info, ensure_ascii=False))

    Path("index.html").write_text(html)
    total = sum(len(cat.get("作品",[])) for cat in data.get("作品集",[]))
    print(f"Generated index.html: {len(cats_data)} categories, {total} works")

if __name__ == "__main__":
    generate()

#!/usr/bin/env python3
"""Generate portfolio index.html from data.json"""
import json
from pathlib import Path

BASE = "https://raw.githubusercontent.com/497832698/portfolio-images/main/img"

def e(s):
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def build_item(item):
    img = item.get("主图","")
    detail = item.get("详情图","")
    name = e(item["名称"])
    desc = e(item["描述"])
    rating = item.get("评分", 5)
    tags = str(item.get("标签",[]))
    img_attr = f", img: '{img}'" if img else ""
    detail_attr = f", detailImg: '{detail}'" if detail and len(detail) < 80 else ""
    return f"      {{name: '{name}', desc: '{desc}'{img_attr}{detail_attr}, rating: {rating}, tags: {tags}}}"

def generate():
    data = json.loads(Path("data.json").read_text())

    # Build CATEGORIES JS
    cats_lines = []
    for cat in data.get("作品集", []):
        key = cat["分类键"]
        cats_lines.append(f"    '{key}': {{title: '{cat['分类名']}', count: '{cat.get('职位','')}'}}")
    cats_js = "{\n  " + ",\n  ".join(cats_lines) + "\n  }"

    # Build WORKS_DATA JS
    works_lines = []
    for cat in data.get("作品集", []):
        key = cat["分类键"]
        items = [build_item(item) for item in cat.get("作品", [])]
        works_lines.append(f"    '{key}': [\n" + ",\n".join(items) + "\n    ]")
    works_js = "{\n  " + ",\n  ".join(works_lines) + "\n  }"

    # Read template
    html = Path("template.html").read_text()

    # Replace CATEGORIES block
    start = html.find("const CATEGORIES = {")
    end = html.find("};", start) + 2
    html = html[:start] + "const CATEGORIES = " + cats_js + ";" + html[end:]

    # Replace WORKS_DATA block
    start = html.find("const WORKS_DATA = {")
    end = html.find("};", start) + 2
    html = html[:start] + "const WORKS_DATA = " + works_js + ";" + html[end:]

    Path("index.html").write_text(html)
    total = sum(len(cat.get("作品",[])) for cat in data.get("作品集",[]))
    print(f"Generated index.html: {len(cats_lines)} categories, {total} works")

if __name__ == "__main__":
    generate()

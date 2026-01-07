#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

client = get_supabase_client()

cats = client.table(Tables.CATEGORIES).select("id, title, description").order("title").execute()
cat_map = {c["id"]: c for c in cats.data}

decks = client.table(Tables.DECKS).select("title, title_ko, icon, color, category_id").order("category_id, title").execute()

print("=" * 70)
print("데크 업데이트 결과")
print("=" * 70)

current_cat = None
colors_used = set()

for d in decks.data:
    cat = cat_map.get(d["category_id"], {})
    cat_title = cat.get("title", "Unknown")

    if cat_title != current_cat:
        current_cat = cat_title
        cat_desc = cat.get("description", "")
        print(f"\n[{cat_title}] {cat_desc}")
        print("-" * 60)

    color = d["color"]
    icon = d["icon"] or "-"
    title_ko = d["title_ko"] or "-"

    colors_used.add(color)
    print(f"  {color}  {icon:<22} {title_ko}")

print("\n" + "=" * 70)
print(f"총 {len(decks.data)}개 데크")
print(f"사용된 색상: {len(colors_used)}개 (중복 없음: {len(colors_used) == len(decks.data)})")
print("=" * 70)

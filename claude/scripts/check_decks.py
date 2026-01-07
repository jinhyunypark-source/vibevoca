#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

client = get_supabase_client()

cats = client.table(Tables.CATEGORIES).select("id, title").execute()
cat_map = {c["id"]: c["title"] for c in cats.data}

decks = client.table(Tables.DECKS).select("title, title_ko, icon, color, category_id").order("category_id, title").execute()

print("=== 현재 데크 상태 ===\n")
current_cat = None
count = 0
for d in decks.data:
    cat_title = cat_map.get(d["category_id"], "Unknown")
    if cat_title != current_cat:
        current_cat = cat_title
        print(f"\n[{cat_title}]")
    ko = d.get("title_ko") or "-"
    icon = d.get("icon") or "-"
    color = d.get("color") or "-"
    print(f"  {d['title']}")
    count += 1

print(f"\n총 {count}개 데크")

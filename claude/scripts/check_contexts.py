#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

client = get_supabase_client()

contexts = client.table(Tables.CONTEXTS).select("*").order("type, slug").execute()

print("=== 현재 contexts 테이블 ===\n")

if not contexts.data:
    print("(데이터 없음)")
else:
    current_type = None
    for c in contexts.data:
        if c["type"] != current_type:
            current_type = c["type"]
            print(f"\n[{current_type}]")

        icon = c.get("icon") or "-"
        prompt = c.get("prompt_description") or "-"
        print(f"  {c['slug']:<20} | {c['label']:<15} | icon: {icon}")
        if prompt != "-":
            print(f"    prompt: {prompt[:60]}...")

print(f"\n총 {len(contexts.data)}개")

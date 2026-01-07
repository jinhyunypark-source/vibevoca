#!/usr/bin/env python3
"""
contexts 테이블 업데이트: place, emotion, environment
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

# 새로운 contexts 데이터 정의
CONTEXTS = [
    # === PLACE (장소) ===
    {
        "type": "place",
        "slug": "place_home",
        "label": "Home",
        "label_ko": "집",
        "icon": "home",
        "prompt_description": "At home in a comfortable and relaxed environment, perhaps in the living room or bedroom."
    },
    {
        "type": "place",
        "slug": "place_work",
        "label": "Work",
        "label_ko": "직장",
        "icon": "work",
        "prompt_description": "At the workplace, in an office or professional setting with colleagues around."
    },
    {
        "type": "place",
        "slug": "place_transport",
        "label": "Transport",
        "label_ko": "이동중",
        "icon": "directions_transit",
        "prompt_description": "While commuting or traveling, on a bus, subway, train, or in a car."
    },

    # === EMOTION (감정) ===
    {
        "type": "emotion",
        "slug": "emotion_happy",
        "label": "Happy",
        "label_ko": "행복",
        "icon": "sentiment_very_satisfied",
        "prompt_description": "Feeling happy, joyful, and in a positive mood with a sense of well-being."
    },
    {
        "type": "emotion",
        "slug": "emotion_sad",
        "label": "Sad",
        "label_ko": "슬픔",
        "icon": "sentiment_very_dissatisfied",
        "prompt_description": "Feeling sad, down, or melancholic with a heavy heart."
    },
    {
        "type": "emotion",
        "slug": "emotion_angry",
        "label": "Angry",
        "label_ko": "분노",
        "icon": "mood_bad",
        "prompt_description": "Feeling angry, frustrated, or irritated about something."
    },

    # === ENVIRONMENT (환경) ===
    {
        "type": "environment",
        "slug": "env_sunny",
        "label": "Sunny",
        "label_ko": "맑음",
        "icon": "wb_sunny",
        "prompt_description": "On a bright sunny day with clear blue skies and warm sunlight."
    },
    {
        "type": "environment",
        "slug": "env_rainy",
        "label": "Rainy",
        "label_ko": "비",
        "icon": "water_drop",
        "prompt_description": "On a rainy day with raindrops falling and gray skies."
    },
    {
        "type": "environment",
        "slug": "env_hot",
        "label": "Hot",
        "label_ko": "더움",
        "icon": "local_fire_department",
        "prompt_description": "In hot weather, feeling the heat of summer or a warm climate."
    },
    {
        "type": "environment",
        "slug": "env_cold",
        "label": "Cold",
        "label_ko": "추움",
        "icon": "ac_unit",
        "prompt_description": "In cold weather, feeling the chill of winter or a cold environment."
    },
    {
        "type": "environment",
        "slug": "env_warm",
        "label": "Warm",
        "label_ko": "따뜻함",
        "icon": "thermostat",
        "prompt_description": "In comfortably warm weather, pleasant temperature with a cozy feeling."
    },
]


def main():
    client = get_supabase_client()

    print("=" * 60)
    print("contexts 테이블 업데이트")
    print("=" * 60)

    # 1. 기존 데이터 조회
    existing = client.table(Tables.CONTEXTS).select("id, slug").execute()
    existing_map = {c["slug"]: c["id"] for c in existing.data}
    print(f"\n기존 데이터: {len(existing.data)}개")

    # 2. 새 데이터 정의된 slug 목록
    new_slugs = {c["slug"] for c in CONTEXTS}

    # 3. 삭제할 데이터 (정의에 없는 것)
    to_delete = [slug for slug in existing_map if slug not in new_slugs]
    if to_delete:
        print(f"\n삭제할 데이터: {to_delete}")
        for slug in to_delete:
            client.table(Tables.CONTEXTS).delete().eq("slug", slug).execute()
            print(f"  - {slug} 삭제됨")

    # 4. 데이터 upsert (있으면 업데이트, 없으면 추가)
    print(f"\n데이터 upsert...")

    for ctx in CONTEXTS:
        slug = ctx["slug"]

        if slug in existing_map:
            # 업데이트
            client.table(Tables.CONTEXTS).update({
                "type": ctx["type"],
                "label": ctx["label"],
                "icon": ctx["icon"],
                "prompt_description": ctx["prompt_description"],
            }).eq("slug", slug).execute()
            print(f"  ✓ {slug} (업데이트)")
        else:
            # 추가
            client.table(Tables.CONTEXTS).insert({
                "type": ctx["type"],
                "slug": ctx["slug"],
                "label": ctx["label"],
                "icon": ctx["icon"],
                "prompt_description": ctx["prompt_description"],
            }).execute()
            print(f"  + {slug} (추가)")

    # 5. 결과 확인
    final = client.table(Tables.CONTEXTS).select("*").order("type, slug").execute()

    print(f"\n" + "=" * 60)
    print("결과")
    print("=" * 60)

    current_type = None
    for c in final.data:
        if c["type"] != current_type:
            current_type = c["type"]
            print(f"\n[{current_type}]")

        print(f"  {c['icon']:<25} {c['label']:<10} ({c['slug']})")

    print(f"\n총 {len(final.data)}개 contexts")
    print("=" * 60)


if __name__ == "__main__":
    main()

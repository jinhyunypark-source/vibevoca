#!/usr/bin/env python3
"""
데크를 10개 카테고리로 재매핑하는 스크립트
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

# 10개 카테고리 정의
CATEGORIES = [
    {"title": "COMMUNICATION", "description": "의사소통"},
    {"title": "SENSE_STYLE", "description": "감각과 스타일"},
    {"title": "INTELLIGENCE_JUDGMENT", "description": "Intelligence & Judgment"},
    {"title": "RELATIONSHIPS_SOCIAL", "description": "인간관계와 유대감 (Relationships & Social Interaction)"},
    {"title": "CHANGE_GROWTH_DECLINE", "description": "변화와 성장/쇠퇴 (Change, Growth & Decline)"},
    {"title": "DIFFICULTY_COMPLEXITY", "description": "난이도와 복잡성 (Difficulty & Complexity)"},
    {"title": "POWER_AUTHORITY", "description": "권력, 영향력, 지배 (Power, Authority & Influence)"},
    {"title": "SIZE_QUANTITY_SCOPE", "description": "크기, 양, 범위 (Size, Quantity & Scope)"},
    {"title": "MONEY_FINANCE", "description": "돈과 경제적 상태 (Money & Finance)"},
    {"title": "TIME_DURATION_FREQUENCY", "description": "시간과 빈도 (Time, Duration & Frequency)"},
]

# 데크 -> 카테고리 매핑
DECK_TO_CATEGORY = {
    # 1. 의사소통 (Communication)
    "BREVITY_VERBOSITY": "COMMUNICATION",
    "PERSUASION_CONFLICT": "COMMUNICATION",
    "LOGIC_CLARITY": "COMMUNICATION",
    "FLUENCY_DELIVERY": "COMMUNICATION",
    "ATTITUDE_TONE": "COMMUNICATION",

    # 2. 감각과 스타일 (Sense & Style)
    "SIGHT": "SENSE_STYLE",
    "AESTHETIC_SENSE": "SENSE_STYLE",
    "TASTE": "SENSE_STYLE",
    "SOUND_AUDITORY": "SENSE_STYLE",
    "TOUCH_TEXTURE": "SENSE_STYLE",
    "SMELL_SCENT": "SENSE_STYLE",

    # 3. Intelligence & Judgment
    "1_GENERAL_INTELLIGENCE_BRILLIANCE": "INTELLIGENCE_JUDGMENT",
    "2_WISDOM_INSIGHT_PRUDENCE": "INTELLIGENCE_JUDGMENT",
    "PRACTICALITY_WIT_CUNNING": "INTELLIGENCE_JUDGMENT",
    "STUPIDITY_DULLNESS": "INTELLIGENCE_JUDGMENT",
    "IGNORANCE_NAIVETY_CONFUSION": "INTELLIGENCE_JUDGMENT",

    # 4. 인간관계와 유대감 (Relationships & Social Interaction)
    "SIGNIFICANCE_DEPTH": "RELATIONSHIPS_SOCIAL",
    "INTIMACY_AFFECTION": "RELATIONSHIPS_SOCIAL",
    "SOCIAL_STATUS_CONNECTION": "RELATIONSHIPS_SOCIAL",
    "COOPERATION_HARMONY": "RELATIONSHIPS_SOCIAL",
    "CONFLICT_DISTANCE": "RELATIONSHIPS_SOCIAL",
    "SOCIAL_BEHAVIOR_PERSONALITY": "RELATIONSHIPS_SOCIAL",

    # 5. 변화와 성장/쇠퇴 (Change, Growth & Decline)
    "GROWTH_PROSPERITY": "CHANGE_GROWTH_DECLINE",
    "DECLINE_DETERIORATION": "CHANGE_GROWTH_DECLINE",
    "TRANSFORMATION_ADAPTATION": "CHANGE_GROWTH_DECLINE",
    "FLUCTUATION_STAGNATION": "CHANGE_GROWTH_DECLINE",
    "START_END_RECOVERY": "CHANGE_GROWTH_DECLINE",

    # 6. 난이도와 복잡성 (Difficulty & Complexity)
    "HIGH_DIFFICULTY_EFFORT": "DIFFICULTY_COMPLEXITY",
    "LOW_DIFFICULTY_EASE": "DIFFICULTY_COMPLEXITY",
    "COMPLEXITY_INTRICACY": "DIFFICULTY_COMPLEXITY",
    "SIMPLICITY_CLARITY": "DIFFICULTY_COMPLEXITY",

    # 7. 권력, 영향력, 지배 (Power, Authority & Influence)
    "DOMINANCE_CONTROL": "POWER_AUTHORITY",
    "OPPRESSION_TYRANNY": "POWER_AUTHORITY",
    "SUBMISSION_COMPLIANCE": "POWER_AUTHORITY",
    "AUTHORITY_PRESTIGE": "POWER_AUTHORITY",
    "AUTONOMY_LENIENCY": "POWER_AUTHORITY",

    # 8. 크기, 양, 범위 (Size, Quantity & Scope)
    "ENORMOUSNESS_VASTNESS": "SIZE_QUANTITY_SCOPE",
    "MINUTENESS_SMALLNESS": "SIZE_QUANTITY_SCOPE",
    "ABUNDANCE_EXCESS": "SIZE_QUANTITY_SCOPE",
    "SCARCITY_DEFICIENCY": "SIZE_QUANTITY_SCOPE",
    "SCOPE_COMPREHENSIVENESS": "SIZE_QUANTITY_SCOPE",

    # 9. 돈과 경제적 상태 (Money & Finance)
    "WEALTH_AFFLUENCE": "MONEY_FINANCE",
    "POVERTY_HARDSHIP": "MONEY_FINANCE",
    "FRUGALITY_STINGINESS": "MONEY_FINANCE",
    "LUXURY_EXTRAVAGANCE": "MONEY_FINANCE",
    "COST_PRICE_VALUE": "MONEY_FINANCE",
    "INCOME_PROFIT_FINANCIAL_STATUS": "MONEY_FINANCE",

    # 10. 시간과 빈도 (Time, Duration & Frequency)
    "PERMANENCE_LONGEVITY": "TIME_DURATION_FREQUENCY",
    "TRANSIENCE_BREVITY": "TIME_DURATION_FREQUENCY",
    "FREQUENCY_REPETITION": "TIME_DURATION_FREQUENCY",
    "TIMING_SPEED_PUNCTUALITY": "TIME_DURATION_FREQUENCY",
    "SEQUENCE_INTERVAL_DURATION": "TIME_DURATION_FREQUENCY",
    "TIMELINESS_FUTURE_PAST": "TIME_DURATION_FREQUENCY",
}


def main():
    client = get_supabase_client()

    print("=" * 60)
    print("데크 카테고리 재매핑 스크립트")
    print("=" * 60)

    # 1. 기존 카테고리 조회
    existing_cats = client.table(Tables.CATEGORIES).select("*").execute()
    cat_by_title = {c["title"]: c for c in existing_cats.data}

    print(f"\n[1] 기존 카테고리: {len(existing_cats.data)}개")
    for c in existing_cats.data:
        print(f"    - {c['title']}")

    # 2. 새 카테고리 생성 (없는 것만)
    print(f"\n[2] 카테고리 생성/확인...")
    category_ids = {}

    for cat in CATEGORIES:
        if cat["title"] in cat_by_title:
            category_ids[cat["title"]] = cat_by_title[cat["title"]]["id"]
            print(f"    ✓ {cat['title']} (기존)")
        else:
            # 새로 생성
            result = client.table(Tables.CATEGORIES).insert({
                "title": cat["title"],
                "description": cat["description"]
            }).execute()
            category_ids[cat["title"]] = result.data[0]["id"]
            print(f"    + {cat['title']} (신규 생성)")

    # 3. 데크 조회
    decks = client.table(Tables.DECKS).select("id, title, category_id").execute()
    print(f"\n[3] 데크 재매핑 ({len(decks.data)}개)...")

    updated = 0
    skipped = 0
    unmapped = []

    for deck in decks.data:
        deck_title = deck["title"]

        if deck_title not in DECK_TO_CATEGORY:
            unmapped.append(deck_title)
            continue

        target_cat_title = DECK_TO_CATEGORY[deck_title]
        target_cat_id = category_ids[target_cat_title]

        # 현재 카테고리와 다르면 업데이트
        if deck["category_id"] != target_cat_id:
            client.table(Tables.DECKS).update({
                "category_id": target_cat_id
            }).eq("id", deck["id"]).execute()
            print(f"    ✓ {deck_title} -> {target_cat_title}")
            updated += 1
        else:
            skipped += 1

    print(f"\n[4] 결과:")
    print(f"    - 업데이트됨: {updated}개")
    print(f"    - 변경 없음: {skipped}개")

    if unmapped:
        print(f"    - 매핑 안됨: {len(unmapped)}개")
        for u in unmapped:
            print(f"        ! {u}")

    # 4. GENERAL 카테고리 삭제 (더 이상 사용 안 함)
    print(f"\n[5] 미사용 카테고리 정리...")

    # GENERAL 카테고리에 속한 데크가 있는지 확인
    if "GENERAL" in cat_by_title:
        general_id = cat_by_title["GENERAL"]["id"]
        remaining = client.table(Tables.DECKS).select("id").eq("category_id", general_id).execute()

        if len(remaining.data) == 0:
            client.table(Tables.CATEGORIES).delete().eq("id", general_id).execute()
            print(f"    - GENERAL 카테고리 삭제됨 (비어있음)")
        else:
            print(f"    - GENERAL 카테고리 유지 ({len(remaining.data)}개 데크 남음)")

    print("\n" + "=" * 60)
    print("완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()

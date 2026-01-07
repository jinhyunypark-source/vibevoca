#!/usr/bin/env python3
"""
데크 테이블 업데이트: title_ko, icon, color
- 카테고리별 대표색 + 파생색
- 53개 데크 모두 다른 색상
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables

# 카테고리별 대표색 (HSL 기반으로 파생색 생성)
# 형식: "카테고리": (기본 Hex, [파생색 리스트])
CATEGORY_COLORS = {
    # 1. 의사소통 - 파란색 계열
    "COMMUNICATION": ["#3B82F6", "#2563EB", "#1D4ED8", "#60A5FA", "#93C5FD"],

    # 2. 감각과 스타일 - 보라색 계열
    "SENSE_STYLE": ["#8B5CF6", "#7C3AED", "#6D28D9", "#A78BFA", "#C4B5FD", "#5B21B6"],

    # 3. 지성과 판단 - 분홍/마젠타 계열
    "INTELLIGENCE_JUDGMENT": ["#EC4899", "#DB2777", "#BE185D", "#F472B6", "#F9A8D4"],

    # 4. 인간관계 - 주황색 계열
    "RELATIONSHIPS_SOCIAL": ["#F97316", "#EA580C", "#C2410C", "#FB923C", "#FDBA74", "#9A3412"],

    # 5. 변화와 성장 - 초록색 계열
    "CHANGE_GROWTH_DECLINE": ["#22C55E", "#16A34A", "#15803D", "#4ADE80", "#86EFAC"],

    # 6. 난이도와 복잡성 - 슬레이트/회색 계열
    "DIFFICULTY_COMPLEXITY": ["#64748B", "#475569", "#334155", "#94A3B8"],

    # 7. 권력과 영향력 - 노란색/금색 계열
    "POWER_AUTHORITY": ["#EAB308", "#CA8A04", "#A16207", "#FACC15", "#FDE047"],

    # 8. 크기, 양, 범위 - 청록색/시안 계열
    "SIZE_QUANTITY_SCOPE": ["#06B6D4", "#0891B2", "#0E7490", "#22D3EE", "#67E8F9"],

    # 9. 돈과 경제 - 에메랄드/녹색 계열
    "MONEY_FINANCE": ["#10B981", "#059669", "#047857", "#34D399", "#6EE7B7", "#065F46"],

    # 10. 시간과 빈도 - 빨간색 계열
    "TIME_DURATION_FREQUENCY": ["#EF4444", "#DC2626", "#B91C1C", "#F87171", "#FCA5A5", "#991B1B"],
}

# 데크별 상세 정보: title_ko, icon
# icon은 Material Icons 이름 사용
DECK_INFO = {
    # === COMMUNICATION (의사소통) ===
    "LOGIC_CLARITY": {
        "title_ko": "논리와 명확성",
        "icon": "psychology",
    },
    "FLUENCY_DELIVERY": {
        "title_ko": "유창성과 전달력",
        "icon": "record_voice_over",
    },
    "ATTITUDE_TONE": {
        "title_ko": "태도와 어조",
        "icon": "sentiment_satisfied",
    },
    "BREVITY_VERBOSITY": {
        "title_ko": "간결함과 장황함",
        "icon": "short_text",
    },
    "PERSUASION_CONFLICT": {
        "title_ko": "설득과 갈등",
        "icon": "handshake",
    },

    # === SENSE_STYLE (감각과 스타일) ===
    "SIGHT": {
        "title_ko": "시각",
        "icon": "visibility",
    },
    "SOUND_AUDITORY": {
        "title_ko": "청각",
        "icon": "hearing",
    },
    "TASTE": {
        "title_ko": "미각",
        "icon": "restaurant",
    },
    "SMELL_SCENT": {
        "title_ko": "후각",
        "icon": "air",
    },
    "TOUCH_TEXTURE": {
        "title_ko": "촉각",
        "icon": "touch_app",
    },
    "AESTHETIC_SENSE": {
        "title_ko": "미적 감각",
        "icon": "palette",
    },

    # === INTELLIGENCE_JUDGMENT (지성과 판단) ===
    "1_GENERAL_INTELLIGENCE_BRILLIANCE": {
        "title_ko": "지성과 총명함",
        "icon": "lightbulb",
    },
    "2_WISDOM_INSIGHT_PRUDENCE": {
        "title_ko": "지혜와 통찰력",
        "icon": "self_improvement",
    },
    "PRACTICALITY_WIT_CUNNING": {
        "title_ko": "실용성과 재치",
        "icon": "tips_and_updates",
    },
    "STUPIDITY_DULLNESS": {
        "title_ko": "어리석음과 둔함",
        "icon": "block",
    },
    "IGNORANCE_NAIVETY_CONFUSION": {
        "title_ko": "무지와 혼란",
        "icon": "help_outline",
    },

    # === RELATIONSHIPS_SOCIAL (인간관계) ===
    "INTIMACY_AFFECTION": {
        "title_ko": "친밀함과 애정",
        "icon": "favorite",
    },
    "SOCIAL_STATUS_CONNECTION": {
        "title_ko": "사회적 지위와 연결",
        "icon": "groups",
    },
    "COOPERATION_HARMONY": {
        "title_ko": "협력과 조화",
        "icon": "diversity_3",
    },
    "CONFLICT_DISTANCE": {
        "title_ko": "갈등과 거리",
        "icon": "remove_circle",
    },
    "SOCIAL_BEHAVIOR_PERSONALITY": {
        "title_ko": "사회적 행동과 성격",
        "icon": "person",
    },
    "SIGNIFICANCE_DEPTH": {
        "title_ko": "중요성과 깊이",
        "icon": "diamond",
    },

    # === CHANGE_GROWTH_DECLINE (변화와 성장) ===
    "GROWTH_PROSPERITY": {
        "title_ko": "성장과 번영",
        "icon": "trending_up",
    },
    "DECLINE_DETERIORATION": {
        "title_ko": "쇠퇴와 악화",
        "icon": "trending_down",
    },
    "TRANSFORMATION_ADAPTATION": {
        "title_ko": "변화와 적응",
        "icon": "autorenew",
    },
    "FLUCTUATION_STAGNATION": {
        "title_ko": "변동과 정체",
        "icon": "swap_vert",
    },
    "START_END_RECOVERY": {
        "title_ko": "시작, 끝, 회복",
        "icon": "replay",
    },

    # === DIFFICULTY_COMPLEXITY (난이도와 복잡성) ===
    "HIGH_DIFFICULTY_EFFORT": {
        "title_ko": "높은 난이도와 노력",
        "icon": "fitness_center",
    },
    "LOW_DIFFICULTY_EASE": {
        "title_ko": "낮은 난이도와 용이함",
        "icon": "spa",
    },
    "COMPLEXITY_INTRICACY": {
        "title_ko": "복잡성과 정교함",
        "icon": "hub",
    },
    "SIMPLICITY_CLARITY": {
        "title_ko": "단순함과 명료함",
        "icon": "circle",
    },

    # === POWER_AUTHORITY (권력과 영향력) ===
    "DOMINANCE_CONTROL": {
        "title_ko": "지배와 통제",
        "icon": "gavel",
    },
    "OPPRESSION_TYRANNY": {
        "title_ko": "억압과 폭정",
        "icon": "block",
    },
    "SUBMISSION_COMPLIANCE": {
        "title_ko": "복종과 순응",
        "icon": "volunteer_activism",
    },
    "AUTHORITY_PRESTIGE": {
        "title_ko": "권위와 명성",
        "icon": "military_tech",
    },
    "AUTONOMY_LENIENCY": {
        "title_ko": "자율성과 관용",
        "icon": "diversity_1",
    },

    # === SIZE_QUANTITY_SCOPE (크기, 양, 범위) ===
    "ENORMOUSNESS_VASTNESS": {
        "title_ko": "거대함과 광대함",
        "icon": "open_in_full",
    },
    "MINUTENESS_SMALLNESS": {
        "title_ko": "미세함과 작음",
        "icon": "close_fullscreen",
    },
    "ABUNDANCE_EXCESS": {
        "title_ko": "풍요와 과잉",
        "icon": "inventory_2",
    },
    "SCARCITY_DEFICIENCY": {
        "title_ko": "희소성과 결핍",
        "icon": "inventory",
    },
    "SCOPE_COMPREHENSIVENESS": {
        "title_ko": "범위와 포괄성",
        "icon": "zoom_out_map",
    },

    # === MONEY_FINANCE (돈과 경제) ===
    "WEALTH_AFFLUENCE": {
        "title_ko": "부유함과 풍요",
        "icon": "account_balance",
    },
    "POVERTY_HARDSHIP": {
        "title_ko": "가난과 고난",
        "icon": "money_off",
    },
    "FRUGALITY_STINGINESS": {
        "title_ko": "검소함과 인색함",
        "icon": "savings",
    },
    "LUXURY_EXTRAVAGANCE": {
        "title_ko": "사치와 낭비",
        "icon": "diamond",
    },
    "COST_PRICE_VALUE": {
        "title_ko": "비용과 가치",
        "icon": "sell",
    },
    "INCOME_PROFIT_FINANCIAL_STATUS": {
        "title_ko": "수입과 재정 상태",
        "icon": "payments",
    },

    # === TIME_DURATION_FREQUENCY (시간과 빈도) ===
    "PERMANENCE_LONGEVITY": {
        "title_ko": "영속성과 장수",
        "icon": "all_inclusive",
    },
    "TRANSIENCE_BREVITY": {
        "title_ko": "일시성과 짧음",
        "icon": "hourglass_empty",
    },
    "FREQUENCY_REPETITION": {
        "title_ko": "빈도와 반복",
        "icon": "repeat",
    },
    "TIMING_SPEED_PUNCTUALITY": {
        "title_ko": "타이밍과 속도",
        "icon": "speed",
    },
    "SEQUENCE_INTERVAL_DURATION": {
        "title_ko": "순서와 간격",
        "icon": "timeline",
    },
    "TIMELINESS_FUTURE_PAST": {
        "title_ko": "적시성과 시제",
        "icon": "schedule",
    },
}


def main():
    client = get_supabase_client()

    print("=" * 60)
    print("데크 테이블 업데이트: title_ko, icon, color")
    print("=" * 60)

    # 1. 카테고리 조회
    cats = client.table(Tables.CATEGORIES).select("id, title").execute()
    cat_map = {c["title"]: c["id"] for c in cats.data}
    cat_id_to_title = {c["id"]: c["title"] for c in cats.data}

    # 2. 데크 조회
    decks = client.table(Tables.DECKS).select("id, title, category_id").execute()

    print(f"\n총 {len(decks.data)}개 데크 업데이트 시작...\n")

    # 카테고리별 색상 인덱스 추적
    cat_color_index = {cat: 0 for cat in CATEGORY_COLORS}

    updated = 0
    errors = []

    for deck in decks.data:
        deck_title = deck["title"]
        cat_title = cat_id_to_title.get(deck["category_id"])

        if deck_title not in DECK_INFO:
            errors.append(f"정보 없음: {deck_title}")
            continue

        if cat_title not in CATEGORY_COLORS:
            errors.append(f"카테고리 색상 없음: {cat_title}")
            continue

        info = DECK_INFO[deck_title]
        colors = CATEGORY_COLORS[cat_title]
        color_idx = cat_color_index[cat_title]
        color = colors[color_idx % len(colors)]
        cat_color_index[cat_title] += 1

        # 업데이트 데이터
        update_data = {
            "title_ko": info["title_ko"],
            "icon": info["icon"],
            "color": color,
        }

        try:
            client.table(Tables.DECKS).update(update_data).eq("id", deck["id"]).execute()
            print(f"  ✓ {deck_title}")
            print(f"    → {info['title_ko']} | {info['icon']} | {color}")
            updated += 1
        except Exception as e:
            errors.append(f"업데이트 실패 {deck_title}: {e}")

    print(f"\n" + "=" * 60)
    print(f"결과: {updated}개 업데이트 완료")

    if errors:
        print(f"\n오류 {len(errors)}개:")
        for e in errors:
            print(f"  ! {e}")

    print("=" * 60)


if __name__ == "__main__":
    main()

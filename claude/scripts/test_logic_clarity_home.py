"""
LOGIC_CLARITY 데크의 'home' 태그 vibe sentence 테스트

실행 방법:
    cd claude
    source venv/bin/activate
    python scripts/test_logic_clarity_home.py
"""

import sys
import os

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.supabase_config import get_supabase_client


def main():
    print("=" * 80)
    print("🧪 LOGIC_CLARITY 데크 - 'home' 태그 테스트")
    print("=" * 80)

    client = get_supabase_client()

    # 1. LOGIC_CLARITY 데크 찾기
    print("\n📌 Step 1: LOGIC_CLARITY 데크 찾기...")

    deck_response = client.table('decks').select('*').or_(
        f"title.eq.LOGIC_CLARITY,title.ilike.%LOGIC_CLARITY%,title_ko.ilike.%논리%"
    ).execute()

    if not deck_response.data:
        print("❌ LOGIC_CLARITY 데크를 찾을 수 없습니다.")
        print("   다른 이름으로 검색해보겠습니다...")

        # 모든 데크 출력해서 찾기
        all_decks = client.table('decks').select('id, title, title_ko').execute()
        print("\n📋 사용 가능한 데크 목록:")
        for deck in all_decks.data:
            print(f"   - {deck.get('title', 'N/A')} / {deck.get('title_ko', 'N/A')} (id: {deck['id']})")
        return

    deck = deck_response.data[0]
    deck_id = deck['id']
    deck_title = deck.get('title', 'Unknown')
    deck_title_ko = deck.get('title_ko', 'Unknown')

    print(f"✅ 데크 발견:")
    print(f"   Title: {deck_title}")
    print(f"   Title (한글): {deck_title_ko}")
    print(f"   ID: {deck_id}")

    # 2. 데크의 카드 개수 확인
    print(f"\n📌 Step 2: {deck_title} 데크의 카드 확인...")

    cards_response = client.table('cards').select('id, front_text').eq('deck_id', deck_id).execute()
    card_count = len(cards_response.data)

    print(f"✅ 총 {card_count}개의 카드 발견")
    if card_count > 0:
        print(f"   예시 카드: {', '.join([c['front_text'] for c in cards_response.data[:5]])}")

    # 3. card_sentences 테이블에 데이터가 있는지 확인
    print(f"\n📌 Step 3: card_sentences 테이블 확인...")

    sentences_response = client.table('card_sentences').select('*').in_(
        'card_id', [c['id'] for c in cards_response.data]
    ).limit(5).execute()

    sentence_count = len(sentences_response.data)
    print(f"✅ {sentence_count}개의 문장 샘플 발견")

    if sentence_count > 0:
        print("   예시 문장:")
        for i, sent in enumerate(sentences_response.data[:3], 1):
            print(f"   {i}. \"{sent.get('sentence_en', 'N/A')}\"")
            print(f"      한글: \"{sent.get('sentence_ko', 'N/A')}\"")
            print(f"      태그: {sent.get('tags', [])}")
    else:
        print("⚠️  이 데크에 card_sentences 데이터가 없습니다.")
        print("   RPC function은 빈 배열을 반환할 것입니다.")

    # 4. get_vibe_sentences_for_deck RPC 호출
    print(f"\n📌 Step 4: get_vibe_sentences_for_deck 호출...")
    print(f"   Deck ID: {deck_id}")
    print(f"   User Tags: ['home']")

    try:
        rpc_response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': ['home']
        }).execute()

        results = rpc_response.data

        print(f"\n✅ RPC 호출 성공!")
        print(f"   반환된 문장 개수: {len(results)}")

        if len(results) > 0:
            print(f"\n📝 'home' 태그가 포함된 문장들:")
            print("=" * 80)

            for i, item in enumerate(results, 1):
                # card 정보 가져오기
                card = next((c for c in cards_response.data if c['id'] == item['card_id']), None)
                card_text = card['front_text'] if card else 'Unknown'

                print(f"\n{i}. Card: {card_text} (ID: {item['card_id']})")
                print(f"   Sentence (EN): {item.get('sentence_en', 'N/A')}")
                print(f"   Sentence (KO): {item.get('sentence_ko', 'N/A')}")
                print(f"   Tags: {item['tags']}")

                # 'home' 태그 확인
                if 'home' in item['tags']:
                    print(f"   ✅ 'home' 태그 포함 확인")
                else:
                    print(f"   ⚠️  'home' 태그가 없음 (버그 가능성)")
        else:
            print("\n⚠️  'home' 태그와 일치하는 문장이 없습니다.")
            print("   가능한 원인:")
            print("   1. card_sentences 테이블에 데이터가 없음")
            print("   2. 'home' 태그를 가진 문장이 이 데크에 없음")

            # 실제로 어떤 태그들이 있는지 확인
            if sentence_count > 0:
                all_tags = set()
                for sent in sentences_response.data:
                    all_tags.update(sent.get('tags', []))
                print(f"\n   이 데크에서 발견된 태그들: {sorted(all_tags)}")

    except Exception as e:
        print(f"\n❌ RPC 호출 실패:")
        print(f"   에러: {str(e)}")
        print("\n   가능한 원인:")
        print("   1. get_vibe_sentences_for_deck function이 DB에 없음")
        print("   2. database/vibe_sentences_rpc.sql을 실행하지 않음")

    print("\n" + "=" * 80)
    print("🏁 테스트 완료")
    print("=" * 80)


if __name__ == '__main__':
    main()

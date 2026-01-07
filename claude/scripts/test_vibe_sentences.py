#!/usr/bin/env python3
"""
get_vibe_sentences_for_deck RPC Function 테스트 스크립트

표준화된 CLI 인터페이스로 특정 데크와 태그 조합을 테스트합니다.

사용 예시:
    python test_vibe_sentences.py --deck LOGIC_CLARITY --tags home office
    python test_vibe_sentences.py -d "Business Communication" -t work professional
    python test_vibe_sentences.py --list-decks  # 사용 가능한 데크 목록
    python test_vibe_sentences.py --list-tags   # 자주 사용되는 태그 목록
"""

import sys
import os
import argparse

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.supabase_config import get_supabase_client


def print_usage():
    """사용법 출력"""
    print("=" * 80)
    print("🧪 Vibe Sentences RPC Function 테스트 도구")
    print("=" * 80)
    print("\n📖 사용법:")
    print("    python test_vibe_sentences.py --deck <DECK_NAME> --tags <TAG1> <TAG2> ...")
    print("\n📌 옵션:")
    print("    -d, --deck <NAME>        데크 이름 (영어, 필수)")
    print("    -t, --tags <TAG> ...     테스트할 태그 리스트 (필수)")
    print("    --list-decks             사용 가능한 모든 데크 목록 출력")
    print("    --list-tags              자주 사용되는 태그 목록 출력")
    print("    -v, --verbose            상세 출력 모드")
    print("    -h, --help               도움말 표시")
    print("\n💡 예시:")
    print("    python test_vibe_sentences.py --deck LOGIC_CLARITY --tags home office")
    print("    python test_vibe_sentences.py -d \"Business Communication\" -t work")
    print("    python test_vibe_sentences.py --list-decks")
    print("\n" + "=" * 80)


def list_all_decks(client):
    """사용 가능한 모든 데크 목록 출력"""
    print("\n📋 사용 가능한 데크 목록:")
    print("=" * 80)

    try:
        response = client.table('decks').select('id, title, title_ko, category_id').order('title', desc=False).execute()

        if not response.data:
            print("⚠️  데크가 없습니다.")
            return

        print(f"\n총 {len(response.data)}개의 데크:")
        print(f"\n{'No.':<5} {'Title (English)':<30} {'Title (Korean)':<30}")
        print("-" * 80)

        for i, deck in enumerate(response.data, 1):
            title = deck.get('title', 'N/A')
            title_ko = deck.get('title_ko', 'N/A')
            print(f"{i:<5} {title:<30} {title_ko:<30}")

        print("\n💡 사용법: --deck \"DECK_TITLE\" 형태로 입력하세요.")

    except Exception as e:
        print(f"❌ 에러: {str(e)}")


def list_common_tags(client):
    """자주 사용되는 태그 목록 출력"""
    print("\n🏷️  자주 사용되는 태그 목록:")
    print("=" * 80)

    try:
        # card_sentences에서 모든 태그 수집
        response = client.table('card_sentences').select('tags').limit(1000).execute()

        if not response.data:
            print("⚠️  태그 데이터가 없습니다.")
            return

        # 태그 빈도수 계산
        tag_counts = {}
        for item in response.data:
            tags = item.get('tags', [])
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # 빈도순 정렬
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)

        print(f"\n{'Tag':<20} {'Count':<10}")
        print("-" * 30)

        for tag, count in sorted_tags[:30]:  # 상위 30개
            print(f"{tag:<20} {count:<10}")

        print(f"\n총 {len(tag_counts)}개의 고유 태그")
        print("\n💡 사용법: --tags TAG1 TAG2 ... 형태로 입력하세요.")

    except Exception as e:
        print(f"❌ 에러: {str(e)}")


def find_deck_by_name(client, deck_name):
    """데크 이름으로 데크 정보 조회"""
    try:
        # 정확한 일치 먼저 시도
        response = client.table('decks').select('*').eq('title', deck_name).execute()

        if response.data:
            return response.data[0]

        # 대소문자 무시 검색
        response = client.table('decks').select('*').ilike('title', deck_name).execute()

        if response.data:
            return response.data[0]

        # 부분 일치 검색
        response = client.table('decks').select('*').ilike('title', f'%{deck_name}%').execute()

        if response.data:
            if len(response.data) > 1:
                print(f"\n⚠️  '{deck_name}'과 일치하는 데크가 {len(response.data)}개 있습니다:")
                for deck in response.data:
                    print(f"   - {deck['title']} ({deck.get('title_ko', 'N/A')})")
                print("\n더 구체적인 이름을 입력해주세요.")
                return None
            return response.data[0]

        return None

    except Exception as e:
        print(f"❌ 데크 조회 중 에러: {str(e)}")
        return None


def test_vibe_sentences(client, deck_name, user_tags, verbose=False):
    """특정 데크와 태그로 vibe sentences 테스트"""
    print("\n" + "=" * 80)
    print("🧪 Vibe Sentences 테스트")
    print("=" * 80)

    # 1. 데크 찾기
    print(f"\n📌 Step 1: '{deck_name}' 데크 검색...")

    deck = find_deck_by_name(client, deck_name)

    if not deck:
        print(f"❌ '{deck_name}' 데크를 찾을 수 없습니다.")
        print("\n💡 사용 가능한 데크 목록을 보려면:")
        print("   python test_vibe_sentences.py --list-decks")
        return

    deck_id = deck['id']
    deck_title = deck.get('title', 'Unknown')
    deck_title_ko = deck.get('title_ko', 'Unknown')

    print(f"✅ 데크 발견:")
    print(f"   Title: {deck_title}")
    print(f"   Title (한글): {deck_title_ko}")
    print(f"   ID: {deck_id}")

    # 2. 데크의 카드 개수 확인 (verbose 모드)
    if verbose:
        print(f"\n📌 Step 2: {deck_title} 데크의 카드 확인...")

        cards_response = client.table('cards').select('id, front_text').eq('deck_id', deck_id).execute()
        card_count = len(cards_response.data)

        print(f"✅ 총 {card_count}개의 카드 발견")
        if card_count > 0:
            print(f"   예시 카드: {', '.join([c['front_text'] for c in cards_response.data[:5]])}")
    else:
        cards_response = client.table('cards').select('id, front_text').eq('deck_id', deck_id).execute()

    # 3. RPC 호출
    print(f"\n📌 Step {'3' if verbose else '2'}: get_vibe_sentences_for_deck 호출...")
    print(f"   Deck: {deck_title}")
    print(f"   Tags: {user_tags}")

    try:
        rpc_response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = rpc_response.data

        print(f"\n✅ RPC 호출 성공!")
        print(f"   반환된 문장 개수: {len(results)}")

        if len(results) > 0:
            print(f"\n📝 태그 {user_tags}와 일치하는 문장들:")
            print("=" * 80)

            for i, item in enumerate(results, 1):
                # card 정보 가져오기
                card = next((c for c in cards_response.data if c['id'] == item['card_id']), None)
                card_text = card['front_text'] if card else 'Unknown'

                print(f"\n{i}. Card: {card_text}")
                if verbose:
                    print(f"   Card ID: {item['card_id']}")
                print(f"   EN: {item.get('sentence_en', 'N/A')}")
                print(f"   KO: {item.get('sentence_ko', 'N/A')}")
                print(f"   Tags: {item['tags']}")

                # 매칭된 태그 확인
                matched_tags = [tag for tag in user_tags if tag in item['tags']]
                if matched_tags:
                    print(f"   ✅ 매칭된 태그: {matched_tags}")
                else:
                    print(f"   ⚠️  매칭된 태그 없음 (버그 가능성)")
        else:
            print(f"\n⚠️  태그 {user_tags}와 일치하는 문장이 없습니다.")
            print("\n💡 가능한 원인:")
            print("   1. 이 데크에 해당 태그를 가진 문장이 없음")
            print("   2. card_sentences 테이블에 데이터가 부족함")
            print("\n   자주 사용되는 태그를 보려면:")
            print("   python test_vibe_sentences.py --list-tags")

    except Exception as e:
        print(f"\n❌ RPC 호출 실패:")
        print(f"   에러: {str(e)}")
        print("\n💡 가능한 원인:")
        print("   1. get_vibe_sentences_for_deck function이 DB에 없음")
        print("   2. database/vibe_sentences_rpc.sql을 실행하지 않음")

    print("\n" + "=" * 80)
    print("🏁 테스트 완료")
    print("=" * 80)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='Vibe Sentences RPC Function 테스트 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python test_vibe_sentences.py --deck LOGIC_CLARITY --tags home office
  python test_vibe_sentences.py -d "Business Communication" -t work
  python test_vibe_sentences.py --list-decks
  python test_vibe_sentences.py --list-tags
        """
    )

    parser.add_argument('-d', '--deck', type=str, help='데크 이름 (영어)')
    parser.add_argument('-t', '--tags', nargs='+', help='테스트할 태그 리스트')
    parser.add_argument('--list-decks', action='store_true', help='사용 가능한 데크 목록 출력')
    parser.add_argument('--list-tags', action='store_true', help='자주 사용되는 태그 목록 출력')
    parser.add_argument('-v', '--verbose', action='store_true', help='상세 출력 모드')

    # 인자가 없으면 사용법 출력
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(0)

    args = parser.parse_args()

    # Supabase 클라이언트 초기화
    try:
        client = get_supabase_client()
    except Exception as e:
        print(f"❌ Supabase 연결 실패: {str(e)}")
        print("\n💡 .env 파일에 SUPABASE_URL과 SUPABASE_KEY가 설정되어 있는지 확인하세요.")
        sys.exit(1)

    # 데크 목록 출력
    if args.list_decks:
        list_all_decks(client)
        return

    # 태그 목록 출력
    if args.list_tags:
        list_common_tags(client)
        return

    # 데크와 태그가 모두 제공되었는지 확인
    if not args.deck or not args.tags:
        print("❌ 에러: --deck과 --tags 옵션이 모두 필요합니다.")
        print("\n사용법을 보려면:")
        print("    python test_vibe_sentences.py")
        sys.exit(1)

    # 테스트 실행
    test_vibe_sentences(client, args.deck, args.tags, args.verbose)


if __name__ == '__main__':
    main()

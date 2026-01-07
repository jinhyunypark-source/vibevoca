"""
get_vibe_sentences_for_deck RPC Function 단위 테스트

테스트 대상:
- Supabase RPC: get_vibe_sentences_for_deck(p_deck_id UUID, p_user_tags TEXT[])
- 기능: 특정 데크의 카드들 중, 사용자 태그와 일치하는 vibe 문장 반환

실행 방법:
    cd claude
    source venv/bin/activate
    pytest scripts/test_get_vibe_sentences_for_deck.py -v
"""

import os
import sys
import uuid
import pytest
from typing import List, Dict

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.supabase_config import get_supabase_client


class TestGetVibeSentencesForDeck:
    """get_vibe_sentences_for_deck RPC 테스트"""

    @pytest.fixture(scope="function")
    def supabase_client(self):
        """Supabase 클라이언트 fixture"""
        return get_supabase_client()

    @pytest.fixture(scope="function")
    def test_data(self, supabase_client):
        """테스트 데이터 생성 및 정리 fixture"""
        client = supabase_client
        test_ids = {
            'category_id': str(uuid.uuid4()),
            'deck_id': str(uuid.uuid4()),
            'card_ids': [str(uuid.uuid4()) for _ in range(3)],
            'sentence_ids': []
        }

        try:
            # 1. 카테고리 생성
            client.table('categories').insert({
                'id': test_ids['category_id'],
                'name': 'Test Category',
                'slug': f'test-cat-{uuid.uuid4().hex[:8]}',
                'description': 'Test category for unit testing'
            }).execute()

            # 2. 데크 생성
            client.table('decks').insert({
                'id': test_ids['deck_id'],
                'category_id': test_ids['category_id'],
                'name': 'Test Deck',
                'slug': f'test-deck-{uuid.uuid4().hex[:8]}',
                'description': 'Test deck for unit testing',
                'order_index': 0
            }).execute()

            # 3. 카드 3개 생성
            cards_data = [
                {
                    'id': test_ids['card_ids'][0],
                    'deck_id': test_ids['deck_id'],
                    'front_text': 'happy',
                    'back_text': '행복한',
                    'order_index': 0
                },
                {
                    'id': test_ids['card_ids'][1],
                    'deck_id': test_ids['deck_id'],
                    'front_text': 'excited',
                    'back_text': '흥분한',
                    'order_index': 1
                },
                {
                    'id': test_ids['card_ids'][2],
                    'deck_id': test_ids['deck_id'],
                    'front_text': 'calm',
                    'back_text': '차분한',
                    'order_index': 2
                }
            ]
            client.table('cards').insert(cards_data).execute()

            # 4. card_sentences 생성 (각 카드에 여러 문장, 다양한 태그)
            sentences_data = [
                # Card 1 (happy): cafe, outdoor 태그
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][0],
                    'sentence': 'I feel happy at this cafe.',
                    'tags': ['cafe', 'positive']
                },
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][0],
                    'sentence': 'Walking in the park makes me happy.',
                    'tags': ['outdoor', 'positive']
                },
                # Card 2 (excited): office, meeting 태그
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][1],
                    'sentence': 'I am excited about the meeting.',
                    'tags': ['office', 'meeting', 'positive']
                },
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][1],
                    'sentence': 'The presentation made me excited.',
                    'tags': ['office', 'work']
                },
                # Card 3 (calm): home, quiet 태그
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][2],
                    'sentence': 'I feel calm at home.',
                    'tags': ['home', 'quiet']
                },
                {
                    'id': str(uuid.uuid4()),
                    'card_id': test_ids['card_ids'][2],
                    'sentence': 'Reading helps me stay calm.',
                    'tags': ['home', 'relaxing']
                },
            ]

            result = client.table('card_sentences').insert(sentences_data).execute()
            test_ids['sentence_ids'] = [item['id'] for item in result.data]

            # 테스트 실행
            yield test_ids

        finally:
            # 정리 (역순으로 삭제)
            print("\n🧹 테스트 데이터 정리 중...")

            # card_sentences 삭제
            if test_ids['sentence_ids']:
                client.table('card_sentences').delete().in_('id', test_ids['sentence_ids']).execute()

            # cards 삭제
            client.table('cards').delete().in_('id', test_ids['card_ids']).execute()

            # deck 삭제
            client.table('decks').delete().eq('id', test_ids['deck_id']).execute()

            # category 삭제
            client.table('categories').delete().eq('id', test_ids['category_id']).execute()

            print("✅ 테스트 데이터 정리 완료")

    def test_function_returns_matching_tags(self, supabase_client, test_data):
        """태그가 일치하는 문장만 반환하는지 테스트"""
        client = supabase_client
        deck_id = test_data['deck_id']

        # cafe 태그로 검색
        user_tags = ['cafe']

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증
        assert len(results) > 0, "결과가 최소 1개 이상이어야 함"

        # 모든 결과가 'cafe' 태그를 포함하는지 확인
        for item in results:
            assert 'cafe' in item['tags'], f"반환된 문장이 'cafe' 태그를 포함해야 함: {item}"
            assert 'card_id' in item, "card_id 필드가 있어야 함"
            assert 'sentence' in item, "sentence 필드가 있어야 함"
            assert 'tags' in item, "tags 필드가 있어야 함"

        print(f"✅ 'cafe' 태그로 {len(results)}개 문장 반환 성공")

    def test_function_with_multiple_tags(self, supabase_client, test_data):
        """여러 태그로 검색 시 OR 조건으로 작동하는지 테스트"""
        client = supabase_client
        deck_id = test_data['deck_id']

        # office OR home 태그로 검색
        user_tags = ['office', 'home']

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증: office 또는 home 태그가 있는 문장들이 반환되어야 함
        assert len(results) > 0, "결과가 최소 1개 이상이어야 함"

        for item in results:
            has_office = 'office' in item['tags']
            has_home = 'home' in item['tags']
            assert has_office or has_home, f"반환된 문장이 'office' 또는 'home' 태그를 포함해야 함: {item}"

        print(f"✅ 'office' OR 'home' 태그로 {len(results)}개 문장 반환 성공")

    def test_function_with_no_matching_tags(self, supabase_client, test_data):
        """일치하는 태그가 없을 때 빈 배열 반환하는지 테스트"""
        client = supabase_client
        deck_id = test_data['deck_id']

        # 존재하지 않는 태그로 검색
        user_tags = ['nonexistent_tag', 'fake_tag']

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증: 결과가 없어야 함
        assert len(results) == 0, "일치하는 태그가 없으므로 빈 배열이어야 함"

        print("✅ 일치하는 태그 없을 때 빈 배열 반환 성공")

    def test_function_with_nonexistent_deck(self, supabase_client, test_data):
        """존재하지 않는 데크 ID로 호출 시 빈 배열 반환하는지 테스트"""
        client = supabase_client

        # 존재하지 않는 deck_id
        nonexistent_deck_id = str(uuid.uuid4())
        user_tags = ['cafe']

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': nonexistent_deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증: 결과가 없어야 함
        assert len(results) == 0, "존재하지 않는 데크이므로 빈 배열이어야 함"

        print("✅ 존재하지 않는 데크 ID로 호출 시 빈 배열 반환 성공")

    def test_function_returns_correct_structure(self, supabase_client, test_data):
        """반환 구조가 올바른지 테스트 (card_id, sentence, tags)"""
        client = supabase_client
        deck_id = test_data['deck_id']

        user_tags = ['positive']  # 여러 카드에 걸쳐 있는 태그

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증
        assert len(results) > 0, "결과가 최소 1개 이상이어야 함"

        for item in results:
            # 필수 필드 존재 확인
            assert 'card_id' in item, "card_id 필드가 있어야 함"
            assert 'sentence' in item, "sentence 필드가 있어야 함"
            assert 'tags' in item, "tags 필드가 있어야 함"

            # 타입 확인
            assert isinstance(item['card_id'], str), "card_id는 문자열(UUID)이어야 함"
            assert isinstance(item['sentence'], str), "sentence는 문자열이어야 함"
            assert isinstance(item['tags'], list), "tags는 배열이어야 함"

            # card_id가 테스트 데이터의 card_ids 중 하나인지 확인
            assert item['card_id'] in test_data['card_ids'], f"반환된 card_id가 테스트 데이터에 속해야 함: {item['card_id']}"

        print(f"✅ 반환 구조 검증 성공: {len(results)}개 문장")

    def test_function_limit_500(self, supabase_client, test_data):
        """LIMIT 500 제한이 작동하는지 테스트 (데이터가 충분하지 않으므로 로직만 확인)"""
        client = supabase_client
        deck_id = test_data['deck_id']

        # 모든 태그 포함
        user_tags = ['cafe', 'outdoor', 'office', 'meeting', 'home', 'quiet', 'positive', 'work', 'relaxing']

        response = client.rpc('get_vibe_sentences_for_deck', {
            'p_deck_id': deck_id,
            'p_user_tags': user_tags
        }).execute()

        results = response.data

        # 검증: 500개 이하여야 함 (실제로는 6개만 있음)
        assert len(results) <= 500, "결과가 500개를 초과하면 안 됨"

        print(f"✅ LIMIT 검증 성공: {len(results)}개 반환 (최대 500)")


def run_tests():
    """테스트 실행 함수"""
    print("=" * 80)
    print("🧪 get_vibe_sentences_for_deck RPC Function 단위 테스트")
    print("=" * 80)

    # pytest 실행
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_tests()

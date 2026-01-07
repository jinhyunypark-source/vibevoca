#!/usr/bin/env python3
"""
AI 기반 단어 컨텐츠 관리 스크립트

사용법:
    python word_manager.py list-decks
    python word_manager.py list-cards <deck_id>
    python word_manager.py add-word <deck_id> --word "단어" --meaning "뜻" --examples "예문1" "예문2"
    python word_manager.py generate-words <deck_id> --count 5
    python word_manager.py generate-example <card_id> --context "cafe,happy,quiet"
"""

import argparse
import json
import sys
import os

# 상위 디렉토리의 config 모듈 import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables


def list_categories():
    """모든 카테고리 목록 조회"""
    client = get_supabase_client()
    response = client.table(Tables.CATEGORIES).select("*").execute()

    print("\n=== 카테고리 목록 ===")
    for cat in response.data:
        print(f"  [{cat['id'][:8]}...] {cat['title']}")
        if cat.get('description'):
            print(f"      └ {cat['description']}")
    return response.data


def list_decks(category_id=None):
    """데크 목록 조회"""
    client = get_supabase_client()
    query = client.table(Tables.DECKS).select("*")

    if category_id:
        query = query.eq("category_id", category_id)

    response = query.order("order_index").execute()

    print("\n=== 데크 목록 ===")
    for deck in response.data:
        title_ko = deck.get('title_ko') or deck['title']
        print(f"  [{deck['id'][:8]}...] {deck['title']} ({title_ko})")
    return response.data


def list_cards(deck_id):
    """특정 데크의 카드 목록 조회"""
    client = get_supabase_client()
    response = client.table(Tables.CARDS).select("*").eq("deck_id", deck_id).execute()

    print(f"\n=== 카드 목록 (데크: {deck_id[:8]}...) ===")
    print(f"총 {len(response.data)}개의 카드\n")

    for card in response.data:
        print(f"  [{card['id'][:8]}...] {card['front_text']}")
        print(f"      └ {card['back_text']}")
        if card.get('example_sentences'):
            for ex in card['example_sentences'][:1]:  # 첫 번째 예문만 표시
                print(f"      └ 예: {ex[:50]}...")
        print()
    return response.data


def add_word(deck_id, word, meaning, examples=None):
    """새 단어 추가"""
    client = get_supabase_client()

    data = {
        "deck_id": deck_id,
        "front_text": word,
        "back_text": meaning,
        "example_sentences": examples or []
    }

    response = client.table(Tables.CARDS).insert(data).execute()

    if response.data:
        print(f"\n✅ 단어 추가 완료: {word}")
        print(f"   ID: {response.data[0]['id']}")
    return response.data


def delete_word(card_id):
    """단어 삭제"""
    client = get_supabase_client()
    response = client.table(Tables.CARDS).delete().eq("id", card_id).execute()

    if response.data:
        print(f"\n✅ 단어 삭제 완료: {card_id}")
    return response.data


def update_word(card_id, word=None, meaning=None, examples=None):
    """단어 수정"""
    client = get_supabase_client()

    data = {}
    if word:
        data["front_text"] = word
    if meaning:
        data["back_text"] = meaning
    if examples is not None:
        data["example_sentences"] = examples

    if not data:
        print("수정할 내용이 없습니다.")
        return None

    response = client.table(Tables.CARDS).update(data).eq("id", card_id).execute()

    if response.data:
        print(f"\n✅ 단어 수정 완료: {card_id}")
    return response.data


def get_deck_info(deck_id):
    """데크 정보 조회"""
    client = get_supabase_client()
    response = client.table(Tables.DECKS).select("*").eq("id", deck_id).single().execute()
    return response.data


def get_card_info(card_id):
    """카드 정보 조회"""
    client = get_supabase_client()
    response = client.table(Tables.CARDS).select("*").eq("id", card_id).single().execute()
    return response.data


def main():
    parser = argparse.ArgumentParser(description="AI 기반 단어 컨텐츠 관리")
    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # list-categories
    subparsers.add_parser("list-categories", help="카테고리 목록 조회")

    # list-decks
    decks_parser = subparsers.add_parser("list-decks", help="데크 목록 조회")
    decks_parser.add_argument("--category", help="카테고리 ID로 필터링")

    # list-cards
    cards_parser = subparsers.add_parser("list-cards", help="카드 목록 조회")
    cards_parser.add_argument("deck_id", help="데크 ID")

    # add-word
    add_parser = subparsers.add_parser("add-word", help="새 단어 추가")
    add_parser.add_argument("deck_id", help="데크 ID")
    add_parser.add_argument("--word", required=True, help="영어 단어")
    add_parser.add_argument("--meaning", required=True, help="한글 뜻")
    add_parser.add_argument("--examples", nargs="*", help="예문들")

    # update-word
    update_parser = subparsers.add_parser("update-word", help="단어 수정")
    update_parser.add_argument("card_id", help="카드 ID")
    update_parser.add_argument("--word", help="새 영어 단어")
    update_parser.add_argument("--meaning", help="새 한글 뜻")
    update_parser.add_argument("--examples", nargs="*", help="새 예문들")

    # delete-word
    delete_parser = subparsers.add_parser("delete-word", help="단어 삭제")
    delete_parser.add_argument("card_id", help="카드 ID")

    # get-deck
    get_deck_parser = subparsers.add_parser("get-deck", help="데크 정보 조회")
    get_deck_parser.add_argument("deck_id", help="데크 ID")

    # get-card
    get_card_parser = subparsers.add_parser("get-card", help="카드 정보 조회")
    get_card_parser.add_argument("card_id", help="카드 ID")

    args = parser.parse_args()

    if args.command == "list-categories":
        list_categories()
    elif args.command == "list-decks":
        list_decks(args.category)
    elif args.command == "list-cards":
        list_cards(args.deck_id)
    elif args.command == "add-word":
        add_word(args.deck_id, args.word, args.meaning, args.examples)
    elif args.command == "update-word":
        update_word(args.card_id, args.word, args.meaning, args.examples)
    elif args.command == "delete-word":
        delete_word(args.card_id)
    elif args.command == "get-deck":
        deck = get_deck_info(args.deck_id)
        print(json.dumps(deck, indent=2, ensure_ascii=False))
    elif args.command == "get-card":
        card = get_card_info(args.card_id)
        print(json.dumps(card, indent=2, ensure_ascii=False))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
영어 단어 추출 프로그램

deck 이름을 입력받아 Supabase의 decks, cards 테이블을 조인하여
해당 덱의 front_text(영어 단어) 리스트를 가져옵니다.

Usage:
    python extract_words_from_deck.py --deck-name "Daily Essentials"
    python extract_words_from_deck.py --deck-name "Business English" --output words.json
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


class WordExtractor:
    def __init__(self):
        self.client = get_supabase_client()

    def get_words_by_deck_name(self, deck_name: str) -> List[Dict]:
        """
        deck 이름으로 단어 목록 추출

        Returns:
            List[Dict]: [
                {
                    "card_id": "uuid",
                    "word": "exhausted",
                    "meaning": "매우 피곤한",
                    "deck_id": "uuid",
                    "deck_name": "Daily Essentials"
                },
                ...
            ]
        """
        try:
            # decks 테이블에서 deck_name으로 deck 찾기
            deck_result = self.client.table('decks').select('id, title').eq('title', deck_name).execute()

            if not deck_result.data:
                print(f"Error: Deck '{deck_name}' not found")
                return []

            deck = deck_result.data[0]
            deck_id = deck['id']

            # cards 테이블에서 해당 deck의 카드들 가져오기
            cards_result = self.client.table('cards').select(
                'id, front_text, back_text, deck_id'
            ).eq('deck_id', deck_id).execute()

            words = []
            for card in cards_result.data:
                words.append({
                    "card_id": card['id'],
                    "word": card['front_text'],
                    "meaning": card['back_text'],
                    "deck_id": deck_id,
                    "deck_name": deck_name
                })

            return words

        except Exception as e:
            print(f"Error extracting words: {e}")
            return []

    def save_to_file(self, words: List[Dict], output_path: str):
        """단어 목록을 JSON 파일로 저장"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(words, f, ensure_ascii=False, indent=2)
            print(f"Saved {len(words)} words to {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def print_summary(self, words: List[Dict]):
        """단어 목록 요약 출력"""
        if not words:
            print("No words found")
            return

        print("\n" + "=" * 60)
        print(f"Deck: {words[0]['deck_name']}")
        print(f"Total words: {len(words)}")
        print("=" * 60)
        print("\nWord list:")
        for i, word in enumerate(words, 1):
            print(f"  {i:2d}. {word['word']:20s} - {word['meaning']}")


def main():
    parser = argparse.ArgumentParser(description="Extract words from a deck by name")
    parser.add_argument("--deck-name", required=True, help="Name of the deck")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()

    extractor = WordExtractor()
    words = extractor.get_words_by_deck_name(args.deck_name)

    if words:
        extractor.print_summary(words)

        if args.output:
            extractor.save_to_file(words, args.output)

        return words
    else:
        print(f"No words found for deck: {args.deck_name}")
        return []


if __name__ == "__main__":
    main()

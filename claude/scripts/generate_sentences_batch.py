#!/usr/bin/env python3
"""
Batch Sentence Generator for Card Words

배치 프로세스로 단어별 예문을 LLM으로 생성하여 DB에 저장.

Usage:
    python generate_sentences_batch.py --word "exhausted"
    python generate_sentences_batch.py --deck-id "uuid"
    python generate_sentences_batch.py --all --limit 100

Output Format (card_sentences 테이블):
    - card_id: 단어 카드 ID
    - word: 영어 단어
    - sentence_en: 영어 예문
    - sentence_ko: 한글 번역
    - tags: ['baseball', 'sports'] (관심사 태그)
    - is_default: True/False
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client

# ============================================
# Interest Categories for Sentence Generation
# ============================================

INTEREST_CATEGORIES = {
    "baseball": {
        "tags": ["baseball", "sports", "mlb", "kbo"],
        "contexts": [
            "야구 경기 중",
            "메이저리그 명장면",
            "한국 프로야구",
            "전설적인 야구선수"
        ],
        "examples": ["Babe Ruth", "Lee Dae-ho", "home run", "pitcher", "World Series"]
    },
    "soccer": {
        "tags": ["soccer", "football", "sports", "premier_league"],
        "contexts": [
            "축구 경기 중",
            "월드컵",
            "프리미어리그"
        ],
        "examples": ["Son Heung-min", "Messi", "goal", "penalty kick"]
    },
    "music": {
        "tags": ["music", "concert", "album", "kpop"],
        "contexts": [
            "콘서트에서",
            "음악 앨범 리뷰",
            "K-pop 아이돌"
        ],
        "examples": ["BTS", "concert", "album", "Grammy"]
    },
    "gaming": {
        "tags": ["gaming", "esports", "video_game"],
        "contexts": [
            "게임 플레이 중",
            "e스포츠 대회",
            "보스전"
        ],
        "examples": ["Faker", "boss fight", "level up", "multiplayer"]
    },
    "cooking": {
        "tags": ["cooking", "food", "recipe", "chef"],
        "contexts": [
            "요리 중",
            "레스토랑에서",
            "요리 프로그램"
        ],
        "examples": ["Gordon Ramsay", "Baek Jong-won", "recipe", "ingredient"]
    },
    "movies": {
        "tags": ["movies", "film", "cinema", "oscar"],
        "contexts": [
            "영화 리뷰",
            "오스카 시상식",
            "감독 인터뷰"
        ],
        "examples": ["Bong Joon-ho", "Oscar", "plot twist", "scene"]
    },
    "technology": {
        "tags": ["technology", "tech", "ai", "startup"],
        "contexts": [
            "기술 발표",
            "AI 개발",
            "스타트업"
        ],
        "examples": ["Elon Musk", "AI", "innovation", "smartphone"]
    },
    "fitness": {
        "tags": ["fitness", "gym", "workout", "health"],
        "contexts": [
            "헬스장에서",
            "운동 후",
            "마라톤"
        ],
        "examples": ["workout", "gym", "muscle", "marathon"]
    },
    "travel": {
        "tags": ["travel", "adventure", "tourism"],
        "contexts": [
            "여행 중",
            "해외에서",
            "배낭여행"
        ],
        "examples": ["destination", "landmark", "culture", "backpacking"]
    },
    "reading": {
        "tags": ["reading", "books", "literature", "novel"],
        "contexts": [
            "독서 중",
            "책 리뷰",
            "작가 인터뷰"
        ],
        "examples": ["novel", "author", "bestseller", "Haruki Murakami"]
    }
}


# ============================================
# LLM Prompt Template
# ============================================

SENTENCE_GENERATION_PROMPT = """
Generate example sentences for the English word "{word}" ({meaning}).

Requirements:
1. Create {count} example sentences
2. Each sentence should naturally use the word "{word}"
3. Context: {context}
4. Keep sentences 10-20 words
5. Make it relatable and memorable

Output JSON format:
{{
    "sentences": [
        {{
            "en": "English sentence here.",
            "ko": "한글 번역/설명"
        }}
    ]
}}

Word: {word}
Meaning: {meaning}
Context: {context}
"""


# ============================================
# Sentence Generator Class
# ============================================

class SentenceGenerator:
    def __init__(self, use_llm: bool = False):
        self.client = get_supabase_client()
        self.use_llm = use_llm

    def get_cards(self, deck_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get cards from database."""
        query = self.client.table('cards').select('id, front_text, back_text, deck_id')

        if deck_id:
            query = query.eq('deck_id', deck_id)

        result = query.limit(limit).execute()
        return result.data

    def generate_default_sentences(self, word: str, meaning: str, count: int = 2) -> List[Dict]:
        """Generate default (general) sentences for a word."""
        # 실제로는 LLM 호출, 여기서는 템플릿 기반 예시
        templates = [
            {
                "en": f"The situation was quite {word}.",
                "ko": f"상황이 꽤 {meaning}."
            },
            {
                "en": f"I felt {word} about the whole experience.",
                "ko": f"전체 경험에 대해 {meaning} 느꼈다."
            },
            {
                "en": f"It was a {word} moment for everyone involved.",
                "ko": f"관련된 모든 사람들에게 {meaning} 순간이었다."
            }
        ]
        return templates[:count]

    def generate_interest_sentences(
        self,
        word: str,
        meaning: str,
        interest: str,
        count: int = 2
    ) -> List[Dict]:
        """Generate interest-specific sentences for a word."""
        if interest not in INTEREST_CATEGORIES:
            return []

        category = INTEREST_CATEGORIES[interest]

        # 실제로는 LLM 호출, 여기서는 예시 템플릿
        # TODO: OpenAI/Claude API 연동
        example_sentences = {
            "baseball": [
                {
                    "en": f"The pitcher's fastball was {word} in the ninth inning.",
                    "ko": f"9회 투수의 패스트볼은 {meaning}."
                },
                {
                    "en": f"Babe Ruth's legendary career was simply {word}.",
                    "ko": f"베이브 루스의 전설적인 커리어는 정말 {meaning}."
                }
            ],
            "soccer": [
                {
                    "en": f"Son Heung-min's goal was {word} under pressure.",
                    "ko": f"압박 속에서 손흥민의 골은 {meaning}."
                },
                {
                    "en": f"The World Cup final atmosphere was {word}.",
                    "ko": f"월드컵 결승 분위기는 {meaning}."
                }
            ],
            "music": [
                {
                    "en": f"BTS's new album was {word} according to critics.",
                    "ko": f"비평가들에 따르면 BTS의 새 앨범은 {meaning}."
                },
                {
                    "en": f"The concert's encore was {word} and emotional.",
                    "ko": f"콘서트 앵콜은 {meaning}고 감동적이었다."
                }
            ],
            "gaming": [
                {
                    "en": f"Faker's gameplay in the finals was {word}.",
                    "ko": f"결승전에서 페이커의 플레이는 {meaning}."
                },
                {
                    "en": f"The boss fight was {word} but rewarding.",
                    "ko": f"보스전은 {meaning}지만 보람찼다."
                }
            ],
            "cooking": [
                {
                    "en": f"Gordon Ramsay called the dish {word}.",
                    "ko": f"고든 램지는 그 요리를 {meaning}고 평가했다."
                },
                {
                    "en": f"Baek Jong-won's recipe was surprisingly {word}.",
                    "ko": f"백종원의 레시피는 의외로 {meaning}."
                }
            ],
            "movies": [
                {
                    "en": f"Bong Joon-ho's Oscar speech was {word}.",
                    "ko": f"봉준호 감독의 오스카 수상 소감은 {meaning}."
                },
                {
                    "en": f"The plot twist was {word} and unexpected.",
                    "ko": f"반전은 {meaning}고 예상치 못했다."
                }
            ],
            "technology": [
                {
                    "en": f"The AI's response was surprisingly {word}.",
                    "ko": f"AI의 응답은 놀랍게도 {meaning}."
                },
                {
                    "en": f"Elon Musk's announcement was {word}.",
                    "ko": f"일론 머스크의 발표는 {meaning}."
                }
            ]
        }

        return example_sentences.get(interest, [])[:count]

    def save_sentences(
        self,
        card_id: str,
        word: str,
        sentences: List[Dict],
        tags: List[str],
        is_default: bool
    ) -> int:
        """Save generated sentences to database."""
        saved_count = 0

        for sentence in sentences:
            try:
                self.client.table('card_sentences').insert({
                    "card_id": card_id,
                    "word": word,
                    "sentence_en": sentence["en"],
                    "sentence_ko": sentence["ko"],
                    "tags": tags,
                    "is_default": is_default,
                    "is_verified": False,  # 검수 전
                    "source": "llm"
                }).execute()
                saved_count += 1
            except Exception as e:
                print(f"  ! Error saving sentence: {e}")

        return saved_count

    def process_card(self, card: Dict, interests: List[str] = None) -> int:
        """Process a single card and generate sentences."""
        card_id = card['id']
        word = card['front_text']
        meaning = card['back_text']

        print(f"\nProcessing: {word} ({meaning})")
        total_saved = 0

        # 1. Generate default sentences
        default_sentences = self.generate_default_sentences(word, meaning, count=2)
        saved = self.save_sentences(card_id, word, default_sentences, [], is_default=True)
        print(f"  + Default sentences: {saved}")
        total_saved += saved

        # 2. Generate interest-based sentences
        interests_to_use = interests or list(INTEREST_CATEGORIES.keys())

        for interest in interests_to_use:
            if interest in INTEREST_CATEGORIES:
                tags = INTEREST_CATEGORIES[interest]["tags"]
                interest_sentences = self.generate_interest_sentences(word, meaning, interest, count=2)

                if interest_sentences:
                    saved = self.save_sentences(card_id, word, interest_sentences, tags, is_default=False)
                    print(f"  + {interest} sentences: {saved}")
                    total_saved += saved

        return total_saved

    def run_batch(
        self,
        deck_id: Optional[str] = None,
        limit: int = 100,
        interests: List[str] = None
    ):
        """Run batch processing for multiple cards."""
        print("=" * 60)
        print("Batch Sentence Generation")
        print("=" * 60)

        cards = self.get_cards(deck_id=deck_id, limit=limit)
        print(f"\nFound {len(cards)} cards to process")

        total_sentences = 0
        for i, card in enumerate(cards, 1):
            print(f"\n[{i}/{len(cards)}]", end="")
            total_sentences += self.process_card(card, interests)

        print("\n" + "=" * 60)
        print(f"Total sentences generated: {total_sentences}")
        print("=" * 60)


# ============================================
# CLI
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Generate example sentences for vocabulary cards")
    parser.add_argument("--word", help="Generate for a specific word")
    parser.add_argument("--deck-id", help="Generate for all cards in a deck")
    parser.add_argument("--all", action="store_true", help="Generate for all cards")
    parser.add_argument("--limit", type=int, default=100, help="Limit number of cards")
    parser.add_argument("--interests", nargs="+", help="Specific interests to generate for")
    parser.add_argument("--list-interests", action="store_true", help="List available interests")

    args = parser.parse_args()

    if args.list_interests:
        print("\nAvailable interest categories:")
        for interest, data in INTEREST_CATEGORIES.items():
            print(f"  - {interest}: {data['tags']}")
        return

    generator = SentenceGenerator()

    if args.word:
        # Find card by word
        result = generator.client.table('cards').select('*').eq('front_text', args.word).limit(1).execute()
        if result.data:
            generator.process_card(result.data[0], args.interests)
        else:
            print(f"Word not found: {args.word}")

    elif args.deck_id:
        generator.run_batch(deck_id=args.deck_id, limit=args.limit, interests=args.interests)

    elif args.all:
        generator.run_batch(limit=args.limit, interests=args.interests)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

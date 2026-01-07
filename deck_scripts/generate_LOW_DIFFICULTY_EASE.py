#!/usr/bin/env python3
"""
예문 생성 스크립트: LOW_DIFFICULTY_EASE

이 스크립트는 'LOW_DIFFICULTY_EASE' 덱의 단어들에 대해
자연스러운 예문을 생성합니다.

생성된 예문은 검토 후 DB에 업로드할 수 있습니다.
"""

import sys
import os
import json
from typing import List, Dict
from anthropic import Anthropic

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


DECK_INFO = {
    "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
    "deck_title": "LOW_DIFFICULTY_EASE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "1ff3e2e5-cd23-41bc-9658-0089cb447034",
        "word": "Easy",
        "meaning": "쉬운 (어렵지 않은, 일반적)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "4c87d220-5242-4bcd-9b27-c89ce0aee716",
        "word": "Facile",
        "meaning": "술술 풀리는, 손쉬운 (너무 쉬워서 깊이가 없는/경솔한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "d7850515-390b-4d71-83e5-c436de814749",
        "word": "Cinch",
        "meaning": "아주 쉬운 일 (식은 죽 먹기)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "a68c7c44-21a7-42a8-96b8-80f48ec4964e",
        "word": "Simple",
        "meaning": "간단한 (복잡하지 않고 단순한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "150e4791-9fce-4fb7-8e4b-35d1f3e2ec24",
        "word": "Effortless",
        "meaning": "노력이 필요 없는 (너무 쉬워서 힘이 안 드는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "25de00bd-2c70-4bfd-921b-fb5fdf29d26d",
        "word": "Smooth",
        "meaning": "순조로운 (장애물 없이 매끄러운)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "b7b316a4-fdc1-4e04-8dde-306f3cffd487",
        "word": "Painless",
        "meaning": "고통 없는, 수월한 (힘들지 않게 처리된)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "b3e8df0a-b230-4afe-93b4-8a4e6889eb68",
        "word": "Manageable",
        "meaning": "감당할 수 있는 (다루기 쉬운)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "6664e068-ab0f-4f28-b0d3-354f2b55cc4b",
        "word": "Doable",
        "meaning": "할 만한 (실행 가능한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "8cb4b39e-0409-4dfb-9395-044398fda4b1",
        "word": "Breezy",
        "meaning": "경쾌한, 식은 죽 먹기인 (바람 불듯 시원하고 쉬운)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "99e4dab8-3214-47b4-a589-1bef03125ae3",
        "word": "Light",
        "meaning": "가벼운 (부담 없는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "8e0942ef-ab7f-40bf-a841-9143883fc685",
        "word": "Undemanding",
        "meaning": "요구가 적은, 편한 (노력이 별로 안 드는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "447c59a0-1b55-46ee-a6ee-f16f42c05514",
        "word": "Straightforward",
        "meaning": "수월한, 간단한 (복잡한 것 없이 바로 이해되는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "fd497690-4d90-4a93-8d1c-8ffbbd2df390",
        "word": "User-friendly",
        "meaning": "사용하기 쉬운 (사용자 친화적인)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "c4febb6a-7edf-4525-b813-8467184261a3",
        "word": "Snap",
        "meaning": "쉬운 일 (손가락 튕기듯 쉬운)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "d3a6be30-78a2-4189-aae8-a2bacaf873a8",
        "word": "Walk in the park",
        "meaning": "아주 쉬운 일 (산책하듯 편한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "09b99b8f-9d7e-4175-9687-b7c0aab10721",
        "word": "Accessible",
        "meaning": "접근하기 쉬운, 이해하기 쉬운 (진입 장벽이 낮은)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "eb0d513d-06a4-4b1b-8423-920bf79592aa",
        "word": "Elementary",
        "meaning": "초보적인, 기초적인 (아주 쉬운)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "57e37378-8371-4598-a6e0-ce185cf88a8e",
        "word": "Basic",
        "meaning": "기본적인 (가장 밑바닥의 쉬운 수준)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "1be14ae1-03b0-4ea5-974e-e6a7e732a74b",
        "word": "Introductory",
        "meaning": "입문의 (초보자를 위한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "40d4be44-e44c-4f98-bd46-d4eb7d20a9c7",
        "word": "Child's play",
        "meaning": "아이들 장난 같은 (매우 쉬운 일)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "d5303fe9-e742-4a3f-8746-f4c58864b3eb",
        "word": "Piece of cake",
        "meaning": "누워서 떡 먹기 (매우 쉬운 일)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "c8e876e7-7611-4380-b937-bae5f284162b",
        "word": "No-brainer",
        "meaning": "고민할 필요도 없는 쉬운 결정",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "222589ea-cf2f-4410-bfba-d72b0bbd2ebd",
        "word": "Instinctive",
        "meaning": "본능적인 (배우지 않아도 저절로 되는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "b34c3cd5-d834-4c41-b1a0-97b2ad54edc7",
        "word": "Automatic",
        "meaning": "자동적인 (생각 없이도 되는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "b0ab1631-9b22-477d-8836-e366e0a3bfb8",
        "word": "Intuitive",
        "meaning": "직관적인 (설명서 없이도 알 수 있는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "42fc876e-aaea-4af6-8acb-0595b7ebaa82",
        "word": "Seamless",
        "meaning": "매끄러운 (끊김이나 어려움이 없는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "48bcca7f-9235-494a-9c12-aaf8de4fefcb",
        "word": "Uncomplicated",
        "meaning": "복잡하지 않은 (단순한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "4fb533d4-9c8f-4137-99f1-df7ccb60ed45",
        "word": "Trouble-free",
        "meaning": "문제가 없는 (말썽 없이 잘 되는)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    },
    {
        "card_id": "b93842b1-310c-4774-b69c-9596904ba834",
        "word": "Convenient",
        "meaning": "편리한 (쓰기 쉽고 편한)",
        "deck_id": "8ee701c5-f189-4d1f-b0d6-d262b8b2241a",
        "deck_title": "LOW_DIFFICULTY_EASE"
    }
]

RELEVANT_TAGS = [
    "style",
    "planning",
    "education",
    "soccer",
    "place",
    "outdoor",
    "environment",
    "school",
    "shopping",
    "movie"
]


class SentenceGenerator:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.client = get_supabase_client()

    def generate_prompt(self, word: str, meaning: str) -> str:
        """예문 생성을 위한 프롬프트"""

        prompt = f"""당신은 영어 학습 예문을 생성하는 전문가입니다.

주어진 영어 단어에 대해 학습자가 쉽게 이해하고 기억할 수 있는 자연스러운 예문을 만들어주세요.

**단어**: {word}
**의미**: {meaning}

**추천 태그**: {', '.join(RELEVANT_TAGS)}
- 위 태그들은 'LOW_DIFFICULTY_EASE' 덱과 관련이 깊은 주제들입니다
- 각 예문에 자연스럽게 어울리는 태그 5개 내외를 선택해주세요
- 모든 태그를 억지로 사용하지 마세요

**요구사항**:
1. 총 5-8개의 예문을 생성해주세요
2. 각 예문은 10-20단어 정도의 자연스러운 문장이어야 합니다
3. 단어 '{word}'가 자연스럽게 사용되어야 합니다
4. 다양한 맥락과 상황을 다루어주세요
5. 실생활에서 사용 가능한 자연스러운 문장이어야 합니다
6. **한국어 번역은 자연스러운 한국어로 작성해주세요** (직역이 아닌 의역)

**출력 형식** (JSON):
{{
  "sentences": [
    {{
      "word": "{word}",
      "sentence_en": "영어 예문",
      "sentence_ko": "자연스러운 한국어 번역",
      "tags": ["선택된", "태그", "5개", "내외"]
    }}
  ]
}}

반드시 위의 JSON 형식으로만 응답해주세요."""

        return prompt

    def call_claude_api(self, prompt: str) -> Dict:
        """Claude API 호출"""
        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            content = response.content[0].text

            # JSON 추출
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            return json.loads(json_str)

        except Exception as e:
            print(f"  ! Error calling API: {e}")
            return {"sentences": []}

    def generate_all_sentences(self) -> List[Dict]:
        """모든 단어에 대해 예문 생성"""

        print("=" * 70)
        print(f"예문 생성: {DECK_INFO['deck_title']}")
        print("=" * 70)
        print(f"총 단어 수: {DECK_INFO['total_words']}")
        print(f"추천 태그: {', '.join(RELEVANT_TAGS)}")
        print("=" * 70)

        all_sentences = []

        for i, word_data in enumerate(WORDS, 1):
            print(f"\n[{i}/{len(WORDS)}] {word_data['word']} ({word_data['meaning']})")

            prompt = self.generate_prompt(word_data['word'], word_data['meaning'])
            result = self.call_claude_api(prompt)

            sentences = result.get('sentences', [])

            # card_id와 deck_title 추가
            for sentence in sentences:
                sentence['card_id'] = word_data['card_id']
                sentence['deck_title'] = DECK_INFO['deck_title']

            all_sentences.extend(sentences)
            print(f"  ✓ {len(sentences)}개 예문 생성됨")

        return all_sentences

    def save_results(self, sentences: List[Dict], output_file: str):
        """결과를 JSON 파일로 저장"""

        output_data = {
            "deck_info": DECK_INFO,
            "total_sentences": len(sentences),
            "sentences": sentences
        }

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 결과 저장: {output_file}")
        print(f"  총 {len(sentences)}개 예문 생성")

    def print_summary(self, sentences: List[Dict]):
        """생성된 예문 요약 출력"""

        print("\n" + "=" * 70)
        print("생성 결과 미리보기")
        print("=" * 70)

        # 처음 3개 예문만 출력
        for i, sentence in enumerate(sentences[:3], 1):
            print(f"\n[예문 {i}]")
            print(f"  단어: {sentence['word']}")
            print(f"  영문: {sentence['sentence_en']}")
            print(f"  한글: {sentence['sentence_ko']}")
            print(f"  태그: {', '.join(sentence['tags'])}")

        if len(sentences) > 3:
            print(f"\n... 외 {len(sentences) - 3}개 예문")


def main():
    generator = SentenceGenerator()

    # 예문 생성
    sentences = generator.generate_all_sentences()

    # 결과 저장
    output_file = f"output/sentences/{DECK_INFO['deck_title'].replace('/', '_')}.json"
    generator.save_results(sentences, output_file)

    # 요약 출력
    generator.print_summary(sentences)

    print("\n" + "=" * 70)
    print("✓ 완료!")
    print("  검토 후 upload_sentences_to_db.py를 사용해서 DB에 업로드하세요.")
    print("=" * 70)


if __name__ == "__main__":
    main()

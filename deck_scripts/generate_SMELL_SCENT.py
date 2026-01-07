#!/usr/bin/env python3
"""
예문 생성 스크립트: SMELL_SCENT

이 스크립트는 'SMELL_SCENT' 덱의 단어들에 대해
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
    "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
    "deck_title": "SMELL_SCENT",
    "total_words": 21
}

WORDS = [
    {
        "card_id": "0e101dc2-2bfc-4623-af6d-6de9d737ff7f",
        "word": "Fragrant",
        "meaning": "향기로운 >  fragile(깨지기쉬운, 향기가 사라지기쉬운)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "5c86045c-2bf0-40b3-ba76-7320092475a4",
        "word": "Redolent",
        "meaning": "~향이 감도는/생각나게 하는   odor (냄새) (라)olere향기나다",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "b1fccf05-ac96-4d13-a001-cf85e95a9aa6",
        "word": "Aromatic",
        "meaning": "향이 좋은 (음식/허브)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "ee9fd469-575c-4d9f-bccb-87d7fb9fb6cf",
        "word": "Scented",
        "meaning": "향이 나는 (인공/자연)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "f4ea32d9-cb10-4de4-ad8e-c6b05e1424fe",
        "word": "Perfumed",
        "meaning": "향수를 뿌린",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "4913bbca-43d6-4c57-a64e-afb094d2ce4f",
        "word": "Floral",
        "meaning": "꽃향기의",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "d385ef0a-3439-42be-bc3c-b16bd0d43ba3",
        "word": "Fresh",
        "meaning": "신선한, 상쾌한",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "8aa469f9-692c-4f5a-81ca-0b4ad6863c38",
        "word": "Earthy",
        "meaning": "흙냄새 나는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "c131c89e-877c-4d86-b097-a19405c28615",
        "word": "Musky",
        "meaning": "사향 냄새가 나는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "98899bfa-9fbb-4e71-a988-d959966c600c",
        "word": "Smoky",
        "meaning": "연기 냄새가 나는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "9281d4ee-ea3e-424f-97e9-c6311c90b394",
        "word": "Stinking",
        "meaning": "악취가 진동하는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "048fda6f-8c4e-4a11-b663-34b4e5b1a483",
        "word": "Foul",
        "meaning": "더러운, 고약한",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "9fbf32a6-954a-44fa-9894-947c25165cbc",
        "word": "Fetid",
        "meaning": "극도로 악취가 나는 (부패)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "4f68fdf8-11b7-45d5-9240-489f394acf0c",
        "word": "Musty",
        "meaning": "곰팡내 나는, 퀴퀴한",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "311cb003-fb7c-4905-ad8e-b348168044f7",
        "word": "Rancid",
        "meaning": "쩐내가 나는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "84d65dcc-6eac-47a5-b5d9-af7cdb521b15",
        "word": "Pungent",
        "meaning": "코를 찌르는",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "5c5c0f2d-ccdb-4664-9c13-768f29da3f01",
        "word": "Acrid",
        "meaning": "매캐한",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "bf5a10d7-7455-4143-bf9d-a114674ab733",
        "word": "Malodorous",
        "meaning": "악취가 나는 (격식)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "5524545d-584d-4776-8914-986676f3d42e",
        "word": "Noxious",
        "meaning": "유독한, 유해한",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "d724cb1d-ab15-449c-84c0-ff5345e7c14e",
        "word": "Overpowering",
        "meaning": "압도적인 (너무 강한)",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    },
    {
        "card_id": "03aafbaf-7a4d-418a-a290-c38e8bb8b693",
        "word": "Stale",
        "meaning": "케케묵은, 신선하지 않은",
        "deck_id": "97336a6a-a995-40c3-8fbb-03c3ab1c2318",
        "deck_title": "SMELL_SCENT"
    }
]

RELEVANT_TAGS = [
    "education",
    "entrepreneur",
    "marketing",
    "work",
    "food",
    "planning",
    "family",
    "study",
    "ai",
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
- 위 태그들은 'SMELL_SCENT' 덱과 관련이 깊은 주제들입니다
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

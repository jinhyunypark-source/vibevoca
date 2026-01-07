#!/usr/bin/env python3
"""
예문 생성 스크립트: AESTHETIC_SENSE

이 스크립트는 'AESTHETIC_SENSE' 덱의 단어들에 대해
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
    "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
    "deck_title": "AESTHETIC_SENSE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "19841029-1883-4aa5-a4f2-83a4a7904f0e",
        "word": "Exquisite",
        "meaning": "매우 아름다운 (정교함)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "c5b1e01f-f4da-47db-ad91-1fb8cb1a19aa",
        "word": "Opulent",
        "meaning": "호화로운 (부유함)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "01590c34-f005-4cab-ba7a-e8356a3deff8",
        "word": "Sophisticated",
        "meaning": "세련된, 교양 있는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "ea115463-8246-40b0-9eb7-9c0d9f059955",
        "word": "Resplendent",
        "meaning": "눈부시게 빛나는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "e871da84-77c9-4814-b69f-d02a4a6e4785",
        "word": "Ethereal",
        "meaning": "천상적인, 가냘픈",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "284bfd6c-7a7a-4122-88c0-a37a3d9fe48a",
        "word": "Classy",
        "meaning": "격조 높은",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "510294ac-9fc7-4b33-a321-403a2370ed37",
        "word": "Alluring",
        "meaning": "매혹적인 (유혹하는)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "add8d957-8054-4836-97f6-76dc456409de",
        "word": "Gaudy",
        "meaning": "야한 (부정적)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "087143e2-3fb9-44a0-a186-84b44fba58ef",
        "word": "Tacky",
        "meaning": "촌스러운 (싸구려)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "087e6879-9a79-453f-bf28-b33752fc9612",
        "word": "Kitsch",
        "meaning": "키치한 (저속한 예술)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "9cfbe282-36bf-44cd-978f-81f0d3c3d4fa",
        "word": "Garish",
        "meaning": "(색이) 요란한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "94ab2f57-c44b-49b7-b4e9-9021cef99485",
        "word": "Dowdy",
        "meaning": "볼품없는 (옷차림)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "b1263c09-7cf0-45f2-adb7-b249b49c2b50",
        "word": "Frumpy",
        "meaning": "지저분하고 유행 지난",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "93b0959b-9e27-405f-9dfb-2daf46f97762",
        "word": "Drab",
        "meaning": "칙칙한, 생기 없는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "767b8cb3-71ac-48d8-b9ee-3309fc2db2be",
        "word": "Timeless",
        "meaning": "유행을 타지 않는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "e426b027-f20b-486d-ad79-e9925baa8f0b",
        "word": "Graceful",
        "meaning": "우아한 (움직임/선)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "c19db3d3-7292-4506-a996-0d2c223d1d17",
        "word": "Elegant",
        "meaning": "우아한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "c2601b1d-c61f-43bc-a930-197fee6bf38c",
        "word": "Sublime",
        "meaning": "숭고한 (경외감)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "a09997e5-1911-4c9b-8ace-a0114b56b8cc",
        "word": "Majestic",
        "meaning": "장엄한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "5e668c65-1e01-4b5b-b343-5e2682eddfdb",
        "word": "Ostentatious",
        "meaning": "대놓고 과시하는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "567cae1a-398d-4b42-a54e-30bd3c0635ff",
        "word": "Mundane",
        "meaning": "평범한, 재미없는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "bab073f6-1173-4e0e-a39a-7ce8eaf9c195",
        "word": "Tasteful",
        "meaning": "고상한, 센스 있는",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "3b7ad0e2-0a5c-45e4-94ad-5ba30c9be432",
        "word": "Loud",
        "meaning": "(무늬가) 요란한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "46baca49-08ca-41bc-8462-9a91891eeb4b",
        "word": "Grotesque",
        "meaning": "기괴한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "90907eae-a955-40a3-b2f7-61ae0b5185cf",
        "word": "Hideous",
        "meaning": "흉측한, 끔찍한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "d7dcffed-470b-4c25-9565-c547457eb6a9",
        "word": "Iconic",
        "meaning": "상징적인",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "17f5ea08-ac12-4725-8fb1-c93fdee17178",
        "word": "Stunning",
        "meaning": "기절할 만큼 멋진",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "500eb93a-0de6-4220-b28c-d95c9415d9b8",
        "word": "Radiant",
        "meaning": "빛나는 (행복/아름다움)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "cbec6a8f-d8be-4ef6-b802-7f31787b168b",
        "word": "Refined",
        "meaning": "정제된, 고상한",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    },
    {
        "card_id": "e3d1e013-30de-4683-b0e5-ec6840b5582e",
        "word": "Charming",
        "meaning": "매력적인 (아기자기함)",
        "deck_id": "a684d2c4-a9a4-4e13-a081-a2b62d3c218e",
        "deck_title": "AESTHETIC_SENSE"
    }
]

RELEVANT_TAGS = [
    "exercise",
    "career",
    "time",
    "education",
    "family",
    "business",
    "wellness",
    "job",
    "vacation",
    "marketing"
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
- 위 태그들은 'AESTHETIC_SENSE' 덱과 관련이 깊은 주제들입니다
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

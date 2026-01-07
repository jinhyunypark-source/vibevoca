#!/usr/bin/env python3
"""
예문 생성 스크립트: LUXURY_EXTRAVAGANCE

이 스크립트는 'LUXURY_EXTRAVAGANCE' 덱의 단어들에 대해
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
    "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
    "deck_title": "LUXURY_EXTRAVAGANCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "25b62218-a56a-47aa-afd5-29cef39cb781",
        "word": "Extravagant",
        "meaning": "사치스러운, 낭비하는 (분수에 넘치게 쓰는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "9062281d-4e7c-4342-ac7a-1eea45935aa1",
        "word": "Lavish",
        "meaning": "호화로운, 아끼지 않는 (풍성하게 쏟아붓는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "db00d201-e620-4453-bcdd-117febb5f18f",
        "word": "Luxurious",
        "meaning": "고급스러운, 사치스러운 (편안하고 비싼)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "ab7c8d40-50a6-4e51-b533-882bb517c072",
        "word": "Sumptuous",
        "meaning": "비싸고 화려한 (보기에도 훌륭한)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "bdcb70f8-fb5e-4c40-ae9b-9000187f88ff",
        "word": "Costly",
        "meaning": "비싼, 대가가 큰 (비용이 많이 드는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "36dde633-15bb-428c-8e1d-891be98df484",
        "word": "Exorbitant",
        "meaning": "터무니없이 비싼 (상식을 벗어난 가격)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "c8677252-da3e-4d90-bbe9-ab7bbcf94215",
        "word": "Expensive",
        "meaning": "비싼 (가격이 높은)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "56e5440e-f450-40ad-857f-2742f1ace8af",
        "word": "Splurging",
        "meaning": "돈을 펑펑 쓰는 (기분 내서 쓰는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "7342906a-26bb-4864-b531-2620caa9caa2",
        "word": "Dear",
        "meaning": "비싼 (영국식 격식: 가격이 높은)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "127cbb07-24d3-45af-8462-58fc214d3e1c",
        "word": "Pricey",
        "meaning": "값비싼 (구어체: 꽤 비싼)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "22703987-3834-483c-99f8-3b424e5b122d",
        "word": "Prodigal",
        "meaning": "낭비하는, 방탕한 (돈을 흥청망청 쓰는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "d04928de-4760-4a90-993d-e4f02e8f499e",
        "word": "Steep",
        "meaning": "(가격이) 비싼 (너무 높게 책정된)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "d82c30f3-94b8-4de0-870a-3343aead3999",
        "word": "Wasteful",
        "meaning": "낭비하는 (쓸데없이 버리는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "afee1ac2-8ee2-4a57-ad12-b0c7b8d5046f",
        "word": "Spendthrift",
        "meaning": "돈을 헤프게 쓰는 사람 (낭비벽이 있는 사람)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "e6517c17-fba9-42d4-a804-eac22648b719",
        "word": "Immoderate",
        "meaning": "무절제한 (과도한)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "d1360a11-ddf0-4897-a511-d082964c30d8",
        "word": "Indulgent",
        "meaning": "탐닉하는, 사치 부리는 (욕망을 채우는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "28bb4b8c-480b-46b6-8917-13d548102b7c",
        "word": "Excessive",
        "meaning": "과도한 (지나친)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "f330b9ae-cdc4-4bad-9b8d-78b1086f6927",
        "word": "Fancy",
        "meaning": "고급의, 화려한 (비싸고 장식적인)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "9779a062-518c-4550-9811-a6ea575a461c",
        "word": "High-end",
        "meaning": "고급의, 고가의 (상위 모델의)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "24200ec1-da4d-42f8-85c0-c093b0024f69",
        "word": "Premium",
        "meaning": "프리미엄, 고급의 (웃돈을 주는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "064fdf81-caee-4a33-be99-0246f7ccf241",
        "word": "Deluxe",
        "meaning": "호화로운, 특급의 (고급스러운)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "c15de269-d25e-4be1-84c8-2a31d579a43a",
        "word": "Exclusive",
        "meaning": "독점적인, 고급의 (아무나 못 들어가는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "7b6f424b-1929-4943-997b-bcf2ba13c609",
        "word": "Posh",
        "meaning": "상류층의, 우아한 (영국식: 고급스러운)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "7e1cf07b-7825-46b9-8ee5-7475efffebc4",
        "word": "Upscale",
        "meaning": "부유층을 겨냥한 (상류층의)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "bf36f972-6ac8-4c36-a85c-f43b2e2a54a9",
        "word": "Flashy",
        "meaning": "호화찬란한, 튀는 (돈 자랑하는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "854e1048-14ff-4371-a78a-a583a47d3683",
        "word": "Ostentatious",
        "meaning": "대놓고 과시하는 (거들먹거리는 사치)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "017b1775-a88b-4f7b-bb64-2ea545887875",
        "word": "Showy",
        "meaning": "화려한, 허세 부리는 (보여주기 위한)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "a8d80221-4398-4684-bdb0-5476a27ce72c",
        "word": "Squandering",
        "meaning": "탕진하는 (함부로 써버리는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "ed354ec2-f0bb-476f-8438-a8ab2463abea",
        "word": "Burning (money)",
        "meaning": "돈을 태우는 (낭비하는)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    },
    {
        "card_id": "206fb400-f55e-4105-98d6-9fef0530e8ca",
        "word": "Overpriced",
        "meaning": "너무 비싼 (가치보다 비싼)",
        "deck_id": "fbeba55c-ee74-49bd-af86-29a2a1f8e4b1",
        "deck_title": "LUXURY_EXTRAVAGANCE"
    }
]

RELEVANT_TAGS = [
    "health",
    "restaurant",
    "hot",
    "journey",
    "vacation",
    "work",
    "digital",
    "communication",
    "outdoor",
    "sad"
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
- 위 태그들은 'LUXURY_EXTRAVAGANCE' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: COST_PRICE_VALUE

이 스크립트는 'COST_PRICE_VALUE' 덱의 단어들에 대해
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
    "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
    "deck_title": "COST_PRICE_VALUE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "dd5fb871-818f-45c6-9e68-2382737d3d4c",
        "word": "Cost",
        "meaning": "비용, 원가 (지불해야 하는 돈)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "ebbe3882-d3bc-4b0c-ad48-f94ed051ea12",
        "word": "Price",
        "meaning": "가격 (판매가)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "6d15a3e9-5d40-4e70-9f47-7770a4a15078",
        "word": "Value",
        "meaning": "가치 (유용성이나 중요성)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "9d40283a-2eb5-470f-823b-24674942dd98",
        "word": "Worth",
        "meaning": "~의 가치가 있는 (금전적/실질적 가치)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "64dd0b2b-c37a-412f-adf3-1224da9bbb2b",
        "word": "Valuable",
        "meaning": "귀중한, 비싼 (가치가 높은)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "4ebd97ed-6df5-45af-82a1-f03738126077",
        "word": "Precious",
        "meaning": "귀중한, 소중한 (매우 아끼는)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "930171e6-9ac5-4d4a-829b-6af9998fc62e",
        "word": "Priceless",
        "meaning": "돈으로 살 수 없는 (매우 귀중한)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "a2975949-5b35-4c73-9801-5bba802c66ad",
        "word": "Invaluable",
        "meaning": "매우 유용한 (값을 따질 수 없을 만큼 귀한)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "0b513dba-4778-4f14-a148-74d753fb58ad",
        "word": "Worthless",
        "meaning": "가치 없는 (쓸모없는)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "671c5b11-b5bf-43ec-b8f5-cb936e03f7fa",
        "word": "Cheap",
        "meaning": "싼, 싸구려의 (가격이 낮거나 품질이 나쁜)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "90977a53-b4df-4d00-a17f-a502bf84454f",
        "word": "Inexpensive",
        "meaning": "저렴한 (비싸지 않은 - 긍정적)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "e69896c6-2924-46ab-b2c8-7161862a71c5",
        "word": "Inferior",
        "meaning": "질이 떨어지는 (하급의)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "0ea364c5-27e9-4dc1-a1d1-288afe330a8c",
        "word": "Shoddy",
        "meaning": "조잡한 (싸구려로 대충 만든)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "74dfcae8-1c1a-4e59-8e1e-3e81355064d6",
        "word": "Rip-off",
        "meaning": "바가지 (터무니없이 비싼 것 - 속어)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "e09a22a3-d576-4b54-b347-de7727492ea2",
        "word": "Steal",
        "meaning": "거저나 다름없는 것 (너무 싸게 잘 산 것)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "6099c47b-8fe1-4a90-b4f5-a3f757128e2d",
        "word": "Deal",
        "meaning": "거래, 싼 물건",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "92189cc4-0d43-425c-8b2d-b11b624bc3b7",
        "word": "Expense",
        "meaning": "지출, 비용 (돈이 나가는 것)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "76323233-fff2-4f42-aed1-692c96b054ac",
        "word": "Expenditure",
        "meaning": "지출, 경비 (공적인 지출)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "0fa5ed7a-3784-419f-902b-13c7fdc012eb",
        "word": "Overhead",
        "meaning": "고정비, 간접비 (운영 유지비)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "038988fc-cfd5-452a-b9d9-fb36abc64a72",
        "word": "Quote",
        "meaning": "견적액 (확정된 제시 가격)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "10e4294a-9b7b-4484-864d-4009abdfb8fe",
        "word": "Outlay",
        "meaning": "경비, 지출 (시작할 때 드는 돈)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "e2499f52-0980-43d7-952c-2197e2941805",
        "word": "Budget",
        "meaning": "예산 (계획된 돈)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "7c55f3ce-dc48-4cb8-b710-ff14eb7ce29f",
        "word": "Estimate",
        "meaning": "견적, 추정 (예상 가격)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "a62d42c7-1e7d-4f64-ad54-ce40b8c467ad",
        "word": "Valuation",
        "meaning": "평가액 (가치 산정)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "fb545737-39af-4ce9-8819-3b23b00d0878",
        "word": "Assessment",
        "meaning": "평가, 사정 (세금 등을 위한 평가)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "79c30d01-b043-426b-9259-5455d0cef2c5",
        "word": "Appraisal",
        "meaning": "감정, 평가 (전문가에 의한 가치 평가)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "f828cb6e-015d-46ee-9774-8ba3c08c2ea5",
        "word": "Charge",
        "meaning": "요금, 청구하다 (서비스 대가)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "5940871e-ea75-48dc-b2b3-4fd2bd6326a8",
        "word": "Fee",
        "meaning": "수수료, 요금 (전문 서비스/입장료)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "8ab586c9-2e69-4aec-ad07-e9fae66efbac",
        "word": "Fare",
        "meaning": "운임 (교통 요금)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    },
    {
        "card_id": "0a6f8471-61e9-4e61-b0a5-19a2299f1c38",
        "word": "Rate",
        "meaning": "요금, 비율 (기준에 따른 가격)",
        "deck_id": "2bd3fdbc-3b68-45c7-99ce-b7a0b21bebd9",
        "deck_title": "COST_PRICE_VALUE"
    }
]

RELEVANT_TAGS = [
    "meeting",
    "shopping",
    "warm",
    "food",
    "university",
    "home",
    "interview",
    "conversation",
    "relationship",
    "wellness"
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
- 위 태그들은 'COST_PRICE_VALUE' 덱과 관련이 깊은 주제들입니다
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

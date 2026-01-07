#!/usr/bin/env python3
"""
예문 생성 스크립트: SIMPLICITY_CLARITY

이 스크립트는 'SIMPLICITY_CLARITY' 덱의 단어들에 대해
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
    "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
    "deck_title": "SIMPLICITY_CLARITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "a0d36370-ec60-47c1-a170-922d8eca0081",
        "word": "Simple",
        "meaning": "단순한 (복잡하지 않은)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "ea7ff179-18f8-4e53-9731-e854d1b6b709",
        "word": "Clear",
        "meaning": "명확한 (이해하기 쉬운)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "baae13d2-8705-4528-b4ed-0563e8a459ca",
        "word": "Plain",
        "meaning": "꾸밈없는, 평이한 (솔직하고 단순한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "0da53072-e67b-41f9-988d-6237ec8b1f17",
        "word": "Straightforward",
        "meaning": "간단명료한 (비비 꼬지 않은)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "40c90d87-f063-4016-84b9-da12d770aae5",
        "word": "Direct",
        "meaning": "직접적인 (우회하지 않는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "659726be-8658-43cc-9630-c124d6c5984e",
        "word": "Coherent",
        "meaning": "일관성 있는 (논리가 명확한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "8b918ea2-ed60-4aa2-bfdb-16983d279782",
        "word": "Lucid",
        "meaning": "명쾌한 (투명하듯 맑고 이해하기 쉬운)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "5f7b01ff-f664-49d9-9ad5-11f974282cb8",
        "word": "Distinct",
        "meaning": "뚜렷한 (구분이 명확한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "140d2d35-524f-4c50-b935-a5b356230427",
        "word": "Explicit",
        "meaning": "명시적인 (숨김없이 드러난)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "ac77b104-b537-4096-a370-878903139b3f",
        "word": "Obvious",
        "meaning": "뻔한, 분명한 (누가 봐도 알 수 있는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "9a1912e0-e9b5-4c7e-9c79-f16a480df34d",
        "word": "Evident",
        "meaning": "명백한 (증거가 있어 확실한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "1166d15b-076c-4b59-b9ce-da77c9482725",
        "word": "Apparent",
        "meaning": "분명한, 외관상의 (눈에 보이는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "232f206d-0d90-48b2-9c94-4368c804251c",
        "word": "Rudimentary",
        "meaning": "기초적인, 미발달의 (아주 기본적인 수준)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "b0ea34aa-693f-4d33-b68b-326fd0cfc99e",
        "word": "Elementary",
        "meaning": "초보적인 (기초 단계의)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "5c57bba0-b2b3-4796-80c3-026391f9b147",
        "word": "Manifest",
        "meaning": "나타나다, 명백한 (겉으로 드러난)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "fde7bd3e-30ba-4fb9-9ad1-cde9e7764df9",
        "word": "Transparent",
        "meaning": "투명한, 빤히 들여다보이는 (숨김없는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "89f12993-e6ca-463d-9862-6c62d83b41a8",
        "word": "Self-explanatory",
        "meaning": "설명이 필요 없는 (보면 바로 아는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "2e2f05ad-9c2d-496a-a94d-5aa050241ef8",
        "word": "Unambiguous",
        "meaning": "모호하지 않은 (뜻이 하나로 명확한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "7b284e3d-99d4-44c0-9896-a9c87518d019",
        "word": "Unmistakable",
        "meaning": "틀림없는 (오해할 여지가 없는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "866937e6-1ada-4d5c-ae76-925315bc1746",
        "word": "Basic",
        "meaning": "기본적인 (가장 밑바탕이 되는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "f5c1368c-b6c8-41a8-89c6-8e95c45be17c",
        "word": "Fundamental",
        "meaning": "근본적인 (핵심이 되는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "0b5cc5ac-b258-445e-8e30-c05d867374d7",
        "word": "Pure",
        "meaning": "순수한 (섞이지 않은)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "95163afe-3707-4776-8c72-eea55132c11f",
        "word": "Stark",
        "meaning": "삭막한, 있는 그대로의 (꾸밈없이 적나라한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "5b73ba73-ca0e-4ae0-a721-cf7d345d84cd",
        "word": "Unadorned",
        "meaning": "꾸밈없는 (장식이 없는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "0868551b-8db2-45df-81ac-d184cfbc7769",
        "word": "Minimalist",
        "meaning": "미니멀한 (최소한의 것만 있는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "387ea0a8-d79f-421d-bbad-0dddfa85ad4d",
        "word": "Bare",
        "meaning": "벌거벗은, 딱 그만큼의 (최소한의)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "1ec36930-b442-48b7-95c3-c76b7376d4be",
        "word": "Essential",
        "meaning": "필수적인, 본질적인 (군더더기 뺀 핵심)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "1c0f8162-0afa-4aa8-bf82-9256a5c35de5",
        "word": "Core",
        "meaning": "핵심의 (가장 중심이 되는)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "6e8c318c-db83-4547-827c-166d7bfeec56",
        "word": "Concise",
        "meaning": "간결한 (짧고 명확한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    },
    {
        "card_id": "fdb60be1-76a6-4e4b-9325-75cd4596bf99",
        "word": "Crisp",
        "meaning": "상쾌한, 바삭한, 간결한 (깔끔하고 명쾌한)",
        "deck_id": "8e707742-a241-4c9f-8cb5-a25cbc231c39",
        "deck_title": "SIMPLICITY_CLARITY"
    }
]

RELEVANT_TAGS = [
    "career",
    "nature",
    "feeling",
    "family",
    "social",
    "startup",
    "school",
    "style",
    "sad",
    "restaurant"
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
- 위 태그들은 'SIMPLICITY_CLARITY' 덱과 관련이 깊은 주제들입니다
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

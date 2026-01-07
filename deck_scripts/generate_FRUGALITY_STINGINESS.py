#!/usr/bin/env python3
"""
예문 생성 스크립트: FRUGALITY_STINGINESS

이 스크립트는 'FRUGALITY_STINGINESS' 덱의 단어들에 대해
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
    "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
    "deck_title": "FRUGALITY_STINGINESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "f815dd3c-d4ac-453d-93d6-18338c3289a8",
        "word": "Frugal",
        "meaning": "검소한 (필요한 것만 사며 아끼는 - 긍정적)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "0d33ddb6-30ac-4f39-84fb-7409f390ffe4",
        "word": "Thrifty",
        "meaning": "절약하는 (돈 관리를 잘하는 - 긍정적)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "732c6900-3fc5-4b39-971d-364fcbfc410e",
        "word": "Economical",
        "meaning": "경제적인 (낭비가 없고 효율적인)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "39f8ac13-f8f8-4330-b614-0cae35a08676",
        "word": "Prudent",
        "meaning": "신중한 (미래를 위해 돈을 아끼는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "027efbcc-c722-4e2c-8aa8-f043e2d1ca81",
        "word": "Budget",
        "meaning": "저렴한, 예산의 (가격이 싼)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "d40de30c-b26a-4b5b-ac91-a4c22b2558dc",
        "word": "Cheap",
        "meaning": "싼, 인색한 (값이 싸거나 돈 쓰기 싫어하는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "0c853102-b45a-4116-9c07-78ee40c50b1e",
        "word": "Stingy",
        "meaning": "인색한 (돈 쓰는 것을 싫어하는 - 부정적)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "bbd67357-455a-48a0-9d0f-aa779e80390e",
        "word": "Miserly",
        "meaning": "구두쇠 같은 (돈을 모으기만 하고 안 쓰는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "8588ff9e-eac3-44c0-bc3d-f6512bb0f10d",
        "word": "Parsimonious",
        "meaning": "지나치게 인색한 (돈을 극도로 아끼는 - 격식)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "7a6dce83-95fe-47af-9310-db77a10ac7e6",
        "word": "Tight-fisted",
        "meaning": "주먹을 꽉 쥔 (인색한) (돈을 안 놓으려는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "11284b1b-4365-4735-a5e6-416d6499870b",
        "word": "Penny-pinching",
        "meaning": "구두쇠 짓을 하는 (동전 한 닢도 아끼는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "415c7fd0-92a5-4d69-a663-a29a792a91c2",
        "word": "Mean",
        "meaning": "인색한 (영국식: 돈에 대해 쩨쩨한)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "740e547c-11e2-49d7-b628-82d1056ed12a",
        "word": "Close",
        "meaning": "돈을 잘 안 쓰는 (지갑을 닫은)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "d44ecaca-2119-45d3-ad3a-33b366700783",
        "word": "Sparing",
        "meaning": "아껴 쓰는, 조금만 쓰는 (절약하는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "bc8f2dcd-df96-4787-a8b7-86d114bea888",
        "word": "Ascetic",
        "meaning": "금욕적인 (물질적 쾌락을 거부하는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "7a2af701-17d5-4296-9134-53c42e817c72",
        "word": "Austere",
        "meaning": "검소한, 긴축의 (사치 없이 엄격한)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "166b0bb4-ebae-40d2-8fcd-5bfba4f3fc74",
        "word": "Conservative",
        "meaning": "보수적인 (재정적으로 모험하지 않는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "32c1d296-c312-4f42-9a21-ed7f2411ac3e",
        "word": "Cost-effective",
        "meaning": "비용 효율적인 (가격 대비 성능이 좋은)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "ef90141e-25c8-4190-b546-e81cb5241583",
        "word": "Discount",
        "meaning": "할인 (깎아주는 것)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "f1f3eb3a-219f-41b5-b4a1-8709c6f8d49c",
        "word": "Bargain",
        "meaning": "특가품, 흥정 (싸게 잘 산 물건)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "fbb286cc-d04a-421f-a230-c4fadf16092f",
        "word": "Value",
        "meaning": "가성비 좋은, 가치 (가격 대비 가치가 있는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "134a4f4c-9125-42ce-a194-5fbe57d7021b",
        "word": "Low-cost",
        "meaning": "저비용의 (값이 싼)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "e8c31149-1a0f-4396-95f9-cb5abfad4037",
        "word": "Reasonable",
        "meaning": "합리적인 (가격이 적당한)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "4039dd37-199c-4ead-9922-285752e3375c",
        "word": "Affordable",
        "meaning": "감당할 수 있는 (비싸지 않은)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "73d2d3a7-f11e-4b0c-a95e-9cc7c79380dd",
        "word": "Modest",
        "meaning": "수수한, 적당한 (비싸지 않은)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "7fa98e3e-0256-47ea-814e-691f5a11355e",
        "word": "Simple",
        "meaning": "소박한 (화려하지 않은)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "3b56b9bc-098f-4ca1-b4aa-aca81a307ff6",
        "word": "Spartan",
        "meaning": "검소하고 엄격한 (편의시설이 없는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "007a2c31-7b84-4666-9243-e9bc083f21db",
        "word": "Skimping",
        "meaning": "지나치게 아끼는 (재료 등을 덜 쓰는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "ff7c0714-7e3d-41eb-b354-4ec283ce7056",
        "word": "Tight",
        "meaning": "인색한, 꽉 조인 (돈을 안 푸는)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    },
    {
        "card_id": "75bbabae-be76-4a13-86ed-aef9deddea3e",
        "word": "Scrooge",
        "meaning": "스크루지, 구두쇠 (인색한 사람의 대명사)",
        "deck_id": "f4c171f5-08fd-4436-829c-2f9dd9204597",
        "deck_title": "FRUGALITY_STINGINESS"
    }
]

RELEVANT_TAGS = [
    "fashion",
    "place",
    "job",
    "hobby",
    "sad",
    "career",
    "health",
    "office",
    "business",
    "digital"
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
- 위 태그들은 'FRUGALITY_STINGINESS' 덱과 관련이 깊은 주제들입니다
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

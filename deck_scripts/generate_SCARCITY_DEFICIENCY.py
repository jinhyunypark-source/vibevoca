#!/usr/bin/env python3
"""
예문 생성 스크립트: SCARCITY_DEFICIENCY

이 스크립트는 'SCARCITY_DEFICIENCY' 덱의 단어들에 대해
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
    "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
    "deck_title": "SCARCITY_DEFICIENCY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "06c971f2-865b-41f4-85cf-e1b545a31646",
        "word": "Scarce",
        "meaning": "희소한, 부족한 (구하기 힘든)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "124147c0-06a9-4c60-8070-04be7822d3cc",
        "word": "Rare",
        "meaning": "드문, 희귀한 (자주 일어나지 않는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "897ee704-94ab-46a4-a55d-99563ab5c1c2",
        "word": "Sparse",
        "meaning": "드문드문한 (밀도가 낮은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "d6b7f370-7204-4c92-a4d8-69d2cf95008a",
        "word": "Scant",
        "meaning": "부족한, 거의 없는 (충분하지 않은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "d3ca1f72-a0e5-47a5-b7a7-fb4a0928ae05",
        "word": "Meager",
        "meaning": "빈약한, 불충분한 (양이나 질이 형편없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "4b33773d-044e-4a28-a33f-d506e855ce3c",
        "word": "Paltry",
        "meaning": "쥐꼬리만한, 시시한 (너무 적어서 하찮은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "9dbcc597-57d2-42c1-bd92-17f70d567424",
        "word": "Insufficient",
        "meaning": "불충분한 (필요량을 채우지 못한)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "9d6966b5-5105-4aaa-88c9-6876b21d2e9d",
        "word": "Inadequate",
        "meaning": "부적절한, 불충분한 (요구에 못 미치는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "8fd79c25-d69b-4672-8846-63d59fcc3742",
        "word": "Lacking",
        "meaning": "부족한, 결여된 (없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "2ea0dd05-e894-461e-966d-dfe35041db05",
        "word": "Wanting",
        "meaning": "모자라는, 부족한 (기대에 못 미치는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "1a965fc9-ff6c-4d73-9baa-81507e385cb3",
        "word": "Deficient",
        "meaning": "결핍된 (필수 요소가 빠진)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "a4276337-e5e3-48f9-938c-27fc9b31b1bd",
        "word": "Short",
        "meaning": "부족한 (모자라는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "bc6ee05b-b14a-4b92-bdd7-448453559c89",
        "word": "Tight",
        "meaning": "빠듯한 (여유가 없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "6f14d043-c3f6-4b3c-a023-713f16b5459a",
        "word": "Limited",
        "meaning": "제한된 (많지 않은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "a1d78eea-b287-4d5c-94f5-a6e915313eec",
        "word": "Empty",
        "meaning": "빈 (내용물이 없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "364be8d4-d893-419d-81fa-00f95be523bc",
        "word": "Vacant",
        "meaning": "비어 있는 (사람이 없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "883d0ba9-15e7-4470-8d0e-f70a623a6bf3",
        "word": "Void",
        "meaning": "텅 빈, 무효의 (공허한 공간)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "1b9390ce-1ed8-4a54-940d-b21afa47016a",
        "word": "Barren",
        "meaning": "척박한, 불모의 (생산력이 없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "076b9226-81e0-4ae9-b4a3-80eca737d0b2",
        "word": "Destitute",
        "meaning": "극빈한 (가진 것이 아무것도 없는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "c5054790-d06a-49fb-bce9-b0486bbfae69",
        "word": "Impoverished",
        "meaning": "빈곤한 (가난해진)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "0f964b87-0601-4b23-a8cc-0f9ada9d904c",
        "word": "Poor",
        "meaning": "가난한, 형편없는 (질이나 양이 낮은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "30ec2696-1735-41ad-a006-1765810eb530",
        "word": "Deprived",
        "meaning": "궁핍한, 불우한 (필수적인 것을 못 누리는)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "b8fe20f8-0ec7-4389-b81c-8176c1b188ae",
        "word": "Dearth",
        "meaning": "부족, 결핍 (기근처럼 모자람 - 명사)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "d313040c-6994-4b2f-96c8-50cc219e72fc",
        "word": "Famine",
        "meaning": "기근 (식량이 극도로 부족한 상태)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "dddaa544-1cbf-4362-aa78-18ac66ac2c99",
        "word": "Drought",
        "meaning": "가뭄 (물 부족)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "649cb872-b16e-40e1-b1dc-57946a7ff391",
        "word": "Deficit",
        "meaning": "적자, 부족액 (수입보다 지출이 많은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "a62dec6c-0a5a-44ac-8521-16650fbcfc71",
        "word": "Shortage",
        "meaning": "부족 (수요보다 공급이 적음)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "569e91c5-1fce-4556-be81-81ef9d76a13a",
        "word": "Scarcity",
        "meaning": "희소성 (드묾)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "b105b9b4-65f9-4376-a0c9-f500232c716a",
        "word": "Need",
        "meaning": "필요, 궁핍 (가난)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    },
    {
        "card_id": "a12e88f2-4820-4794-8fe3-4fd8e85d3b42",
        "word": "Minimal",
        "meaning": "최소한의 (아주 적은)",
        "deck_id": "c1bb612c-764b-4dc6-862c-e8eb98389b00",
        "deck_title": "SCARCITY_DEFICIENCY"
    }
]

RELEVANT_TAGS = [
    "daily_life",
    "business",
    "happy",
    "study",
    "outdoor",
    "journey",
    "career",
    "conversation",
    "weather",
    "family"
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
- 위 태그들은 'SCARCITY_DEFICIENCY' 덱과 관련이 깊은 주제들입니다
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

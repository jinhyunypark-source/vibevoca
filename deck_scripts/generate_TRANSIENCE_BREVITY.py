#!/usr/bin/env python3
"""
예문 생성 스크립트: TRANSIENCE_BREVITY

이 스크립트는 'TRANSIENCE_BREVITY' 덱의 단어들에 대해
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
    "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
    "deck_title": "TRANSIENCE_BREVITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "5de5f3b1-a37f-4251-9db6-ac1bb48857cd",
        "word": "Ephemeral",
        "meaning": "덧없는, 단명하는 (하루살이처럼 수명이 짧은)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "80b97e52-b4bd-42a9-8bda-d7b404a6dbf1",
        "word": "Fleeting",
        "meaning": "순식간의, 덧없는 (빠르게 지나가 버리는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "e4c33656-982a-4651-a800-994fc62d1055",
        "word": "Interim",
        "meaning": "중간의, 임시의 (다음 단계 전까지의)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "2177ed27-b593-4112-bde5-aede433f1cb5",
        "word": "Provisional",
        "meaning": "임시의, 잠정적인 (나중에 바뀔 수 있는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "0c117e23-7482-4186-b60a-32a173983b9f",
        "word": "Transient",
        "meaning": "일시적인, 머물다 가는 (오래 머물지 않는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "c6f5a302-ef02-48c8-b08e-1f076dfd9761",
        "word": "Transitory",
        "meaning": "일시적인 (영원하지 않고 지나가는 성질의)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "bec23fd2-df03-4899-b479-a2e99477146e",
        "word": "Temporary",
        "meaning": "임시의 (정해진 기간만 쓰는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "c010e6a5-5a27-4165-89cb-139bb76d23da",
        "word": "Fugitive",
        "meaning": "도망 다니는, 덧없는 (붙잡아 둘 수 없는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "006c3c2e-6eb4-414d-9d86-5d1f1de6192d",
        "word": "Momentary",
        "meaning": "순간적인 (아주 짧은 찰나의)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "74b6ee3d-681c-40d8-b583-c0593e6a6c91",
        "word": "Brief",
        "meaning": "짧은, 잠시의 (시간이 길지 않은)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "bb6d1089-091a-403e-b45c-9d2d2de9bed7",
        "word": "Short-lived",
        "meaning": "단명하는, 오래가지 못하는",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "45d28481-88e7-4a6c-86fa-c47e00c9e4b1",
        "word": "Evanescent",
        "meaning": "쉬이 사라지는, 덧없는 (안개처럼 사라지는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "99baf7f0-71c8-49af-9aa2-9d8dc2d08609",
        "word": "Passing",
        "meaning": "지나가는, 일시적인 (머물지 않는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "2e5b7344-645b-4695-b442-79114fcd1d4e",
        "word": "Tentative",
        "meaning": "잠정적인, 머뭇거리는 (확정되지 않은)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "9fabba40-e580-442f-a9bf-48744f78deab",
        "word": "Cursory",
        "meaning": "대충 하는, 피상적인 (시간을 들이지 않은)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "f7737151-383b-44b9-b15d-e987c9656792",
        "word": "Instantaneous",
        "meaning": "즉각적인 (동시에 일어나는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "97a054f2-8074-4458-b513-e98bbe8d5e6b",
        "word": "Abrupt",
        "meaning": "갑작스러운 (예고 없이 뚝 끊기는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "9ad3595d-5589-4bf8-b02e-2f41eff715f3",
        "word": "Sudden",
        "meaning": "갑작스러운 (예상치 못한)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "816cd86e-e550-4685-982b-98ce7078caa1",
        "word": "Short-term",
        "meaning": "단기적인 (가까운 미래만 보는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "1b7f4ed6-4626-40a5-818f-6441fbce6b4a",
        "word": "Impermanent",
        "meaning": "영구적이지 않은 (변하기 쉬운)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "79653d5a-abfe-4cf0-856f-5fc0b9bd064b",
        "word": "Volatile",
        "meaning": "휘발성의, 변덕스러운 (금방 변해버리는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "cfa34e39-4707-4efc-afa3-0ec3195d3ab4",
        "word": "Swift",
        "meaning": "신속한 (재빠르게 지나가는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "16bb79b6-64aa-49fa-be70-1d1b116a4011",
        "word": "Hasty",
        "meaning": "서두르는, 성급한 (시간을 충분히 안 쓴)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "8e044fd4-124c-4d6e-8097-7915c47f170c",
        "word": "Fly-by-night",
        "meaning": "믿을 수 없는, 덧없는 (야반도주하는/잠깐 하고 마는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "7e3e98e6-c5f6-4549-9839-b134a80b1b46",
        "word": "Mortal",
        "meaning": "언젠가 죽는, 필멸의 (유한한 생명의)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "6a5a2ef7-890f-4123-b415-0c1ea9df5916",
        "word": "Finite",
        "meaning": "유한한 (한계가 있는)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "54812bb7-9178-4cfb-8f8f-87ab9d47bfe0",
        "word": "Phase",
        "meaning": "단계, 시기 (지나가는 한 국면)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "792ce43c-c357-4ee2-a5fd-a5cdf776a924",
        "word": "Spell",
        "meaning": "잠깐의 기간 (날씨나 활동의 짧은 기간)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "f16a0710-922d-4dec-a16e-a35668567ce3",
        "word": "Flash",
        "meaning": "섬광, 순간 (번쩍하는 사이)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    },
    {
        "card_id": "5a24ea52-ca64-4bcb-a5e3-ddb77c04eeee",
        "word": "Blink",
        "meaning": "눈 깜짝할 사이 (아주 짧은 순간)",
        "deck_id": "c3bf4630-ac47-4bf0-9cab-d147f7ebf1ac",
        "deck_title": "TRANSIENCE_BREVITY"
    }
]

RELEVANT_TAGS = [
    "study",
    "vacation",
    "fashion",
    "internet",
    "family",
    "cooking",
    "business",
    "job",
    "art",
    "social"
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
- 위 태그들은 'TRANSIENCE_BREVITY' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: TRANSFORMATION

이 스크립트는 'TRANSFORMATION' 덱의 단어들에 대해
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
    "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
    "deck_title": "TRANSFORMATION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "cf02ecf5-fbc4-475e-8cc9-0fb38c150255",
        "word": "Evolve",
        "meaning": "진화하다 (서서히 더 나은 형태로 변하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "64d2f5c4-de12-4bdd-9fdc-934e8fd2e685",
        "word": "Transform",
        "meaning": "변형시키다 (모습을 완전히 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "918aaee1-6fe7-4e63-b410-f5e6b50d3e61",
        "word": "Metamorphose",
        "meaning": "변태하다, 탈바꿈하다 (생물학적/극적 변화)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "5a9d668b-05d4-48bd-93f8-e23225ae4346",
        "word": "Convert",
        "meaning": "전환하다 (용도나 형태를 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "1cf4497c-2dcd-4815-8a2d-3ebec87a02a3",
        "word": "Alter",
        "meaning": "고치다, 변경하다 (약간 수정하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "e048b91c-392f-4ec6-86d7-4bed27f1f414",
        "word": "Modify",
        "meaning": "수정하다 (개선을 위해 조금 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "266f1f43-b10d-43e4-b5ce-0a3bf4c0654a",
        "word": "Adjust",
        "meaning": "조절하다, 맞추다 (적합하게 맞추다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "d9d38b3a-22af-43be-a0b1-8cf2300e8ece",
        "word": "Adapt",
        "meaning": "적응하다 (환경에 맞게 변화하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "6ac70c37-2f4c-4a7c-9ac2-d5f07993d63f",
        "word": "Acclimate",
        "meaning": "익숙해지다, 순응시키다 (기후/환경에)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "de028bf0-911c-45ed-bda4-93e9f2866403",
        "word": "Revise",
        "meaning": "개정하다 (다시 보고 고치다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "b4c9110a-3b16-4445-88e1-bf1521cd2b85",
        "word": "Reform",
        "meaning": "개혁하다 (제도를 뜯어고치다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "d2bb64e4-99e9-4c7d-9d83-8c6eb58b5e4d",
        "word": "Remodel",
        "meaning": "리모델링하다 (구조를 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "3e9fd0a1-b284-4c88-9246-33ffdedf46d7",
        "word": "Renovate",
        "meaning": "보수하다, 새롭게 하다 (낡은 것을 새것처럼)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "d36783f0-061b-444a-b968-8ab0bbe0499f",
        "word": "Revolutionize",
        "meaning": "혁신을 일으키다 (근본적으로 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "38636fd5-ceb2-4da0-a2b4-251961502e64",
        "word": "Shift",
        "meaning": "이동하다, 바뀌다 (위치나 방향을 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "5a3caaf5-4b6b-43c1-a30c-c17c4a614fc1",
        "word": "Vary",
        "meaning": "다양하다, 달라지다 (변화를 주다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "5f8d04d3-f7b8-4f96-930d-cbf1be5e41ad",
        "word": "Diversify",
        "meaning": "다각화하다 (여러 가지로 나누다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "3279f005-aedb-4633-90b9-9b36c9620ba9",
        "word": "Mutate",
        "meaning": "돌연변이하다 (유전자가 변하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "5f26a13a-a157-48cc-bb73-1819404eb207",
        "word": "Transmute",
        "meaning": "(성질을) 바꾸다 (마법/연금술처럼 변하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "8c8fec4d-6aaf-4039-9235-b6a44965b1d3",
        "word": "Reshape",
        "meaning": "모양을 다시 만들다 (재형성하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "5361fcf6-269b-4eda-b3c5-b2e20a290245",
        "word": "Reconfigure",
        "meaning": "재구성하다 (설정을 다시 하다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "55f3ab58-6382-4959-a84c-9a6e42627c26",
        "word": "Overhaul",
        "meaning": "철저히 점검하다, 뜯어고치다",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "1f06e854-cd08-4fc9-99ed-f67b42811ccd",
        "word": "Refine",
        "meaning": "정제하다, 다듬다 (불순물을 없애다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "b32ef000-3cd5-43c6-823d-f7f6a312adbc",
        "word": "Polish",
        "meaning": "광을 내다, 세련되게 하다",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "05577cbb-e238-4ccc-a34d-c218f07be9bf",
        "word": "Tweak",
        "meaning": "살짝 조정하다 (미세하게 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "f02de0f2-a4b1-4bfe-b9e2-e678485d27a8",
        "word": "Customize",
        "meaning": "주문 제작하다 (개인에게 맞추다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "6728b70d-20d6-43f7-89f5-8a6f90801b0a",
        "word": "Tailor",
        "meaning": "(목적에) 맞추다 (재단사가 옷을 맞추듯)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "e2138afa-688f-4859-90d0-33c822dbcd93",
        "word": "Transition",
        "meaning": "이행하다 (다른 상태로 넘어가다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "d2a7a0aa-8660-480f-b972-0865266ccd37",
        "word": "Switch",
        "meaning": "바꾸다, 전환하다 (다른 것으로 휙 바꾸다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    },
    {
        "card_id": "a60413af-cfb1-4651-bb67-ce9776a8c85f",
        "word": "Substitute",
        "meaning": "대체하다 (대신 쓰다)",
        "deck_id": "20d4b397-2173-4a22-98d0-4840e86b98ae",
        "deck_title": "TRANSFORMATION"
    }
]

RELEVANT_TAGS = [
    "sport",
    "fashion",
    "technology",
    "outdoor",
    "sad",
    "cooking",
    "place",
    "career",
    "food",
    "health"
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
- 위 태그들은 'TRANSFORMATION' 덱과 관련이 깊은 주제들입니다
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

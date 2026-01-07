#!/usr/bin/env python3
"""
예문 생성 스크립트: OPPRESSION_TYRANNY

이 스크립트는 'OPPRESSION_TYRANNY' 덱의 단어들에 대해
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
    "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
    "deck_title": "OPPRESSION_TYRANNY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "063c84e4-2d46-4c69-bc32-a97c67ab2b13",
        "word": "Oppressive",
        "meaning": "억압적인 (숨 막히게 내리누르는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "6f0eb068-e74d-4685-b567-b2b664ae917f",
        "word": "Tyrannical",
        "meaning": "폭군의, 전제적인 (제멋대로 권력을 휘두르는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "dab40673-aa79-4686-b1ee-103eda4c639f",
        "word": "Dictatorial",
        "meaning": "독재적인 (남의 말을 안 듣고 지시만 하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "f89be803-fbe9-4c2d-b85e-381714637fa7",
        "word": "Autocratic",
        "meaning": "전제 군주적인, 독단적인 (혼자서 모든 결정을 내리는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "52051977-1670-4c5f-8746-b4d0fb724f13",
        "word": "Despotic",
        "meaning": "폭군적인 (절대 권력으로 횡포를 부리는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "3c5e35b0-249c-4d5f-ad67-cb4d76019eb4",
        "word": "Totalitarian",
        "meaning": "전체주의적인 (개인의 자유를 완전히 통제하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "cfa9962b-1875-43eb-b867-cb0186a9abe9",
        "word": "Coercive",
        "meaning": "강압적인 (힘이나 위협으로 강요하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "22f42379-8580-4cdb-908c-edd57320208e",
        "word": "Draconian",
        "meaning": "매우 엄격한, 가혹한 (법이나 처벌이 지나친)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "48783207-8dbe-42a4-8bee-b855fcb293fb",
        "word": "Repressive",
        "meaning": "탄압하는 (감정이나 자유를 억누르는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "8bce3d0b-799b-4ef0-b709-ec83dc725f9f",
        "word": "Ruthless",
        "meaning": "무자비한 (동정심 없이 잔인한)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "699ecfa7-2f94-41ea-8cd6-582a1b69b359",
        "word": "Cruel",
        "meaning": "잔인한 (고통을 주는 것을 즐기는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "70f34486-e2fb-4278-8fb1-d987ecb739b2",
        "word": "Heavy-handed",
        "meaning": "가혹한, 서투른 (힘을 너무 과하게 쓰는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "b8d254d0-b096-437a-9d46-0b682b03a279",
        "word": "Iron-fisted",
        "meaning": "철권통치의 (매우 엄격하고 타협 없는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "c960aeb0-2e0d-411e-84ae-f927722781e9",
        "word": "Domineering",
        "meaning": "오만한, 거만한 (남을 쥐고 흔들려는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "05237915-2da0-4f0f-bcfd-ba729b77dd6c",
        "word": "Bossy",
        "meaning": "이래라저래라 하는 (사사건건 지시하는 - 비격식)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "36a2d3e6-4add-4fe4-b725-e29364ac8c6a",
        "word": "Imperious",
        "meaning": "고압적인 (황제처럼 거만하게 명령하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "0585a30b-5a87-4414-8b21-822054564a91",
        "word": "Arbitrary",
        "meaning": "제멋대로인, 독단적인 (원칙 없이 기분 내키는 대로)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "1966f8b1-6d14-47ed-954f-61d8a971a016",
        "word": "Unjust",
        "meaning": "부당한 (정의롭지 못한)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "0d34d002-e8e1-4b2d-b80d-f7e139a4ca8b",
        "word": "Exploitative",
        "meaning": "착취하는 (남의 노동력을 부당하게 이용하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "c1106e43-306f-4fb1-a63e-b37244131670",
        "word": "Subjugating",
        "meaning": "예속시키는, 정복하는 (지배하에 두는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "7698b9fd-5a85-4b9d-9479-319a80add92d",
        "word": "Crushing",
        "meaning": "짓밟는, 압도적인 (희망이나 저항을 박살 내는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "6863e2b6-0492-44b3-a7ed-7255dd749f6e",
        "word": "Intimidating",
        "meaning": "위협적인 (겁을 주는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "faa1280e-960a-4caf-90df-b98a6c8b56c2",
        "word": "Suffocating",
        "meaning": "숨 막히는 (자유가 없어 답답한)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "97f87495-b557-45cb-ac9f-2ddd98e4588e",
        "word": "Restrictive",
        "meaning": "제한하는, 구속하는 (자유를 막는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "8cd96a5b-abf2-4044-9baa-17b52b9b757b",
        "word": "Threatening",
        "meaning": "협박하는 (해를 끼칠 듯한)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "4ffad3e7-ab83-4fbf-8767-c38b8d5bf391",
        "word": "Menacing",
        "meaning": "위협적인 (불길하고 위험한 느낌)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "4bd12cf7-6ca8-45a0-bf96-27b34499a8d6",
        "word": "Bullying",
        "meaning": "괴롭히는 (약자를 못살게 구는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "3a3d9346-e429-42d4-a918-a2a72918dc3d",
        "word": "Overbearing",
        "meaning": "압제적인, 거만한 (남을 누르고 자기 뜻대로만 하는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "06b47746-d99a-425a-8fa6-3b8c1495a900",
        "word": "Violent",
        "meaning": "폭력적인 (물리적 힘을 쓰는)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    },
    {
        "card_id": "ebfb628e-9ffe-4d64-ab38-3ab4ca18bb53",
        "word": "Harsh",
        "meaning": "가혹한 (너무 엄하고 모진)",
        "deck_id": "be02ae19-dcf9-4709-ad19-d94833e992bd",
        "deck_title": "OPPRESSION_TYRANNY"
    }
]

RELEVANT_TAGS = [
    "warm",
    "health",
    "cooking",
    "happy",
    "meeting",
    "communication",
    "business",
    "medical",
    "education",
    "entrepreneur"
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
- 위 태그들은 'OPPRESSION_TYRANNY' 덱과 관련이 깊은 주제들입니다
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

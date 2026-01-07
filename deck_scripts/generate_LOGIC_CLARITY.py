#!/usr/bin/env python3
"""
예문 생성 스크립트: LOGIC_CLARITY

이 스크립트는 'LOGIC_CLARITY' 덱의 단어들에 대해
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
    "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
    "deck_title": "LOGIC_CLARITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "2caa0b2a-dad1-4cc7-ad56-02982280cd86",
        "word": "Articulate",
        "meaning": "조리 있는, 분명한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "e019f073-2e65-4763-8ab4-e02f0db156f0",
        "word": "Coherent",
        "meaning": "일관성 있는, 앞뒤가 맞는",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "88862819-3d7e-4c7b-ae7e-ba92a2a53a20",
        "word": "Candid",
        "meaning": "솔직한 (숨김없는)",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "6677655b-26cb-4be8-bc85-9347496b811a",
        "word": "Frank",
        "meaning": "노골적인, 솔직한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "63f9e3bc-0ff6-4c6e-ad7a-9b98bc5bdfcc",
        "word": "Logical",
        "meaning": "논리적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "a2a6a064-a982-44a2-8688-c978866317d8",
        "word": "Rational",
        "meaning": "이성적인, 합리적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "ec32d9ce-527f-499f-a68e-337215d94919",
        "word": "Lucid",
        "meaning": "명쾌한, 알기 쉬운",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "0a8d967e-fe1d-41aa-9f6f-4f4aeb4f65db",
        "word": "Subjective",
        "meaning": "주관적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "c2b3efa1-c722-47a1-a80b-d6988b71e403",
        "word": "Objective",
        "meaning": "객관적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "d3ecd33d-390c-4d74-adf5-ea78d2fa593d",
        "word": "Ambiguous",
        "meaning": "모호한 (두 가지 해석 가능)",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "4c3bda1e-a0ea-4b86-abb4-1e2d67db9380",
        "word": "Fallacious",
        "meaning": "틀린, 오류가 있는",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "1381858e-ef01-4860-9d52-e3f64b1b774a",
        "word": "Vague",
        "meaning": "애매한, 희미한 (구체적 X)",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "6a00292e-7355-427c-9a5b-89c8840e4618",
        "word": "Incoherent",
        "meaning": "앞뒤가 안 맞는, 횡설수설하는",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "7b52e8b9-c898-40bb-8e65-79afc40fb792",
        "word": "Irrational",
        "meaning": "비이성적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "3be5c7a3-7f9b-46a0-a882-26f1ce6e59f5",
        "word": "Valid",
        "meaning": "타당한, 유효한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "66380a74-8f88-409a-8754-22f50ed17490",
        "word": "Sound",
        "meaning": "건전한, 믿을 만한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "a205a4d0-bef3-4073-a7b1-c68a9e6b0962",
        "word": "Explicit",
        "meaning": "명시적인, 노골적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "7c47d358-4e11-4ca5-bc4d-a94bfbbe2427",
        "word": "Implicit",
        "meaning": "암시적인, 내포된",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "54ee95b1-0324-4690-b107-4965cecffb3c",
        "word": "Subtle",
        "meaning": "미묘한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "6c6f65b3-ee6e-45b7-a248-1cf92c7b46b1",
        "word": "Nuanced",
        "meaning": "뉘앙스가 있는 (미묘한 차이)",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "c677161d-cb1a-45b1-ada8-9f7ddbf518d2",
        "word": "Relevant",
        "meaning": "관련 있는, 적절한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "7ef99542-04ec-4647-857f-7f6897014d89",
        "word": "Irrelevant",
        "meaning": "무관한, 엉뚱한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "807740b8-9754-4717-b6b8-6ed901720d8d",
        "word": "Precise",
        "meaning": "정밀한, 꼼꼼한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "3a7ec700-e283-4667-9da7-711665eaa3ec",
        "word": "Accurate",
        "meaning": "정확한 (사실과 일치)",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "b23693d5-e849-4d47-b276-48d42815860a",
        "word": "Misleading",
        "meaning": "오해의 소지가 있는",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "e0b38585-3890-41ad-9954-280344b8538c",
        "word": "Deceptive",
        "meaning": "기만적인, 속이는",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "e4b92c46-540c-47db-bd4c-9e6261068c5c",
        "word": "Direct",
        "meaning": "직접적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "a0c8fa31-7f3f-4369-b1ab-531ae32188d1",
        "word": "Indirect",
        "meaning": "간접적인, 우회적인",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "88761816-356d-4fbb-8c56-14483386ad69",
        "word": "Obscure",
        "meaning": "모호한, 이해하기 힘든",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    },
    {
        "card_id": "c7a7dad8-8c9a-446b-a670-cad6ddf34c12",
        "word": "Clear-cut",
        "meaning": "명백한",
        "deck_id": "3c319e42-dc0b-4a02-a942-fb60237e1c10",
        "deck_title": "LOGIC_CLARITY"
    }
]

RELEVANT_TAGS = [
    "warm",
    "happy",
    "art",
    "social",
    "outdoor",
    "conversation",
    "schedule",
    "learning",
    "relationship",
    "friendship"
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
- 위 태그들은 'LOGIC_CLARITY' 덱과 관련이 깊은 주제들입니다
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

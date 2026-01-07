#!/usr/bin/env python3
"""
예문 생성 스크립트: SIGHT

이 스크립트는 'SIGHT' 덱의 단어들에 대해
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
    "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
    "deck_title": "SIGHT",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d74d3de2-0558-4a51-aa88-6880800f14f5",
        "word": "Ornate",
        "meaning": "장식이 화려한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "dcddb5fc-7cde-4119-8a04-ce8fd02eac73",
        "word": "Dapper",
        "meaning": "말쑥한 (남성)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "40dbb788-2a60-4ea5-99d1-c1c675c7bc6b",
        "word": "Eclectic",
        "meaning": "절충적인 (다양한)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "4e5fc110-41ad-442b-9e36-93165d67249c",
        "word": "Vibrant",
        "meaning": "(색이) 강렬한, 선명한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "31d338d4-e9b0-41fd-a2b8-ce8f99ddcc48",
        "word": "Opaque",
        "meaning": "불투명한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "05fa5481-0419-43de-87c4-21be65e397cf",
        "word": "Translucent",
        "meaning": "반투명한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "217e87e9-da2b-48e1-b478-7b55aa2d5b1c",
        "word": "Streamlined",
        "meaning": "유선형의, 능률적인",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "ca1c1d9c-7848-4ce1-9311-64ccb2780e9e",
        "word": "Bohemian (Boho)",
        "meaning": "자유분방한, 보헤미안",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "b5e88c19-43fc-4dd0-9559-2716117babd4",
        "word": "Sleek",
        "meaning": "매끄러운, 맵시 있는",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "a1b1bb20-f744-4aff-bf57-50e7659cc6a2",
        "word": "Chic",
        "meaning": "시크한, 세련된",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "53f8cc15-78fc-4f6f-adb1-883fba3a5800",
        "word": "Vintage",
        "meaning": "빈티지한 (진품 옛것)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "792d9750-500b-4696-9aee-234c8ddacbf8",
        "word": "Retro",
        "meaning": "복고풍의 (재현)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "64621b0d-06ea-47ae-9fa4-7c6e52ded2ed",
        "word": "Curvaceous",
        "meaning": "곡선미가 있는",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "e02302e7-df09-4626-8659-97c086b7f30a",
        "word": "Angular",
        "meaning": "각진, 모난",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "92dfa1d9-1af4-4595-9328-1c4c65aeef13",
        "word": "Avant-garde",
        "meaning": "아방가르드한 (전위적)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "66c5ca7f-3722-4945-8756-7f81f1aeedff",
        "word": "Preppy",
        "meaning": "단정한 (명문 학교풍)",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "53bbb825-f5de-4b93-a05b-0247698ced4c",
        "word": "Minimalist",
        "meaning": "미니멀한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "c122d5c8-edc8-4062-88e5-81dde7d502f0",
        "word": "Rustic",
        "meaning": "투박한, 시골풍의",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "0849bfc3-df6c-40b0-a21f-47caca9a7bc4",
        "word": "Futuristic",
        "meaning": "미래지향적인",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "d7eb500b-e201-454e-8f9a-ec51928f28ac",
        "word": "Geometric",
        "meaning": "기하학적인",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "80758a03-bedc-4038-92fd-0770ceb6bf66",
        "word": "Delicate",
        "meaning": "섬세한, 여리여리한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "4be6217c-f02c-433a-ac38-2122b29eeb8f",
        "word": "Monochrome",
        "meaning": "단색의, 흑백의",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "5079ddfd-67e2-4131-b4be-8969e15c14bd",
        "word": "Muted",
        "meaning": "(색이) 차분한, 톤 다운된",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "7f616597-8c95-48fa-9f83-25cfd0166682",
        "word": "Glossy",
        "meaning": "광택이 나는, 번들거리는",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "72178c98-c998-4b01-85be-baa3e0d9a2ca",
        "word": "Matte",
        "meaning": "무광의",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "1b172a82-9e21-4a1c-895b-880626382243",
        "word": "Textured",
        "meaning": "질감이 살아있는",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "a7d2e125-c7ce-4997-89ba-fbb05b0a13ca",
        "word": "Asymmetrical",
        "meaning": "비대칭의",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "52d7ed93-cd10-4856-93b2-65db5743dfa8",
        "word": "Bulky",
        "meaning": "부피가 큰",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "8cd69f42-5d63-4ba4-a89e-e08522f7c5ad",
        "word": "Compact",
        "meaning": "소형의, 콤팩트한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    },
    {
        "card_id": "804a1596-4d14-4396-9b5f-cc038094cb11",
        "word": "Bold",
        "meaning": "대담한, 뚜렷한",
        "deck_id": "c7010323-1ee7-45a3-b5b5-69229b44aacc",
        "deck_title": "SIGHT"
    }
]

RELEVANT_TAGS = [
    "smartphone",
    "activity",
    "shopping",
    "place",
    "restaurant",
    "planning",
    "time",
    "internet",
    "study",
    "nature"
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
- 위 태그들은 'SIGHT' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: PERSUASION_CONFLICT

이 스크립트는 'PERSUASION_CONFLICT' 덱의 단어들에 대해
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
    "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
    "deck_title": "PERSUASION_CONFLICT",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "880ac916-2094-4c6e-994a-deb47b100d2e",
        "word": "Persuasive",
        "meaning": "설득력 있는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "f5c0b316-c04e-4001-a3da-a137e3d2a73e",
        "word": "Convincing",
        "meaning": "납득이 가는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "2ad51eda-ffc3-411c-ad5f-5d815eb89d75",
        "word": "Compelling",
        "meaning": "강력한, 마음을 끄는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "1c5374e9-7c36-4423-a3a1-28319069f58e",
        "word": "Coercive",
        "meaning": "강압적인 (라)arcere가두다",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "814bf26d-b43c-4e3c-b9a1-e73d6de44b47",
        "word": "coercion",
        "meaning": "상자,숨기다",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "56345925-576c-4e92-b9b7-ed9cb6a3177e",
        "word": "arcane",
        "meaning": "비밀의, 신비 (esoteric)",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "f2a6a14a-316c-4d44-9498-3844823a604b",
        "word": "Accusatory",
        "meaning": "비난하는 듯한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "5d66e1e0-2c8d-480e-8de1-2b8603fca888",
        "word": "Flattering",
        "meaning": "아첨하는, 비위를 맞추는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "bfebe675-7c1e-49ad-a747-c95cc3f30b65",
        "word": "Defiant",
        "meaning": "반항적인, 도전적인",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "1c5cd5db-f90a-4db5-91a3-b277126060bd",
        "word": "Contentious",
        "meaning": "논쟁을 불러일으키는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "2f82a348-ac03-44d5-a95b-d54170e207e3",
        "word": "contend",
        "meaning": "경멸하다",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "36869451-54e6-4e4c-93dc-100c9c504559",
        "word": "Blunt",
        "meaning": "직설적인",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "9a182e69-5d36-4ebe-b10b-167c6507d684",
        "word": "Conciliatory",
        "meaning": "달래는, 회유하는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "533f89a5-2d1a-4a19-ae16-3c3deef4f727",
        "word": "concil",
        "meaning": "모임",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "94c78ea2-48dc-4fc9-b725-03b6f4a0e1f1",
        "word": "council",
        "meaning": "지방 의회",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "d47fe7c6-1fd3-4930-9834-59e4fe2f6840",
        "word": "Sycophantic",
        "meaning": "아부하는 (비굴함) 그_밀고자",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "ff2471c8-ffa3-4c42-b55e-806f3cb2b3b9",
        "word": "Complimentary",
        "meaning": "칭찬하는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "60c5b308-c0ca-4ba8-93f5-fb20f6628883",
        "word": "complement",
        "meaning": "보충하다. 보충물",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "1d774029-cff9-4f8a-a265-b8fd93dd4d7b",
        "word": "Manipulative",
        "meaning": "조종하는, 교활한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "43f1aaf2-34ca-432d-babe-4a926cc74828",
        "word": "Influential",
        "meaning": "영향력 있는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "eaec7c4b-9eaa-45a1-8928-45f5068080b7",
        "word": "Critical",
        "meaning": "비판적인",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "11f16482-b634-46c5-adce-bb61e723a508",
        "word": "Judgmental",
        "meaning": "남을 섣불리 판단하는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "2336f1e0-4c4f-499c-a1c6-171d5bc348e6",
        "word": "Apologetic",
        "meaning": "사과하는, 미안해하는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "a51a91ed-34d8-4f34-a7e3-9cc37e68c2c1",
        "word": "Agreeable",
        "meaning": "동의하는, 쾌활한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "3f3a59d6-badb-48c7-bec8-613e903f1152",
        "word": "Disagreeable",
        "meaning": "까칠한, 불쾌한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "ae95b49f-bcac-4a29-bc96-ea2d1f5b904a",
        "word": "Argumentative",
        "meaning": "논쟁을 좋아하는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "495cc63e-a78b-4135-b6d3-8f3e99837ab6",
        "word": "Diplomatic",
        "meaning": "외교적인, 요령 있는",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "320dcfae-92fc-4719-9bf7-59bf6fd1a7c2",
        "word": "Tactful",
        "meaning": "재치 있는, 눈치 빠른",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "357eb383-7a5f-42c1-9203-1a79bddfc1a0",
        "word": "Harsh",
        "meaning": "가혹한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    },
    {
        "card_id": "f05d288b-943e-4c95-b18f-e299fa3a7c9c",
        "word": "Gentle",
        "meaning": "온화한",
        "deck_id": "60b25d05-c509-4ca0-a116-c91772c3fb4d",
        "deck_title": "PERSUASION_CONFLICT"
    }
]

RELEVANT_TAGS = [
    "family",
    "conversation",
    "soccer",
    "home",
    "code",
    "shopping",
    "warm",
    "learning",
    "movie",
    "entertainment"
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
- 위 태그들은 'PERSUASION_CONFLICT' 덱과 관련이 깊은 주제들입니다
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

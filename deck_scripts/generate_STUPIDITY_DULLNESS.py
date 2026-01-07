#!/usr/bin/env python3
"""
예문 생성 스크립트: STUPIDITY_DULLNESS

이 스크립트는 'STUPIDITY_DULLNESS' 덱의 단어들에 대해
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
    "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
    "deck_title": "STUPIDITY_DULLNESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "3afdf279-b3d0-44ae-902d-0e32a4758fdb",
        "word": "Stupid",
        "meaning": "멍청한 (가장 일반적인 비하 표현)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "2f026ce1-d753-4abd-8602-19a2d3acb63d",
        "word": "Dumb",
        "meaning": "바보 같은 (원래는 벙어리의 뜻, 구어체)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "829a7fb7-d088-463f-9f66-1425b1062b0a",
        "word": "Idiotic",
        "meaning": "백치 같은 (매우 멍청한)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "fdeb7842-f42b-41af-884e-cea3ff6ee968",
        "word": "Moronic",
        "meaning": "저능한 (어리석음을 강조하는 모욕)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "cb87abbf-2375-4c15-bdc3-32e0959c465b",
        "word": "Imbecilic",
        "meaning": "천치 같은 (지능이 매우 낮은)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "5974ebc2-f2cd-4bfb-b9eb-9fac531204d9",
        "word": "Foolish",
        "meaning": "어리석은 (지혜롭지 못한 행동)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "ccccae33-fbc7-4e15-b2db-c7b8389f4446",
        "word": "Silly",
        "meaning": "철없는, 바보 같은 (가벼운 어리석음, 장난스러운)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "2fa5a038-d767-45a0-b0f4-9fdfba9c58ce",
        "word": "Ridiculous",
        "meaning": "터무니없는, 웃기는 (말도 안 되게 어리석은)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "0ddd74af-7b47-470b-a88b-e9ce6682820c",
        "word": "Absurd",
        "meaning": "부조리한, 불합리한 (논리에 맞지 않는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "071f08c7-53f9-4754-b01b-9b2f0486d853",
        "word": "Ludicrous",
        "meaning": "우스꽝스러운 (비웃음을 살 만한)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "6826f9c0-51bf-4d44-a180-58027981a8b0",
        "word": "Preposterous",
        "meaning": "가당찮은, 앞뒤가 바뀐 (상식 밖의)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "89cf3ca1-c0f7-46e6-b893-853851aef2dd",
        "word": "Senseless",
        "meaning": "무분별한, 무의미한 (지각없는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "671c8b29-f81c-4c9c-91e9-7cc32440e9cf",
        "word": "Mindless",
        "meaning": "생각 없는 (지성이 필요 없거나 사용 안 함)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "5ae4674a-7878-4a89-9cdd-a4d1c99d4d12",
        "word": "Brainless",
        "meaning": "뇌가 없는 (멍청한) (지능이 없음을 비꼬는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "ac5f7f5b-28d0-49a9-9118-b58aba329c87",
        "word": "Vacuous",
        "meaning": "멍한, 공허한 (지성이 비어 있는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "51239d3f-96ab-4817-8b43-e7f886ab4aee",
        "word": "Vapid",
        "meaning": "흥미롭지 못한, 김빠진 (지적 자극이 없는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "432cf8ed-8198-4d3d-bc1a-9373348117b3",
        "word": "Dense",
        "meaning": "둔한 (이해가 느리고 꽉 막힌)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "8a457d87-8b34-4160-9f63-171e15c7e886",
        "word": "Thick",
        "meaning": "머리가 나쁜 (구어체) (Dense와 유사)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "a5519e62-c5c5-4bee-9fd3-90ceddafb3e7",
        "word": "Slow",
        "meaning": "(이해가) 느린",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "3c40719d-9dd1-4cba-89ea-1194ec8bef6e",
        "word": "Dim",
        "meaning": "흐릿한, 둔한 (똑똑하지 않은)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "1e6b3080-4c7f-480d-a838-04fcc55597b0",
        "word": "Dull",
        "meaning": "둔감한, 우둔한 (예리하지 못한)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "61a36fb2-4410-43e6-8c7a-7357f7192713",
        "word": "Obtuse",
        "meaning": "둔감한 (일부러 이해하려 하지 않는 듯한)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "6e834c63-6cbb-4008-b3f6-9d6ca209aa7c",
        "word": "Unintelligent",
        "meaning": "지능이 낮은 (객관적 묘사)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "3639bf41-7790-472e-a6f2-19e269507a90",
        "word": "Simple-minded",
        "meaning": "단순한 (복잡한 것을 이해 못 하는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "2119d5d8-02f0-4cfa-a201-4de072c2f9b4",
        "word": "Half-witted",
        "meaning": "얼간이 같은 (지능이 모자라는)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "c7944e81-dc7d-433b-a20d-6943bddfef02",
        "word": "Crazy",
        "meaning": "미친, 말도 안 되는",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "63054b58-681b-421e-9aff-beb31be210f8",
        "word": "Insane",
        "meaning": "정신 나간, 비상식적인",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "f4edd8ef-5c55-408c-9ed7-d294e5055155",
        "word": "Mad",
        "meaning": "미친 (화난/정신 이상)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "bacf50d9-565d-447f-904c-4d4620d651b5",
        "word": "Lunatic",
        "meaning": "광적인, 미치광이 같은",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    },
    {
        "card_id": "7cdfcf1e-5571-49c4-80e8-f570fbe856e1",
        "word": "Deranged",
        "meaning": "정신 착란의 (정상이 아닌)",
        "deck_id": "cb1db2e3-81f7-43c0-8168-fe695316b9c7",
        "deck_title": "STUPIDITY_DULLNESS"
    }
]

RELEVANT_TAGS = [
    "place",
    "travel",
    "wellness",
    "restaurant",
    "sad",
    "schedule",
    "health",
    "learning",
    "daily_life",
    "movie"
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
- 위 태그들은 'STUPIDITY_DULLNESS' 덱과 관련이 깊은 주제들입니다
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

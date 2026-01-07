#!/usr/bin/env python3
"""
예문 생성 스크립트: ATTITUDE_TONE

이 스크립트는 'ATTITUDE_TONE' 덱의 단어들에 대해
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
    "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
    "deck_title": "ATTITUDE_TONE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "6e5f306d-dcf5-4d1f-a0b1-b6fdd7a8e5a6",
        "word": "Assertive",
        "meaning": "단호한, 자기주장이 강한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "fa5517bb-378b-4323-a4ed-7753db3f2adb",
        "word": "Polite",
        "meaning": "예의 바른",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "cd81e24c-69ca-4b45-9be4-98c0ae5098ad",
        "word": "Enthusiastic",
        "meaning": "열정적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "b87c515a-f04d-457e-a155-f0ff5c4cc563",
        "word": "Humble",
        "meaning": "겸손한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "20d513c9-e1a9-4b9f-8d68-a300c9249128",
        "word": "Aggressive",
        "meaning": "공격적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "4a05c177-ae0f-44e0-93d3-a94f77591dd9",
        "word": "Condescending",
        "meaning": "거들먹거리는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "dfd1b4b0-75df-4415-b012-8cd7febdafa1",
        "word": "Passive",
        "meaning": "수동적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "2ab67fce-2b63-4127-a99b-56f514d70272",
        "word": "Patronizing",
        "meaning": "가르치려 드는, 생색내는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "e6a7ed6a-5e32-43c6-8a76-56adfc7fdbc8",
        "word": "Defensive",
        "meaning": "방어적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "559b8506-4ea6-4471-8306-7b278a7b915a",
        "word": "Sarcastic",
        "meaning": "빈정대는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "02f9624e-72b8-4a50-8395-c412e166b86d",
        "word": "Haughty",
        "meaning": "거만한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "d5f8afab-c245-45db-b8e6-c9558b4133b7",
        "word": "Insincere",
        "meaning": "가식적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "c3cec62f-f8f5-462f-b890-785aa2135de3",
        "word": "Apathetic",
        "meaning": "무관심한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "44d271e7-6787-47b7-a935-5171fa2d45b3",
        "word": "Arrogant",
        "meaning": "오만한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "d5ccb6d5-1be9-402d-b78b-07666240b865",
        "word": "Rude",
        "meaning": "무례한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "0d7340cd-5608-4c88-be54-dd5c0ad15b29",
        "word": "Flippant",
        "meaning": "경박한, 건방진",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "9092caf0-5aac-4ef1-b222-89ba378b0aa2",
        "word": "Offensive",
        "meaning": "모욕적인, 불쾌한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "4fb18489-344e-47ef-8417-a8300e8849f0",
        "word": "Cynical",
        "meaning": "냉소적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "322c84f6-be0f-4ba9-9a69-4ed154e04ee4",
        "word": "Ironic",
        "meaning": "반어적인, 아이러니한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "58a3c151-be2a-49af-b14b-c3c59cf777d9",
        "word": "Sympathetic",
        "meaning": "동정적인, 공감하는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "9cde290a-0950-4402-92c1-9a71f142136c",
        "word": "Hypocritical",
        "meaning": "위선적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "b3118a72-d84e-46ec-8ee6-79280d1385a4",
        "word": "Empathetic",
        "meaning": "감정이입하는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "f5ed5060-92be-4a20-b6cd-11dddacd4d7d",
        "word": "Hostile",
        "meaning": "적대적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "91ea577f-84be-4980-8a26-572781fac7fb",
        "word": "Friendly",
        "meaning": "우호적인",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "e071f04d-cd01-440d-99fc-a8cc783221d4",
        "word": "Cold",
        "meaning": "차가운",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "6aebb31e-a5e7-4a22-85a0-d4778d04b301",
        "word": "Distant",
        "meaning": "거리감을 두는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "8215771f-5396-46e5-b7d5-565d94e596ab",
        "word": "Indifferent",
        "meaning": "무심한, 관심 없는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "a17c9be1-72bf-42b4-be4e-180954b8f31e",
        "word": "Sincere",
        "meaning": "진심 어린",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "835463b8-2fc7-4388-b802-97dc4bc39923",
        "word": "Earnest",
        "meaning": "성실한, 진지한",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    },
    {
        "card_id": "e89f8ef2-2586-4b1b-9333-20f42cd8dc21",
        "word": "Respectful",
        "meaning": "존중하는",
        "deck_id": "46a54b8c-1737-4c73-9168-f3ccbee2ac2a",
        "deck_title": "ATTITUDE_TONE"
    }
]

RELEVANT_TAGS = [
    "develope",
    "entrepreneur",
    "activity",
    "conversation",
    "vacation",
    "emotion",
    "place",
    "planning",
    "time",
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
- 위 태그들은 'ATTITUDE_TONE' 덱과 관련이 깊은 주제들입니다
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

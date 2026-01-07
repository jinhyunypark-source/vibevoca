#!/usr/bin/env python3
"""
예문 생성 스크립트: FREQUENCY_REPETITION

이 스크립트는 'FREQUENCY_REPETITION' 덱의 단어들에 대해
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
    "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
    "deck_title": "FREQUENCY_REPETITION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "52b44eec-2f6a-4008-adf8-d35ed02d3351",
        "word": "Intermittent",
        "meaning": "간헐적인 (멈췄다 시작했다 하는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "5dbf65e1-a7dd-4282-b298-b391834eec84",
        "word": "Sporadic",
        "meaning": "산발적인 (불규칙하게 드문드문 일어나는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "cb00c9e3-dda6-4345-9df0-a2205ac9e0f3",
        "word": "Occasional",
        "meaning": "가끔의 (자주는 아니지만 때때로)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "5681bf1d-acce-45bd-971d-e66e5573066e",
        "word": "Periodic",
        "meaning": "주기적인 (일정한 간격을 두고 일어나는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "1a0557fe-4715-4179-a2f9-f4bddc6ed418",
        "word": "Recurrent",
        "meaning": "재발하는, 되풀이되는 (자꾸 다시 일어나는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "124f7a88-36a9-4d17-97b8-ef1d07ce59e7",
        "word": "Frequent",
        "meaning": "빈번한 (자주 일어나는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "5d61bbbf-a2f7-492e-87f1-d63693c75237",
        "word": "Constant",
        "meaning": "끊임없는 (변함없이 계속되는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "cb464316-3a69-47e8-91f2-5bff93c3924a",
        "word": "Continual",
        "meaning": "빈번한 (짜증 날 정도로 자꾸 반복되는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "103c673c-ba6a-4dc9-ba9d-f0b445962b3a",
        "word": "Regular",
        "meaning": "규칙적인 (정해진 패턴대로)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "8ddd8cb1-166f-4bee-8607-20e91f3d046a",
        "word": "Irregular",
        "meaning": "불규칙한 (패턴이 없는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "3127fddc-8bc3-4d01-ba91-2e871f91c034",
        "word": "Cyclical",
        "meaning": "순환하는 (주기를 돌며 반복되는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "762a1b18-7889-4a51-ab96-9c8e577be82a",
        "word": "Hourly",
        "meaning": "매 시간의 (1시간마다)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "96003915-2f36-4268-bdb8-5ea2d06db332",
        "word": "Biennial",
        "meaning": "2년마다의 (격년의)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "467158e8-80f8-43be-b7c4-4f758f2ef915",
        "word": "Perennial",
        "meaning": "다년생의, 연중 계속되는 (오랫동안 반복되는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "13f51951-6005-47a9-b4be-a3942a2fe918",
        "word": "Habitual",
        "meaning": "습관적인 (버릇처럼 하는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "164ae243-791f-4c44-992c-405b4760614a",
        "word": "Customary",
        "meaning": "관례적인 (관습에 따라 늘 하는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "d8ab6956-6e7e-4b39-a6ae-66a403f1becd",
        "word": "Routine",
        "meaning": "일상적인 (정해진 순서대로 하는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "73d30fc4-3fda-4c1f-893c-039d6092a437",
        "word": "Systematic",
        "meaning": "체계적인 (계획에 따라 규칙적으로)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "170b20e7-1a31-4b06-bacd-787c12fd0f0e",
        "word": "Alternate",
        "meaning": "번갈아 일어나는 (하나 건너 하나)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "73bd0ba9-3db3-4789-8c1b-6aef77864700",
        "word": "Consecutive",
        "meaning": "연속적인 (중단 없이 연달아)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "7fb62cb2-3b43-4d1f-8f54-37b5db4c8dad",
        "word": "Successive",
        "meaning": "잇따른 (순서대로 이어지는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "f640e070-2990-4869-9c41-252fac569bda",
        "word": "Spasmodic",
        "meaning": "발작적인 (갑자기 확 일어났다 멈추는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "a239f13b-6fde-49de-bc98-002bd61cc459",
        "word": "Fitful",
        "meaning": "자다 깨다 하는, 불규칙한 (잠깐씩 끊기는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "41bcdd11-91ab-43b2-93ad-32655a856897",
        "word": "Rare",
        "meaning": "드문 (자주 일어나지 않는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "5d5803ea-0bad-422c-a1fa-1657d94867aa",
        "word": "Infrequent",
        "meaning": "드문 (빈도가 낮은)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "77fff128-30a2-431a-b049-46f8308b59f4",
        "word": "Seldom",
        "meaning": "좀처럼 ~않는 (거의 없는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "1205b133-17ec-4f81-a152-1738703f3ded",
        "word": "Scarce",
        "meaning": "희귀한, 부족한 (찾아보기 힘든)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "8907ef68-cc2d-46c1-8fee-0d32d887d201",
        "word": "Commonplace",
        "meaning": "흔한 (너무 자주 있어서 평범한)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "7742e73d-573f-47ec-88b7-6dbed4d7466a",
        "word": "Ubiquitous",
        "meaning": "어디에나 있는 (동시에 도처에 존재하는)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    },
    {
        "card_id": "43ecb879-644d-4e27-8723-94b51d97ea2b",
        "word": "Annual",
        "meaning": "매년의 (1년마다)",
        "deck_id": "a6a8346b-9187-43cc-acab-e47e047f984e",
        "deck_title": "FREQUENCY_REPETITION"
    }
]

RELEVANT_TAGS = [
    "daily_life",
    "work",
    "dining",
    "develope",
    "smartphone",
    "education",
    "startup",
    "entertainment",
    "restaurant",
    "journey"
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
- 위 태그들은 'FREQUENCY_REPETITION' 덱과 관련이 깊은 주제들입니다
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

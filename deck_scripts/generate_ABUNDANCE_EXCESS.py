#!/usr/bin/env python3
"""
예문 생성 스크립트: ABUNDANCE_EXCESS

이 스크립트는 'ABUNDANCE_EXCESS' 덱의 단어들에 대해
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
    "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
    "deck_title": "ABUNDANCE_EXCESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "60d090c5-c437-43f9-8d36-6c95be52eccc",
        "word": "Abundant",
        "meaning": "풍부한 (부족함 없이 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "a4710168-9814-4066-b175-53584ebd6127",
        "word": "Plentiful",
        "meaning": "많은, 풍족한 (충분하고 남는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "ce498df1-dce4-4e53-beed-86b24369481b",
        "word": "Ample",
        "meaning": "충분한 (필요한 만큼 넉넉한)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "b3140d21-b371-4d0a-ae4e-0865ade856c6",
        "word": "Bountiful",
        "meaning": "풍성한 (자연이 주는 혜택이 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "5e0af0df-6de0-46b5-8e65-22da2d0615b9",
        "word": "Copious",
        "meaning": "방대한, 엄청난 (양이 아주 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "4c23ad4d-fdb9-4e42-a204-e9c0489aa4f9",
        "word": "Profuse",
        "meaning": "많은, 아낌없는 (쏟아져 나오는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "69cfcc1f-dcf5-4cdc-ae36-648caf871148",
        "word": "Numerous",
        "meaning": "수많은 (개수가 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "f269c759-9e8b-4838-9421-24de8858b558",
        "word": "Countless",
        "meaning": "셀 수 없는 (너무 많아서 셀 수 없는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "8b7d8444-e20d-4c81-8bab-2ece055b850b",
        "word": "Innumerable",
        "meaning": "무수한 (셀 수 없이 많은 - 격식)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "c5ddc3b0-b89f-46a7-beeb-94c1abbb6067",
        "word": "Myriad",
        "meaning": "무수함 (다양하고 엄청나게 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "df57ab7b-0cce-4f15-be67-e76fc58de7ef",
        "word": "Multitude",
        "meaning": "다수 (아주 많은 수/군중)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "dc03e9c9-0aaf-493d-ad15-d29cba48e0c5",
        "word": "Legion",
        "meaning": "아주 많은 (군대처럼 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "cef1663f-a530-4cd9-b750-22bf482fdfd7",
        "word": "Teeming",
        "meaning": "바글거리는 (생물로 가득 찬)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "c1eadf96-8ee1-4ba4-a07b-ce69aee5db04",
        "word": "Overflowing",
        "meaning": "넘쳐흐르는 (용량을 초과한)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "fc540be1-da6e-496d-9625-7331136369d5",
        "word": "Rife",
        "meaning": "(나쁜 것이) 만연한, 가득한",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "9c4863a5-a53c-4938-aa4f-3f712d0e8b8a",
        "word": "Rampant",
        "meaning": "걷잡을 수 없는, 만연한 (잡초처럼 퍼지는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "02322395-c4ee-4f8e-9d1e-e9e18fb33bd3",
        "word": "Excessive",
        "meaning": "과도한 (정도에 지나친)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "130b2973-ab71-4aa5-95bd-1142e4346d49",
        "word": "Superfluous",
        "meaning": "불필요한, 잉여의 (필요 이상으로 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "7524fb92-2c4b-46d7-b1a0-d8d2df98b04d",
        "word": "Surplus",
        "meaning": "잉여, 흑자 (쓰고 남은 것)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "df0fed75-b25f-4d01-8cf0-0e5b51c3a83a",
        "word": "Redundant",
        "meaning": "남아도는, 불필요한 (중복되어 쓸모없는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "722cc6f8-bde3-4a28-bc20-595af484cdef",
        "word": "Lavish",
        "meaning": "호화로운, 아끼지 않는 (풍성하게 쓰는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "4d20133e-bae1-4037-897d-5834d509eed9",
        "word": "Generous",
        "meaning": "후한, 넉넉한 (양을 많이 주는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "f13a8a3f-d81e-419a-9865-9f118a2ec1b6",
        "word": "Rich",
        "meaning": "풍부한 (함유량이 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "d6c5937e-9fbb-427a-b6cd-6d97849b9056",
        "word": "Wealthy",
        "meaning": "부유한 (재산이 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "a83e2b59-0e29-4535-9ecf-388a9aa319d4",
        "word": "Affluent",
        "meaning": "부유한, 풍족한 (돈이 많아 여유로운)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "c8729e9f-2d68-47b3-a884-7cd33544aa32",
        "word": "Opulent",
        "meaning": "엄청나게 부유한 (사치스러운)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "64bc5af4-af65-4aab-8a40-cb4507472a51",
        "word": "Loaded",
        "meaning": "돈이 많은, 꽉 찬 (속어/비유)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "8c4c6f93-3d33-4c3b-8c0b-bc7bd2bc98c7",
        "word": "Flush",
        "meaning": "돈이 두둑한 (일시적으로 풍족한)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "1f830f6d-03e5-44c8-af73-c36308c1706f",
        "word": "Substantial",
        "meaning": "상당한 (양이 꽤 되는)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    },
    {
        "card_id": "a67eebb3-d92a-415d-b3ab-0c497404d7e0",
        "word": "Infinite",
        "meaning": "무한한 (끝없이 많은)",
        "deck_id": "24a5a7c7-41e5-4a4c-82d8-0633b90c5e93",
        "deck_title": "ABUNDANCE_EXCESS"
    }
]

RELEVANT_TAGS = [
    "job",
    "happy",
    "mood",
    "school",
    "smartphone",
    "communication",
    "conversation",
    "style",
    "cooking",
    "marketing"
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
- 위 태그들은 'ABUNDANCE_EXCESS' 덱과 관련이 깊은 주제들입니다
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

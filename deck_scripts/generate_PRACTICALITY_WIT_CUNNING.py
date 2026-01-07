#!/usr/bin/env python3
"""
예문 생성 스크립트: PRACTICALITY_WIT_CUNNING

이 스크립트는 'PRACTICALITY_WIT_CUNNING' 덱의 단어들에 대해
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
    "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
    "deck_title": "PRACTICALITY_WIT_CUNNING",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "ad447435-a133-43bc-8d8e-8d078d84d3b5",
        "word": "Shrewd",
        "meaning": "상황 판단이 빠른, 예리한 (비즈니스적 감각이 좋은)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "dac4c663-d8d9-4022-b2c1-ef37c22f8700",
        "word": "Astute",
        "meaning": "약삭빠른, 빈틈없는 (핵심을 찌르는 판단력)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "ef859532-0ecf-42a0-8099-44cc9622fb6a",
        "word": "Canny",
        "meaning": "영리한, 신중한 (특히 돈/정치 문제에서)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "11247e7a-1f5a-42a2-98cf-a1a9ac1b6f14",
        "word": "Savvy",
        "meaning": "요령 있는, 정통한 (실전 지식이 있는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "c4313180-43aa-48df-997b-0f4958fed11e",
        "word": "Droll",
        "meaning": "익살스러운 (기묘하게 웃긴)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "5292124f-4875-4d6d-904c-76fc0fe54e46",
        "word": "Devious",
        "meaning": "기만적인, 정도를 벗어난 (정직하지 못한 방법으로) de(벗어나) via(방향,길)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "d33ab3da-88ca-4498-a5ee-60606e75500c",
        "word": "Scheming",
        "meaning": "책략을 꾸미는 (음흉한)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "b1654355-43a2-4f3e-8c82-49a21f248512",
        "word": "Sly",
        "meaning": "교활한, 은밀한 (남을 속이는 데 능한)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "8494fc7b-2fd2-4bc2-92cd-eb0918077725",
        "word": "Street-smart",
        "meaning": "세상 물정에 밝은 (학교 공부보다 실전 경험)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "f06c9212-eeaf-4840-a0aa-d713f70b81e2",
        "word": "Sharp",
        "meaning": "빠릿빠릿한 (눈치가 빠르고 셈이 빠른)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "e270280e-d2b4-409e-9b0a-aae32ab23958",
        "word": "Keen",
        "meaning": "예리한, 날카로운 (감각이 살아있는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "fd8c657a-9f82-4f30-91d3-e5c9af050e07",
        "word": "Witty",
        "meaning": "재치 있는 (말을 재미있고 지능적으로 하는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "f56e3506-5b05-493f-a1a4-e55cb4e550bd",
        "word": "Humorous",
        "meaning": "유머러스한 (재미있는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "a38a6cb7-d1b5-4dbb-8ad7-3d8bb06a5aef",
        "word": "Cunning",
        "meaning": "간교한, 교묘한 (목적 달성을 위해 머리를 쓰는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "61d7d33c-d0e2-42a3-849a-42e0590bfc71",
        "word": "Crafty",
        "meaning": "술수가 뛰어난 (손재주나 속임수에 능한)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "e9a6ac0f-f2b7-4aec-aff4-776f186fa1b1",
        "word": "Wily",
        "meaning": "약삭빠른 (계략을 잘 꾸미는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "2b4bdd65-621a-449f-8ebb-053dcc37fb49",
        "word": "Artful",
        "meaning": "기교 부리는, 교묘한 (솜씨 좋게 속이는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "b5d779c5-6dc1-4a27-b5cd-e0bcebd7c342",
        "word": "Manipulative",
        "meaning": "조종하는 (사람을 교묘하게 다루는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "3b1ace0d-4818-400b-b0b5-a8a181c2d2b7",
        "word": "Vigilant",
        "meaning": "방심하지 않는, 라vigilis (깨어있는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "3f2eb4be-ca08-417b-9b8c-8b63fe301620",
        "word": "vigil",
        "meaning": "날밤새다",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "0de39588-ccad-4075-9745-7ae5ce86c7c5",
        "word": "surveil",
        "meaning": "감시하다",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "cb46298d-7652-4fff-a258-fda05b3ab05c",
        "word": "Pragmatic",
        "meaning": "실리적인  (그)pragma행해진일",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "c0942bfb-dcc4-4fc2-a2a4-d3d112eda725",
        "word": "Machiavellian",
        "meaning": "권모술수의 (목적을 위해 수단을 가리지 않는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "db13dd50-7ce1-4fa8-b3af-4c5c4913b925",
        "word": "Practical",
        "meaning": "실용적인, 현실적인 (이론보다 실제)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "3c7361a0-8b7e-4b64-8fc4-11478197a59f",
        "word": "Realistic",
        "meaning": "현실적인 (꿈꾸지 않고 사실을 보는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "aeed643b-8b83-418c-a81f-2714cb0af624",
        "word": "Down-to-earth",
        "meaning": "현실적인, 소탈한 (허황되지 않은)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "2ad7fe37-cd4b-44c5-be58-87fbb07fe37a",
        "word": "Efficient",
        "meaning": "효율적인 (낭비 없이 일 처리하는)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "7570db34-a4f2-404d-92a5-02465b43502d",
        "word": "Quick",
        "meaning": "빠른 (이해나 동작이 빠른)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "4412e778-bf6a-4188-a7a8-194769cc2bab",
        "word": "Alert",
        "meaning": "기민한, 경계하는 (정신이 바짝 든)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    },
    {
        "card_id": "99a25871-65c5-4805-b10f-713374f6b122",
        "word": "Calculated",
        "meaning": "계산적인 (치밀하게 계획된)",
        "deck_id": "4e296a17-9519-4e69-af33-a7eb9e503985",
        "deck_title": "PRACTICALITY_WIT_CUNNING"
    }
]

RELEVANT_TAGS = [
    "startup",
    "ai",
    "code",
    "warm",
    "style",
    "place",
    "mood",
    "schedule",
    "health",
    "technology"
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
- 위 태그들은 'PRACTICALITY_WIT_CUNNING' 덱과 관련이 깊은 주제들입니다
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

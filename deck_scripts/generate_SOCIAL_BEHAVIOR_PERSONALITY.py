#!/usr/bin/env python3
"""
예문 생성 스크립트: SOCIAL_BEHAVIOR_PERSONALITY

이 스크립트는 'SOCIAL_BEHAVIOR_PERSONALITY' 덱의 단어들에 대해
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
    "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
    "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "ea34cf8d-6b52-4694-b55a-a69fbdc9adeb",
        "word": "Sociable",
        "meaning": "사교적인 (사람들과 어울리기 좋아하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "f9603c8c-25d1-40c8-bea5-5ebe31183487",
        "word": "Gregarious",
        "meaning": "남과 어울리기 좋아하는 (군집 본능이 강한)   (라)*grex 군집*",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "02439463-aa45-43f3-8c69-87b77b03ea52",
        "word": "*greg*",
        "meaning": "무리",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "ecaa8fba-fa38-4db0-9e77-df4fd1045d4b",
        "word": "egregious",
        "meaning": "e(바깥) +gregious(무리)무리 밖에 있는 , 악명높은,",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "0c80ff13-9d9b-46c4-ae05-a0bb7fb4ef8f",
        "word": "Outgoing",
        "meaning": "외향적인 (활달하고 나서는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "0732a7c4-2c3d-4c9e-a8b8-d87164d5a700",
        "word": "Extroverted",
        "meaning": "외향적인 (에너지를 밖으로 발산하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "b211f2c8-5781-4766-b4e8-511645ceb283",
        "word": "Introverted",
        "meaning": "내향적인 (에너지를 안으로 갈무리하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "6562ad4a-7b1e-44ed-9a3f-2d06b811b5cf",
        "word": "Charismatic",
        "meaning": "카리스마 있는 (사람을 끌어당기는 매력)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "951b0243-0500-4a1a-9529-60e72c840828",
        "word": "Charming",
        "meaning": "매력적인 (사람의 마음을 사는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "42d3c04a-b5ef-4a5e-9a73-2564ea8d8dbb",
        "word": "Likable",
        "meaning": "호감 가는 (누구나 좋아하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "33ecdbc0-0a12-4f46-88c2-577f800fd179",
        "word": "Popular",
        "meaning": "인기 있는 (많은 사람이 좋아하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "84791b2e-cadd-49bd-af23-298c95d37263",
        "word": "Altruistic",
        "meaning": "이타적인 (남을 위해 희생하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "3732cdb4-2031-458f-9ca6-59f47ae4854b",
        "word": "Approachable",
        "meaning": "다가가기 쉬운 (말 걸기 편한)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "e331296a-b8fc-4bf4-b596-c34e35f75c0d",
        "word": "Accessible",
        "meaning": "접근 가능한 (쉽게 만날 수 있는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "ae05f45b-a31b-481a-aa66-2ca898214094",
        "word": "Welcoming",
        "meaning": "환대하는 (반갑게 맞아주는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "865b64b2-8626-4046-9677-68d08400528c",
        "word": "Hospitable",
        "meaning": "손님을 잘 대접하는 (후한 대접)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "b7c21305-bba3-4469-98bb-4a7e2625ffec",
        "word": "Generous",
        "meaning": "관대한, 베푸는 (잘 나누어 주는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "f277166c-98bd-4143-8a18-b8c15ed28ed8",
        "word": "Selfish",
        "meaning": "이기적인 (자기만 아는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "1770b90e-9e40-45cb-879e-f6359cdabbc5",
        "word": "Egocentric",
        "meaning": "자기중심적인 (세상이 자기를 중심으로 도는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "2c920c14-de70-488f-8e0c-7d54013f3ce0",
        "word": "Narcissistic",
        "meaning": "자아도취적인 (자기를 너무 사랑하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "d13f6389-3ab5-4740-9bff-c7a2183b67ae",
        "word": "Arrogant",
        "meaning": "오만한 (남을 깔보는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "44763a01-96dc-4fe3-8554-d317213b1754",
        "word": "Humble",
        "meaning": "겸손한 (자기를 낮추는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "92489897-eebb-47c5-b815-2a64cfbb89e3",
        "word": "Modest",
        "meaning": "겸손한, 수수한 (자랑하지 않는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "80a71bc8-d657-404f-9fe4-dfeea791f725",
        "word": "Shy",
        "meaning": "수줍음 타는 (낯을 가리는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "ef71e9f1-b84a-43e1-8ae2-01e318a41de8",
        "word": "Timid",
        "meaning": "소심한 (겁이 많고 자신감 없는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "a59a6ef2-0b15-463b-ab5e-aede948a783d",
        "word": "Bashful",
        "meaning": "부끄럼 타는 (칭찬받으면 수줍어하는)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "b3b72041-af6c-4bd4-b174-5edee3ee89c7",
        "word": "Awkward",
        "meaning": "어색한 (사교적으로 서투른)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "909cf2e0-d98f-4c2d-ad23-3b17c0a31560",
        "word": "Socially awkward",
        "meaning": "사회성이 부족한 (눈치가 없거나 서툰)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "b2896882-4741-43be-8a44-c0b90b95b161",
        "word": "Confident",
        "meaning": "자신감 있는 (당당한)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    },
    {
        "card_id": "81c13518-ba01-45e3-81fd-b258928e40d3",
        "word": "Assertive",
        "meaning": "자기주장이 뚜렷한 (단호한)",
        "deck_id": "add69933-3065-4146-9a6b-ecbc8204b20a",
        "deck_title": "SOCIAL_BEHAVIOR_PERSONALITY"
    }
]

RELEVANT_TAGS = [
    "dining",
    "place",
    "sad",
    "medical",
    "time",
    "mood",
    "activity",
    "relationship",
    "meeting",
    "sport"
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
- 위 태그들은 'SOCIAL_BEHAVIOR_PERSONALITY' 덱과 관련이 깊은 주제들입니다
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

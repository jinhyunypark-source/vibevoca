#!/usr/bin/env python3
"""
예문 생성 스크립트: ENORMOUSNESS_VASTNESS

이 스크립트는 'ENORMOUSNESS_VASTNESS' 덱의 단어들에 대해
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
    "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
    "deck_title": "ENORMOUSNESS_VASTNESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d095f881-d1b8-4c98-a079-31ae25f625d6",
        "word": "Colossal",
        "meaning": "거대한 (동상이나 건축물처럼 압도적인)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "3312c131-ff1d-44da-9d2b-b2e839cb8815",
        "word": "Enormous",
        "meaning": "막대한, 거대한 (일반적으로 매우 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "0ac68385-c107-4a6c-9ec7-f663140819e6",
        "word": "Gigantic",
        "meaning": "장대한, 거인 같은 (자이언트처럼 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "5b55bf25-9631-4cf2-9a47-90a0bda2bbb4",
        "word": "Massive",
        "meaning": "육중한, 대규모의 (무겁고 꽉 찬 느낌)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "421f1add-f87e-45f6-9319-b6112d4264e5",
        "word": "Vast",
        "meaning": "광활한, 어마어마한 (넓게 펼쳐진 면적/범위)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "ed0545bc-6c66-4ed6-a6f6-54f7ed8c77b5",
        "word": "Immense",
        "meaning": "헤아릴 수 없는, 광대한 (측정하기 힘들 만큼 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "7902eda8-f30e-4525-bb34-b3d22eb83fd6",
        "word": "Huge",
        "meaning": "거대한 (가장 일반적으로 쓰이는 큰 크기)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "7ec2a153-75a1-4da9-8a20-cd947c4ed6d2",
        "word": "Mammoth",
        "meaning": "매머드 같은, 거대한 (일이 어렵고 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "76315f49-2ace-4515-9811-102d1dfd18ea",
        "word": "Titanic",
        "meaning": "타이타닉 같은, 엄청난 (힘이나 규모가 거대한)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "ac44091b-0184-4c15-8fa6-25d107dd8d76",
        "word": "Monumental",
        "meaning": "기념비적인, 대단한 (역사에 남을 만큼 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "3a5c6aa6-2caf-4cee-bec2-f1e33ad04fb1",
        "word": "Gargantuan",
        "meaning": "엄청난, 거대한 (식욕이나 부피가 비현실적으로 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "bafe3288-78d8-460c-b7bf-4c5cc2fddf2e",
        "word": "Tremendous",
        "meaning": "엄청난, 대단한 (강도나 양이 놀라울 정도인)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "24094a0e-b884-43c0-8d84-826ee59d44dc",
        "word": "Substantial",
        "meaning": "상당한, 실질적인 (양이 꽤 되고 튼튼한)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "915e1bcc-ec06-4ae6-8a71-6ab0649097d8",
        "word": "Expansive",
        "meaning": "탁 트인, 광범위한 (넓게 뻗어나가는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "6c202c43-89e7-438d-b83e-4d5b5f7b67d3",
        "word": "Extensive",
        "meaning": "광범위한, 대규모의 (넓은 범위에 걸친)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "a0b7fa47-d588-4cf5-9bb5-1b426ada9a94",
        "word": "Broad",
        "meaning": "폭넓은 (가로로 넓은)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "b479d165-b02b-4b52-bdad-95585b569cec",
        "word": "Wide",
        "meaning": "넓은 (폭이 넓은)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "d42df35d-6df4-452c-877d-5c95524fd5a7",
        "word": "Towering",
        "meaning": "우뚝 솟은 (높이가 압도적인)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "e5304512-0bf3-4060-8d46-317809df0ddb",
        "word": "Soaring",
        "meaning": "치솟는 (높이 올라가는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "de7846a3-278d-45d3-b9e8-efaa51a29451",
        "word": "Lofty",
        "meaning": "아주 높은, 고귀한 (높이와 품위가 있는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "4dc7ca3b-669d-4195-a2bf-6c76fef08977",
        "word": "Bulky",
        "meaning": "부피가 큰 (자리를 많이 차지하는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "1820fcea-63e5-44e7-93f8-a177cd0b5cab",
        "word": "Voluminous",
        "meaning": "방대한, 헐렁한 (천이 많이 들거나 양이 많은)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "7f982e3a-5520-4a32-9ef0-216461f62206",
        "word": "Hefty",
        "meaning": "두둑한, 무거운 (무게나 액수가 상당한)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "0799a0b7-e5ec-420e-861f-5bfd921f4a9d",
        "word": "Astronomical",
        "meaning": "천문학적인 (숫자가 상상 초월로 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "40f841e3-620b-4a9d-b583-d3957ac804ef",
        "word": "Infinite",
        "meaning": "무한한 (끝이 없는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "20546944-38e5-4e53-bca4-9e0a9fe8d969",
        "word": "Limitless",
        "meaning": "한계가 없는 (제한이 없는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "f107bf44-1734-4c62-b767-8baaaf06bb36",
        "word": "Boundless",
        "meaning": "끝없는 (경계가 없는)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "4f06c060-2961-4692-92bf-7f7d3ac94b0f",
        "word": "Grand",
        "meaning": "웅장한 (규모가 크고 화려한)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "f59982b2-fe45-489f-86e9-c2ba83eadf10",
        "word": "Majestic",
        "meaning": "장엄한 (위엄 있고 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    },
    {
        "card_id": "f021edd8-faea-4a37-96df-d6e31ce0f927",
        "word": "Prodigious",
        "meaning": "엄청난, 경이로운 (놀라울 정도로 큰)",
        "deck_id": "e713ce9e-9c95-45c6-b3c6-0b863963c4f1",
        "deck_title": "ENORMOUSNESS_VASTNESS"
    }
]

RELEVANT_TAGS = [
    "health",
    "marketing",
    "environment",
    "exercise",
    "entrepreneur",
    "restaurant",
    "internet",
    "social",
    "hot",
    "place"
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
- 위 태그들은 'ENORMOUSNESS_VASTNESS' 덱과 관련이 깊은 주제들입니다
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

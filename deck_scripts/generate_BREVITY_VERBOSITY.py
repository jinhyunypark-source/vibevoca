#!/usr/bin/env python3
"""
예문 생성 스크립트: BREVITY_VERBOSITY

이 스크립트는 'BREVITY_VERBOSITY' 덱의 단어들에 대해
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
    "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
    "deck_title": "BREVITY_VERBOSITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "486d65ca-383e-4570-8c3f-4bbf715a243a",
        "word": "Concise",
        "meaning": "간결한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "9aa0dee5-6fe3-42ee-bdc3-681432bdefba",
        "word": "Brief",
        "meaning": "짧은, 잠시의",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "fe75bdfd-fecf-449c-b744-6a1dc81e2270",
        "word": "Succinct",
        "meaning": "간단명료한  cinch",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "dbde9c12-db0a-42d4-b303-e164815ef35d",
        "word": "Laconic",
        "meaning": "과묵한, 말수가 적은",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "be2177c7-235d-45ba-8cb7-8123d5385653",
        "word": "Reticent",
        "meaning": "말을 아끼는 (신중함)",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "7bb839fb-3dbc-423c-82ad-a64c1ee2ba4c",
        "word": "Taciturn",
        "meaning": "무뚝뚝한, 말이 없는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "5ac7b802-b763-49b5-9281-a3798af2249f",
        "word": "tacit [tǽsit]",
        "meaning": "무언의",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "a3bf5661-bb9a-4906-af8b-aa7073c7a38f",
        "word": "Pithy",
        "meaning": "함축적인, 핵심을 찌르는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "71683d26-2fe6-49ee-b4de-e05cfc0b373f",
        "word": "Wordy",
        "meaning": "말이 많은, 너저분한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "5d9848da-9863-49ab-80ae-e4dfc81c5a4e",
        "word": "Terse",
        "meaning": "(퉁명스럽게) 간결한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "698df5f7-7713-43c1-bbca-54dda9f715da",
        "word": "Loquacious",
        "meaning": "수다스러운 (격식)라.Loqui말하다",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "16d8da2f-9a70-46d9-b8c9-1264d8202207",
        "word": "Verbose",
        "meaning": "장황한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "6c0228cf-44c5-4d75-89e1-91f85dd8faf5",
        "word": "Long-winded",
        "meaning": "길게 늘어놓는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "98e88d13-6e94-4e9b-bab7-bea82e182f05",
        "word": "Garrulous",
        "meaning": "주책없이 수다스러운 (갈갈이)",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "f2eb1835-8086-48e8-bbaf-347128eb32e8",
        "word": "Comprehensive",
        "meaning": "포괄적인",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "745186b8-070f-45f3-a3ef-f0e45bab2e25",
        "word": "Chatty",
        "meaning": "수다 떠는, 잡담하는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "a3661352-521d-444b-ab8c-a79b05948a48",
        "word": "Talkative",
        "meaning": "말하기 좋아하는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "676b4789-559f-4810-856c-496c75cff641",
        "word": "Silent",
        "meaning": "침묵하는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "f0b56988-d1ef-40e1-9f23-29ed75fe8ad9",
        "word": "Detailed",
        "meaning": "상세한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "c029d3e4-a344-4e35-8c9a-fa23c6b14bf1",
        "word": "Elaborate",
        "meaning": "상세히 설명하다",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "df30aece-146f-459d-afbf-8eba674589ba",
        "word": "Exhaustive",
        "meaning": "철저한, 남김없는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "b5f83605-5849-4119-b304-152b4e03cb56",
        "word": "Sketchy",
        "meaning": "대략적인, 불완전한",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "d3e25fe5-bbab-47e2-a83a-6785d387b916",
        "word": "Summarized",
        "meaning": "요약된",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "c4b941d0-0605-450b-899f-6503af6bc884",
        "word": "Abbreviated",
        "meaning": "축약된",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "8699b088-a527-4d3f-9ab4-bc088d7f07e5",
        "word": "Redundant",
        "meaning": "불필요하게 중복되는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "4a80de19-aace-4383-8d60-769586777d08",
        "word": "Meandering",
        "meaning": "두서없는, 정처 없는 (터키의 구불강)",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "5cd10bc9-914c-47e0-bda5-f443b01dda5a",
        "word": "Repetitive",
        "meaning": "반복적인",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "9238ae66-adb9-4ff3-ad47-b4a3d781c0a1",
        "word": "Digressive",
        "meaning": "주제를 벗어나는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "0f3dd96a-716e-420e-8051-1446eea7a165",
        "word": "To the point",
        "meaning": "핵심을 찌르는",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    },
    {
        "card_id": "351a11c6-1acc-4802-aa54-de8c92ece3ca",
        "word": "Curt",
        "meaning": "퉁명스러운",
        "deck_id": "c3412b9e-a009-4a66-aa8e-5a47a15fc60f",
        "deck_title": "BREVITY_VERBOSITY"
    }
]

RELEVANT_TAGS = [
    "place",
    "travel",
    "marketing",
    "exercise",
    "emotion",
    "fashion",
    "feeling",
    "university",
    "friendship",
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
- 위 태그들은 'BREVITY_VERBOSITY' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: POVERTY_HARDSHIP

이 스크립트는 'POVERTY_HARDSHIP' 덱의 단어들에 대해
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
    "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
    "deck_title": "POVERTY_HARDSHIP",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "32440480-38bb-4a82-b6e8-79e08e860b52",
        "word": "Poor",
        "meaning": "가난한 (일반적인 표현)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "11e81b38-962f-4d6a-a163-da231e6036ac",
        "word": "Destitute",
        "meaning": "극빈한 (가진 것이 아무것도 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "0761448e-08a4-4419-aa2b-57f116239aa8",
        "word": "Impoverished",
        "meaning": "빈곤해진 (가난하게 된/열악한)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "d87d9e7c-7d4b-4f61-a439-62516fa07b2d",
        "word": "Indigent",
        "meaning": "곤궁한 (생필품이 부족한 - 격식)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "ca52ceb1-f1df-4511-8dcc-fe0731f961f6",
        "word": "Needy",
        "meaning": "어려운, 궁핍한 (도움이 필요한)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "b1a75040-b2f3-4ca6-b25f-bf46b3a688ea",
        "word": "Penniless",
        "meaning": "무일푼의 (동전 한 푼 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "1d9bff36-08cb-4bbb-8f7f-917cb69928e6",
        "word": "Broke",
        "meaning": "빈털터리인 (돈이 다 떨어진 - 구어체)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "8055034e-e358-4080-a1e9-54878015ffb0",
        "word": "Deprived",
        "meaning": "궁핍한, 불우한 (필수적인 것을 못 누리는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "df95b2fc-f14d-4b18-ac7a-ba62034e9bfa",
        "word": "Bankrupt",
        "meaning": "파산한 (법적으로 빚을 갚을 수 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "c5867c0c-9419-45bf-952e-966c4c06a1e1",
        "word": "Insolvent",
        "meaning": "지불 불능의 (빚이 자산보다 많은)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "b0c50161-8495-4b84-a4e2-f09679820df3",
        "word": "Bust",
        "meaning": "파산한 (망한 - 구어체)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "c91c066e-e846-4576-a99d-00b8d0248a47",
        "word": "In debt",
        "meaning": "빚을 진",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "f5912933-f0cd-4f86-9206-1e1c4f20d99d",
        "word": "Hard up",
        "meaning": "돈에 쪼들리는 (돈이 부족한)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "1ab74049-b62a-40ae-b215-03ec878ef966",
        "word": "Strapped",
        "meaning": "돈이 궁한 (현금이 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "e13c0718-202c-4c6e-8334-444820677844",
        "word": "Short",
        "meaning": "부족한 (돈이 모자라는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "dda59643-1b73-44a7-8d0f-8b14bf8c0db0",
        "word": "Pinched",
        "meaning": "쪼들리는 (경제적으로 압박받는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "e9e083b1-96aa-42b4-a32e-1d6f686a1734",
        "word": "Squalid",
        "meaning": "지저분한, 불결한 (가난으로 더러운)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "f0ba6aa1-3bbe-4537-8d9f-0fa1e000f0f3",
        "word": "Underprivileged",
        "meaning": "혜택 받지 못한 (사회적/경제적으로 낮은)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "a2975127-152d-42f8-aea5-0c9c3b794900",
        "word": "Low-income",
        "meaning": "저소득의 (수입이 적은)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "e167b5bd-7768-4f50-b5b1-2cb13107b014",
        "word": "Subsistence",
        "meaning": "최저 생계의 (겨우 먹고사는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "35ab2162-012b-49fb-a216-ff203867bc32",
        "word": "Hand-to-mouth",
        "meaning": "하루 벌어 하루 먹는 (저축 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "8ee477c8-5463-4fc0-a64b-4cd87684b604",
        "word": "Penury",
        "meaning": "극빈 (지독한 가난 - 명사)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "72eaedd3-e299-4fa0-9024-f7601d174485",
        "word": "Pauper",
        "meaning": "빈민, 극빈자 (거지)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "9f6c13bf-6c10-4abc-9ad5-99c53c03c9c2",
        "word": "Beggar",
        "meaning": "거지 (구걸하는 사람)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "947715b9-cfdc-4b11-a040-b1a1b08c17c5",
        "word": "Hardship",
        "meaning": "곤란, 고난 (경제적 어려움)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "e4d66399-d333-45f0-abf4-afffb5360064",
        "word": "Adversity",
        "meaning": "역경 (불운과 어려움)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "7b1433f6-94f5-421f-8741-084637e0b09e",
        "word": "Default",
        "meaning": "채무 불이행 (빚을 못 갚음)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "ebbd77e6-1723-425a-9709-1e76d959908c",
        "word": "Ruined",
        "meaning": "파산한, 망한 (완전히 무너진)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "f5f32aed-36a7-40a3-9ac9-5552c1a65e34",
        "word": "Tight",
        "meaning": "빠듯한 (여유가 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    },
    {
        "card_id": "20eff885-0a43-4b38-a4c9-b241769541fb",
        "word": "Skint",
        "meaning": "빈털터리인 (영국 속어: 돈이 없는)",
        "deck_id": "48370bd5-3dbc-4ea5-a905-0acfb089b4a1",
        "deck_title": "POVERTY_HARDSHIP"
    }
]

RELEVANT_TAGS = [
    "daily_life",
    "health",
    "emotion",
    "university",
    "vacation",
    "entrepreneur",
    "career",
    "conversation",
    "ai",
    "style"
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
- 위 태그들은 'POVERTY_HARDSHIP' 덱과 관련이 깊은 주제들입니다
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

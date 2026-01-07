#!/usr/bin/env python3
"""
예문 생성 스크립트: SCOPE_COMPREHENSIVENESS

이 스크립트는 'SCOPE_COMPREHENSIVENESS' 덱의 단어들에 대해
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
    "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
    "deck_title": "SCOPE_COMPREHENSIVENESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "87fbe6e0-3657-49f3-95b8-ae3fcf6c7b66",
        "word": "Scope",
        "meaning": "범위, 여지 (다루는 영역)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "8d3190ff-58a3-4ea5-bc72-adbdf1757113",
        "word": "Range",
        "meaning": "범위, 다양성 (A에서 B까지의 폭)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "6732c58c-af9d-4e48-8e50-c3a8d92d13a2",
        "word": "Extent",
        "meaning": "정도, 규모 (미치는 크기)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "c3fb5e9e-2369-422b-8292-c8e85b63c119",
        "word": "Degree",
        "meaning": "정도, 도 (수준이나 단계)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "a44a5a03-4239-4ab2-ad1e-63cd5f1dd8e2",
        "word": "Scale",
        "meaning": "규모, 등급 (비율이나 크기)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "d8b965a3-c27d-4f26-9174-ff3e76cfe415",
        "word": "Magnitude",
        "meaning": "규모, 진도 (거대함이나 중요도)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "a2a77289-321a-4f0a-846b-4624b84bc446",
        "word": "Dimension",
        "meaning": "차원, 관점 (크기나 치수)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "b04cab80-4b11-44e0-9899-f08a39786de2",
        "word": "Area",
        "meaning": "면적, 지역, 분야",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "d3750283-0823-4baf-8ea0-3859e9681f28",
        "word": "Realm",
        "meaning": "영역, 왕국 (활동이나 관심의 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "24b02292-89dc-419c-a317-0733014bd02d",
        "word": "Domain",
        "meaning": "영역, 소유지 (지배하거나 관리하는 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "9a956914-4769-4f80-a8a0-a9f97498100f",
        "word": "Sphere",
        "meaning": "구, 영역 (영향력이 미치는 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "99396285-960a-4c02-963a-e2bf4fb2c725",
        "word": "Horizon",
        "meaning": "지평선, 시야 (인식이나 지식의 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "e9f52497-d43e-4420-a473-b33401e8c8cc",
        "word": "Coverage",
        "meaning": "보도, 적용 범위 (포함하는 정도)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "ff63ff49-c107-440a-9c97-e9aa1dd27957",
        "word": "Comprehensive",
        "meaning": "포괄적인, 종합적인 (모든 것을 다루는)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "648b0a98-d256-4344-bd61-31d22fd431b9",
        "word": "Inclusive",
        "meaning": "포괄적인 (빠짐없이 포함하는)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "1e4cca1c-2763-4623-9930-3a80fdc162b6",
        "word": "Universal",
        "meaning": "보편적인, 전 세계적인 (모두에게 해당하는)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "d52fa483-22f1-42b5-ae34-56d29cdf9c4e",
        "word": "Global",
        "meaning": "지구의, 전반적인 (전체에 걸친)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "d440977c-854c-470b-8c4e-b6d2e9a19119",
        "word": "Total",
        "meaning": "총, 전체의 (합계의)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "6e6b2c58-9f4f-4803-a876-1c2c77f6c0a0",
        "word": "Whole",
        "meaning": "전체의 (빠진 것 없는)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "c2b8c14f-699f-4160-88f6-00eb5e969eaa",
        "word": "Entire",
        "meaning": "내내, 전체의 (처음부터 끝까지)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "dab2ebb3-ac72-49b0-b6bc-9ab0de6ff7cc",
        "word": "Complete",
        "meaning": "완전한 (부족함 없는)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "43357910-ce43-45a3-a1a6-7d11e9ad633e",
        "word": "Partial",
        "meaning": "부분적인 (전체가 아닌)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "b0c77dda-34cf-41f7-b0fd-60d51c8ce286",
        "word": "Segment",
        "meaning": "조각, 부분 (나뉘어진 한 부분)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "0978088a-3505-4e32-854c-9225ecc25e7b",
        "word": "Fraction",
        "meaning": "일부, 파편 (아주 작은 부분)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "2239942e-c88c-4d5d-9439-b97f521f37db",
        "word": "Portion",
        "meaning": "몫, 인분 (할당된 부분)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "f9f45808-9fe8-4ef3-bd09-fe8cd3ae797e",
        "word": "Span",
        "meaning": "기간, 폭 (걸쳐 있는 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "580a456f-11ae-4168-8b04-583cc58eb048",
        "word": "Stretch",
        "meaning": "구간, 뻗음 (펼쳐진 범위)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "bd516e3d-ec5a-44f3-b343-219914c161a5",
        "word": "Reach",
        "meaning": "범위, 거리 (손이 닿는 곳)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "e42b1ad8-1d57-41d9-a58d-558411099fb3",
        "word": "Breadth",
        "meaning": "폭, 넓이 (지식 등의 넓이)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    },
    {
        "card_id": "459f6b98-298d-448b-9f3a-af416ac3cda9",
        "word": "Spectrum",
        "meaning": "스펙트럼, 범위 (양극단 사이의 분포)",
        "deck_id": "6a95738f-4eeb-4021-99c6-3e8c662ef956",
        "deck_title": "SCOPE_COMPREHENSIVENESS"
    }
]

RELEVANT_TAGS = [
    "nature",
    "work",
    "learning",
    "internet",
    "food",
    "medical",
    "activity",
    "develope",
    "social",
    "warm"
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
- 위 태그들은 'SCOPE_COMPREHENSIVENESS' 덱과 관련이 깊은 주제들입니다
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

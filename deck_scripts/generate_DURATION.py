#!/usr/bin/env python3
"""
예문 생성 스크립트: DURATION

이 스크립트는 'DURATION' 덱의 단어들에 대해
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
    "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
    "deck_title": "DURATION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d3bb3b57-fe7a-43fc-94f6-5f1afaf99b60",
        "word": "Chronological",
        "meaning": "연대순의 (시간 순서대로)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "f729af84-fd87-4779-8e24-ba8c138406f3",
        "word": "Sequential",
        "meaning": "순차적인 (논리적 순서에 따른)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "940ca70a-9614-4c82-83ab-9a2b5cccd610",
        "word": "Subsequent",
        "meaning": "그 다음의, 차후의 (뒤에 일어나는)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "b26f0487-af7b-4373-83ac-2f5c5cffbca9",
        "word": "Preceding",
        "meaning": "이전의, 선행하는 (앞서 일어난)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "f78997c5-f099-476a-9b4d-1404c7825143",
        "word": "Prior",
        "meaning": "사전의, 이전의 (더 중요한/먼저인)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "93e836f7-cdd2-40d7-a819-8aabbe1b8d79",
        "word": "Anterior",
        "meaning": "앞쪽의, 이전의 (격식: 앞선)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "506de5c8-a5dd-4d33-b7f0-0674682a5964",
        "word": "Posterior",
        "meaning": "뒤쪽의, 이후의 (격식: 뒤에 오는)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "4b0315eb-5e89-49c7-af6d-3a8bdad684bf",
        "word": "Simultaneous",
        "meaning": "동시의 (같은 시간에)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "6c948d55-786a-4e71-a30c-406a3b76a225",
        "word": "Concurrent",
        "meaning": "동시에 발생하는, 공존하는 (함께 진행되는)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "bea30afd-d684-4709-a060-dd31f34a07e7",
        "word": "Era",
        "meaning": "시대 (특정 사건/인물이 지배하는 시기)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "e9104934-f632-43e3-af8c-f69c718adf91",
        "word": "Epoch",
        "meaning": "시대 (역사의 획을 긋는 중요한 시기)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "6e8cd29a-1a56-45d8-b784-541fb83189e2",
        "word": "Eon",
        "meaning": "억겁, 매우 긴 시간 (지질학적 시대)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "2915381d-93a9-46ea-8455-e4935e28f57a",
        "word": "Millennium",
        "meaning": "천년 (1000년의 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "d124dee8-bcee-4687-8d7f-840699b2580f",
        "word": "Century",
        "meaning": "세기 (100년의 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "70249a83-6cf8-4150-a736-30abd9f4c01b",
        "word": "Decade",
        "meaning": "10년 (10년의 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "e59b3f93-52ad-468f-9ce1-26cf08e7c0b8",
        "word": "Generation",
        "meaning": "세대 (약 30년)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "22e3ca51-e16b-4106-9803-ea8a4b98407a",
        "word": "Dynasty",
        "meaning": "왕조, 명문가 (대가 이어지는 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "0beb06bc-dd90-4b30-8457-bcfb321a792e",
        "word": "Period",
        "meaning": "기간, 시기 (일정한 시간의 구분)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "df2028be-b2c6-4720-8eb2-1371d0b724b4",
        "word": "Phase",
        "meaning": "단계, 국면 (변화의 한 과정)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "88d25f4e-a551-4577-83aa-123afab7e339",
        "word": "Stage",
        "meaning": "단계, 무대 (진행 과정의 한 부분)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "4e701583-9e97-435d-8121-064236fd7835",
        "word": "Interim",
        "meaning": "중간의, 잠정적인 (사이의 시간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "309e1c45-acad-4e7c-88ae-c61da5106afa",
        "word": "Interval",
        "meaning": "간격 (두 사건 사이의 시간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "444c3722-633c-43c2-9ec5-eec0ee498f72",
        "word": "Gap",
        "meaning": "공백, 차이 (빈 시간이나 격차)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "a8971da2-13b1-49ab-aaca-6c494f4d0cbd",
        "word": "Hiatus",
        "meaning": "중단, 공백기 (활동을 잠시 멈춤)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "752ec473-a0ea-47c2-a9ce-2f9284df3a62",
        "word": "Lull",
        "meaning": "소강상태 (잠잠해진 시기)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "03edc454-3d8c-4b8e-adae-1c0fc6bf8790",
        "word": "Respite",
        "meaning": "유예, 일시적 중단 (고통이 멈춘 휴식)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "d2d05e22-5dfd-4532-9283-38acdbe6252a",
        "word": "Tenure",
        "meaning": "재임 기간 (직위에 있는 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "7cabd16e-3309-4a13-b643-34b1bfcfa4c9",
        "word": "Term",
        "meaning": "임기, 학기 (정해진 기간)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "c259faea-a054-4ed5-b465-ac3933396cdc",
        "word": "Duration",
        "meaning": "지속 기간 (계속되는 동안)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    },
    {
        "card_id": "0e052f16-9e6c-442d-99f6-31ea37a58d0d",
        "word": "Span",
        "meaning": "기간, 폭 (걸쳐 있는 범위)",
        "deck_id": "29cfff6b-aa4e-483c-9e85-4f4d470b16da",
        "deck_title": "DURATION"
    }
]

RELEVANT_TAGS = [
    "journey",
    "health",
    "travel",
    "planning",
    "soccer",
    "university",
    "develope",
    "style",
    "restaurant",
    "vacation"
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
- 위 태그들은 'DURATION' 덱과 관련이 깊은 주제들입니다
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

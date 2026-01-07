#!/usr/bin/env python3
"""
예문 생성 스크립트: TIMELINESS_FUTURE_PAST

이 스크립트는 'TIMELINESS_FUTURE_PAST' 덱의 단어들에 대해
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
    "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
    "deck_title": "TIMELINESS_FUTURE_PAST",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "806133bf-b41e-4f9e-a5e8-3ead7e2e4296",
        "word": "Contemporary",
        "meaning": "동시대의, 현대의 (같은 시기/최신)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "293bff53-494a-4140-a4aa-20449fbdd7f1",
        "word": "Modern",
        "meaning": "현대의, 근대의 (과거와 대비되는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "d7fa99cd-4732-479a-931d-9f3645840e92",
        "word": "Current",
        "meaning": "현재의, 통용되는 (지금 일어나고 있는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "ea2a8a78-8963-44da-bf88-db55e807a249",
        "word": "Present-day",
        "meaning": "오늘날의 (지금 이 시대의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "eba4f2fa-bc92-4251-8f63-0263e6dca3b0",
        "word": "Ancient",
        "meaning": "고대의 (아주 먼 옛날의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "8ad0715c-358e-49e9-9eca-f303410e2dab",
        "word": "Archaic",
        "meaning": "고풍의, 낡은 (너무 오래되어 안 쓰는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "bab3e8d6-d7ec-4e19-b8ba-1a0ae5cf2b5b",
        "word": "Primitive",
        "meaning": "원시적인 (초기 단계의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "97be838e-5da8-4e74-ba8c-378ae87dbd85",
        "word": "Primeval",
        "meaning": "태고의, 원시의 (세상 시작 때의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "a6eb5d55-fa7c-40b8-80f4-f80e87816d08",
        "word": "Medieval",
        "meaning": "중세의 (옛날 방식의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "868995a8-2a9f-4075-9375-34f90edd477d",
        "word": "Prehistoric",
        "meaning": "선사 시대의 (역사 기록 이전의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "d1d63340-abaa-4c1f-9849-f94862aa6817",
        "word": "Future",
        "meaning": "미래의 (앞으로 올)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "1c5a5a5a-e854-4ac4-93b6-3f0ea902498b",
        "word": "Prospective",
        "meaning": "장래의, 유망한 (앞으로 될 가능성이 있는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "e48c39fb-c2e9-40c3-8caa-b8c18a2ba135",
        "word": "Imminent",
        "meaning": "임박한, 일촉즉발의 (금방이라도 닥칠)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "39b418e4-3267-493e-bd2e-874d489681ff",
        "word": "Impending",
        "meaning": "곧 닥칠 (불길한 일이 다가오는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "99c2a753-6e1e-4b0f-b3a8-a66001288c34",
        "word": "Looming",
        "meaning": "어렴풋이 나타나는 (걱정거리가 다가오는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "f63342d5-8c98-492f-bb94-13e16cbae3da",
        "word": "Forthcoming",
        "meaning": "다가오는, 곧 나올 (준비된)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "772f274b-e85d-45d8-acce-23e6b8eddc7f",
        "word": "Eventual",
        "meaning": "궁극적인, 언젠가는 일어날 (결국에는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "96213112-b7b5-4bf9-9501-e3ef6d3f8a0b",
        "word": "Ultimate",
        "meaning": "최후의, 궁극적인 (마지막 단계의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "e40a7112-8968-4f50-a935-e9cf1abedb2f",
        "word": "Bygone",
        "meaning": "지나간, 과거의 (추억 속의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "433903c5-7c60-4af1-aede-096e6432696e",
        "word": "Former",
        "meaning": "이전의, 전직의 (직전의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "f960fc72-d250-4549-bcc0-7f3d10fe1665",
        "word": "Previous",
        "meaning": "이전의, 앞선 (순서상 앞의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "381adc24-999e-4dfc-aa61-fbbaba39f8fc",
        "word": "Obsolete",
        "meaning": "구식의, 쓸모없게 된 (더 이상 안 쓰는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "15a1cd7f-8979-4b58-8ad9-b6f23de9b809",
        "word": "Outdated",
        "meaning": "구식인 (날짜가 지난)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "18376b98-b352-458d-91ac-86d396ee1cb7",
        "word": "Antedated",
        "meaning": "시기보다 앞선 (실제보다 날짜를 앞당긴)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "3a0053c5-fe4f-454e-83fe-ca576d3b156d",
        "word": "Retroactive",
        "meaning": "소급 적용되는 (과거까지 거슬러 올라가는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "52f9461d-f52f-47a3-a647-80edfa0b0cce",
        "word": "Anachronistic",
        "meaning": "시대착오적인 (시대에 맞지 않는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "a791188d-745b-4fe0-b5f7-d6eb9db50dc3",
        "word": "Timely",
        "meaning": "시의적절한 (딱 좋은 때의)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "56d7c8d7-7cd2-4fc2-93a7-1e1ffaf2b487",
        "word": "Up-to-date",
        "meaning": "최신의 (현대적인)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "e6227a22-77c0-48f4-b8a9-268268dd4b55",
        "word": "State-of-the-art",
        "meaning": "최첨단의 (가장 발달한)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    },
    {
        "card_id": "c4c606db-635b-4937-b13e-fcefce75636c",
        "word": "Cutting-edge",
        "meaning": "최첨단의 (가장 앞서가는)",
        "deck_id": "2c4e6e97-5bf8-4442-81d7-666d09084032",
        "deck_title": "TIMELINESS_FUTURE_PAST"
    }
]

RELEVANT_TAGS = [
    "interview",
    "conversation",
    "relationship",
    "fashion",
    "family",
    "marketing",
    "hobby",
    "smartphone",
    "soccer",
    "education"
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
- 위 태그들은 'TIMELINESS_FUTURE_PAST' 덱과 관련이 깊은 주제들입니다
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

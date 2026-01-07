#!/usr/bin/env python3
"""
예문 생성 스크립트: GROWTH_PROSPERITY

이 스크립트는 'GROWTH_PROSPERITY' 덱의 단어들에 대해
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
    "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
    "deck_title": "GROWTH_PROSPERITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "f04c2955-0d94-446e-97b6-32d6b22e2556",
        "word": "Flourish",
        "meaning": "번창하다 (꽃이 피듯 아주 잘되다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "fed06d0e-1e79-4880-a10a-f0492fa44994",
        "word": "Thrive",
        "meaning": "잘 자라다, 성공하다 (역경을 딛고 왕성하게)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "ea092f48-9dfb-4caf-be3b-de2112477cf7",
        "word": "Prosper",
        "meaning": "번영하다 (경제적으로 부유해지다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "abf062da-ba4d-4cf6-83f7-bbfc1cbcae71",
        "word": "Boom",
        "meaning": "호황을 맞다, 급속히 발전하다",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "925917fa-4b59-4b33-b639-874efb81548f",
        "word": "Blossom",
        "meaning": "꽃피다, 발달하다 (재능/관계가 만개하다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "bf658a8b-eb72-430a-9216-8e19aa43a8b0",
        "word": "Burgeon",
        "meaning": "급성장하다 (싹이 트듯 빠르게 커지다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "daa5cd6a-0212-4d13-98c0-ba4653e5bf51",
        "word": "Expand",
        "meaning": "확장하다 (범위나 부피가 넓어지다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "7a90d19a-5ba2-4af6-bcb7-8d87fab9ab14",
        "word": "Escalate",
        "meaning": "확대되다, 고조되다 (단계적으로 올라가다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "7ce2f2cd-2d9a-4d36-9f14-651f82cbe8f7",
        "word": "Surge",
        "meaning": "급증하다 (파도처럼 밀려들다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "93cb4804-e556-4886-9e7c-c6d23b439b0d",
        "word": "Soar",
        "meaning": "치솟다 (하늘 높이 날아오르다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "48f9fd7c-52c0-41c8-a673-7830983d14d2",
        "word": "Skyrocket",
        "meaning": "급등하다 (로켓처럼 수직 상승하다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "3a2ba71b-f2b1-4fb3-820f-42ffddf88a53",
        "word": "Amplify",
        "meaning": "증폭시키다 (소리나 효과를 키우다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "070b0e03-f924-4161-a8ec-03cee1ec183b",
        "word": "Augment",
        "meaning": "증대시키다 (추가해서 늘리다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "03a6edf7-6aad-45f1-894b-445045d88743",
        "word": "Enhance",
        "meaning": "향상하다 (질이나 가치를 높이다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "4068e78f-93d0-401e-87a8-f5227cd9acd8",
        "word": "Elevate",
        "meaning": "승격시키다, 높이다 (지위나 수준을 올리다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "4b501ff5-3ac9-43e8-b240-68981d9a2013",
        "word": "Proliferate",
        "meaning": "급증하다, 확산하다 (세포분열 하듯 늘다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "300b6638-a1ce-4bca-9300-64d2fa82447e",
        "word": "Advance",
        "meaning": "진보하다, 나아가다 (앞쪽으로 이동하다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "c10e8803-023f-4d04-89b4-4f742fa1ffe3",
        "word": "Progress",
        "meaning": "전진하다, 진행하다 (목표를 향해 가다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "3c3391c5-9815-4f48-a203-469966a97330",
        "word": "Develop",
        "meaning": "개발하다, 발달하다 (잠재력을 깨우다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "76b4195f-21f3-4b69-9fe1-1bd95499141d",
        "word": "Mature",
        "meaning": "성숙하다 (완전히 자라다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "a13145ce-3abc-4271-b065-e69cc7e2e023",
        "word": "Ripen",
        "meaning": "익다 (과일/기회가 무르익다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "3b1ecd26-7028-4dda-a4fb-60f895ef66cc",
        "word": "Accumulate",
        "meaning": "축적하다 (조금씩 모이다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "9375b599-ba7b-45fb-83aa-b2368ff507f4",
        "word": "Amass",
        "meaning": "모으다 (대량으로 쌓다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "33476ecc-bbc5-4feb-9f34-7c80f361e5e6",
        "word": "Multiply",
        "meaning": "증식하다, 곱하다 (수가 크게 늘다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "d22721b8-6943-4805-bec8-7b2bc3a9bb95",
        "word": "Boost",
        "meaning": "신장시키다, 북돋우다 (아래서 위로 밀어 올림)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "0e84d937-c62f-43c9-a423-0487b5c7c808",
        "word": "Fortify",
        "meaning": "강화하다 (방어력을 높이다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "e24cfd73-fcfc-4fcc-bfdf-e6a51e50bda4",
        "word": "Strengthen",
        "meaning": "강화하다 (힘을 더하다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "33e96e4d-f9e5-44da-9401-ce21fd336bf5",
        "word": "Optimize",
        "meaning": "최적화하다 (가장 효율적으로 만들다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "16fb4e29-d489-4b72-b47e-663b3220ea58",
        "word": "Maximize",
        "meaning": "극대화하다 (최대치로 끌어올리다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    },
    {
        "card_id": "2fad8dd1-9a04-47b3-bb94-59bc2aeff23a",
        "word": "Upgrade",
        "meaning": "개선하다, 업그레이드하다 (등급을 올리다)",
        "deck_id": "d6f27f44-4958-4d0d-a295-3f562908ca9d",
        "deck_title": "GROWTH_PROSPERITY"
    }
]

RELEVANT_TAGS = [
    "feeling",
    "dining",
    "education",
    "environment",
    "planning",
    "style",
    "ai",
    "hot",
    "time",
    "university"
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
- 위 태그들은 'GROWTH_PROSPERITY' 덱과 관련이 깊은 주제들입니다
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

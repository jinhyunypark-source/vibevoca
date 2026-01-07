#!/usr/bin/env python3
"""
예문 생성 스크립트: TASTE

이 스크립트는 'TASTE' 덱의 단어들에 대해
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
    "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
    "deck_title": "TASTE",
    "total_words": 22
}

WORDS = [
    {
        "card_id": "4ca2d456-dcce-43ba-97d4-82eb7abfae2a",
        "word": "Delicious",
        "meaning": "맛있는",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "82ecadac-32b0-41de-8a3b-4813d6ca441c",
        "word": "Savory",
        "meaning": "감칠맛 나는, 짭짤한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "f7164646-65aa-47d1-9357-8d1c34aa78d9",
        "word": "Succulent",
        "meaning": "즙이 많은",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "c1f279d5-7dc7-4cd1-bd8e-e774fb92406a",
        "word": "Zesty",
        "meaning": "상큼한, 톡 쏘는",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "bb5f34d5-3451-4a62-ae9a-f9944dfc091d",
        "word": "Tangy",
        "meaning": "새콤한, 톡 쏘는",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "e061ea45-e93d-4b77-ba94-d5384486dff8",
        "word": "Scrumptious",
        "meaning": "정말 맛있는 (구어체)",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "45794628-11ee-4b1f-b398-87f14996b177",
        "word": "Delectable",
        "meaning": "입안이 즐거운, 맛있는 (라) laetus 즐거운",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "610d9fff-3dc8-4cf9-a225-e1e22b2c4067",
        "word": "Palatable",
        "meaning": "입에 맞는, 먹을 만한(라) 'palatum'(입천장)",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "49a4f011-3f03-42db-8fbf-8c509de355a8",
        "word": "Appetizing",
        "meaning": "구미를 당기는",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "e757f6bc-6e4b-48e4-b893-62025242e5eb",
        "word": "Exquisite",
        "meaning": "정교한 맛의",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "1d77e2cf-986f-4e57-86f5-3440af27a83c",
        "word": "Bland",
        "meaning": "싱거운, 밋밋한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "5eb78bd9-3438-4f39-a778-7cbebe94237d",
        "word": "Stale",
        "meaning": "상한, 눅눅해진",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "9d9faa94-10cd-4f03-8fe2-0a231a6a7ad5",
        "word": "Rancid",
        "meaning": "산패한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "9b4cd713-6809-4452-bfc2-fc699fbe14bf",
        "word": "rancor",
        "meaning": "깊은원한 증오",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "b6ad3f6c-3011-4fda-91ff-b2865df66b97",
        "word": "Insipid",
        "meaning": "맛없는, 김빠진 in+sapere",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "4b54d7ef-a7aa-40e9-b448-af57ebd8d8f0",
        "word": "Pungent",
        "meaning": "톡 쏘는, 자극적인  (라)pungere 찌르다 . ex puncture (구멍내다)",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "510fe3f5-fc19-4274-8b48-b45178de2af1",
        "word": "Acrid",
        "meaning": "매캐한, 쓴",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "16f8c3ff-d135-428e-b83b-6e1756f2f345",
        "word": "Bitter",
        "meaning": "쓴",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "97808f29-8f3f-4333-8b4e-d9f1f5a14af6",
        "word": "Greasy",
        "meaning": "기름진, 느끼한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "359dca20-bbf3-48ef-8438-1eced62d0ad1",
        "word": "Rich",
        "meaning": "진한, 풍부한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "f9805998-2a3a-426b-9528-b55dc3079b09",
        "word": "Crispy",
        "meaning": "바삭바삭한",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    },
    {
        "card_id": "74bb12bd-5f98-426f-a7da-400247bbeee6",
        "word": "Chewy",
        "meaning": "쫄깃한, 질긴",
        "deck_id": "19887ed8-9106-47d7-8d89-c1724642844e",
        "deck_title": "TASTE"
    }
]

RELEVANT_TAGS = [
    "code",
    "communication",
    "internet",
    "activity",
    "movie",
    "time",
    "entertainment",
    "journey",
    "marketing",
    "health"
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
- 위 태그들은 'TASTE' 덱과 관련이 깊은 주제들입니다
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

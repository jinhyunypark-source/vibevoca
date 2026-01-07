#!/usr/bin/env python3
"""
예문 생성 스크립트: DOMINANCE_CONTROL

이 스크립트는 'DOMINANCE_CONTROL' 덱의 단어들에 대해
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
    "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
    "deck_title": "DOMINANCE_CONTROL",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "1dd200a1-9892-4c86-8849-ffd20220ed0e",
        "word": "Potent",
        "meaning": "강력한 (효과나 영향력이 센)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "596724eb-347f-4a4b-a810-ab3ac65e7cb7",
        "word": "Forceful",
        "meaning": "강압적인, 힘찬 (강하게 밀어붙이는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "51f74d17-c82f-4757-b6c8-0b6b716e41bb",
        "word": "Dominant",
        "meaning": "지배적인, 우세한 (가장 힘이 세고 주도적인)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "86d5d8c7-7c84-4553-9d31-00fcacb0e18f",
        "word": "Sovereign",
        "meaning": "주권이 있는, 자주적인 (간섭받지 않는 최고의 권력)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "0534789e-ed3b-443c-9bec-fa4ec316d107",
        "word": "Commanding",
        "meaning": "지휘하는, 위엄 있는 (명령을 내릴 위치에 있는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "4e3cdc7e-30eb-4f7a-85c6-bace54760ef4",
        "word": "Prevailing",
        "meaning": "우세한, 널리 퍼진 (현재 이기고 있거나 주류인)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "d9cf3cc3-2b64-43bc-b5e9-1b73419524d4",
        "word": "Controlling",
        "meaning": "통제하는 (모든 것을 관리하려는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "eaba191c-7618-4a2b-9fd9-a656d4de03a7",
        "word": "Powerful",
        "meaning": "강력한 (힘이나 영향력이 큰)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "cdb2d30c-b797-4ea0-9514-3c1fd0146958",
        "word": "Mighty",
        "meaning": "강대한, 힘센 (규모가 크고 압도적인)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "b39d9b4d-4d72-4f05-b4d6-21a915093547",
        "word": "Supreme",
        "meaning": "최고의, 최상의 (가장 높은 위치의)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "53c60ad4-f37e-437f-8e14-b4ae250209cd",
        "word": "Ruling",
        "meaning": "지배하는, 통치하는 (현재 권력을 잡고 있는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "f7e1912f-9f03-4ea9-9efa-7c4435f4bf76",
        "word": "Governing",
        "meaning": "통치하는, 관리하는 (행정적으로 다스리는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "b0b60343-14d8-4853-92fb-ee7bea99696a",
        "word": "Reigning",
        "meaning": "군림하는, 현재 타이틀을 가진 (왕이나 챔피언)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "2f575ed4-f250-4722-923f-833b866fa105",
        "word": "Invincible",
        "meaning": "천하무적의 (이길 수 없는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "e940b923-60db-41b1-8f8e-a6309c65fc49",
        "word": "Ascendant",
        "meaning": "상승세인, 우세한 (힘이 커지고 있는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "84c937ce-78a5-42ea-ba0e-420b6449b844",
        "word": "Predominant",
        "meaning": "두드러진, 주된 (수적으로나 힘으로 우위인)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "1acdb4b9-a4f4-485b-81fa-e638cda59684",
        "word": "Hegemonic",
        "meaning": "패권적인 (한 국가나 집단이 주도권을 잡은)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "e3ad5452-82ff-4701-b070-e8c1fd7e3c61",
        "word": "Omnipotent",
        "meaning": "전지전능한 (모든 힘을 다 가진)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "cef7bbd0-03db-4a04-8ae3-976af00b18e5",
        "word": "Unrivaled",
        "meaning": "경쟁자가 없는 (비할 데 없는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "63d43d1b-7f01-4482-aa35-ffc58607f700",
        "word": "Superior",
        "meaning": "우월한, 상급의 (남보다 나은)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "e5b89a72-bfff-4939-b23b-362e3124d06b",
        "word": "Chief",
        "meaning": "주요한, 장(長) (조직의 우두머리)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "c2598613-d435-42bc-9751-6749888e8f11",
        "word": "Lead",
        "meaning": "이끄는, 선두의 (앞장서는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "e7e9e056-b442-47cc-91db-f1dfc4e7d25e",
        "word": "Directing",
        "meaning": "지시하는, 감독하는 (방향을 잡아주는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "575b0f57-c09c-4866-87cc-cf3ec3660669",
        "word": "Managing",
        "meaning": "관리하는 (운영하고 다루는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "b372cb0e-4d4f-4a54-b49c-df4f3f35b9be",
        "word": "Supervising",
        "meaning": "감독하는 (지켜보며 관리하는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "30b12460-8a8a-46fb-8fa3-b6ac6b7fd83a",
        "word": "In charge",
        "meaning": "책임이 있는, 담당하는 (권한을 가진)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "f6811b4d-9933-4efd-adcc-133291175434",
        "word": "Masterful",
        "meaning": "주인 같은, 능수능란한 (통제력을 가진)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "5b7356e7-24d4-46a8-b5bd-f010b056a09b",
        "word": "Overriding",
        "meaning": "최우선의, 기각하는 (다른 것보다 더 중요한 권한)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "a6f4af57-5438-4813-aad0-9a1f2bde9363",
        "word": "Preeminent",
        "meaning": "탁월한, 우위의 (남보다 뛰어난)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    },
    {
        "card_id": "8c1a4bc3-c31a-4542-aef9-77402f427ee7",
        "word": "Assertive",
        "meaning": "자기주장이 강한 (단호하게 권리를 찾는)",
        "deck_id": "eee15cc6-7b0d-4b17-9921-9225c31d5c88",
        "deck_title": "DOMINANCE_CONTROL"
    }
]

RELEVANT_TAGS = [
    "hobby",
    "study",
    "entrepreneur",
    "schedule",
    "cooking",
    "happy",
    "education",
    "time",
    "soccer",
    "social"
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
- 위 태그들은 'DOMINANCE_CONTROL' 덱과 관련이 깊은 주제들입니다
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

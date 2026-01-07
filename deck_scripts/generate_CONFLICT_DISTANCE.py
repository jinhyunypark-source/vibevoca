#!/usr/bin/env python3
"""
예문 생성 스크립트: CONFLICT_DISTANCE

이 스크립트는 'CONFLICT_DISTANCE' 덱의 단어들에 대해
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
    "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
    "deck_title": "CONFLICT_DISTANCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "1b39d9e9-b2a3-481d-a7d5-4fd6b67da37c",
        "word": "Hostile",
        "meaning": "적대적인 (적으로 간주하고 공격적인)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "a3404724-92e2-4f0e-a427-ea6d070160d1",
        "word": "Estranged",
        "meaning": "소원해진, 별거 중인 (사이가 멀어져 남남이 된)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "8c9d3e29-cee0-47fb-b7c3-28fe35c47fe6",
        "word": "Distant",
        "meaning": "거리감을 두는 (친하지 않고 멀리하는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "86553075-80d6-403c-a861-cf701f614925",
        "word": "Cold",
        "meaning": "차가운, 쌀쌀맞은 (감정이 없는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "731964ee-e3a8-4200-9889-45e7624002ca",
        "word": "Aloof",
        "meaning": "냉담한 (거리를 두고 무심한 척하는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "bf057e25-ca24-46a4-9945-c7e724e9c700",
        "word": "Detached",
        "meaning": "무심한, 초연한 (감정적으로 분리된)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "bc065515-e244-49b7-845f-ddc87a1cecd3",
        "word": "Alienated",
        "meaning": "소외된 (동떨어지고 배척당한 느낌)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "d031cb19-4c34-4686-b7c4-3be9dd202586",
        "word": "Isolated",
        "meaning": "고립된 (혼자 떨어져 있는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "fc56c205-b1df-44a6-bc77-b953e0aa5cde",
        "word": "Incompatible",
        "meaning": "맞지 않는 (성격 차이로 공존 불가능한)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "5c6b6a6d-bd69-4549-bf78-741de84e1ff4",
        "word": "Abusive",
        "meaning": "학대하는 (폭력적이거나 모욕적인)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "000d57bb-9897-4c9e-8170-8764e29889fa",
        "word": "Toxic",
        "meaning": "유해한 (정신적으로 해를 끼치는 관계)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "892d82e1-af23-4925-a522-3d2bbe7c302a",
        "word": "Manipulative",
        "meaning": "조종하는 (교묘하게 이용해 먹는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "53bf8d1d-ebd8-4acd-abb3-8cef1c16349d",
        "word": "Controlling",
        "meaning": "통제하려는 (자기 멋대로 하려는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "53466d53-7564-47f7-b106-5dd9c8f5bf07",
        "word": "Jealous",
        "meaning": "질투하는 (내 것을 뺏길까 봐/남을 시샘하여)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "de6df224-9b13-4621-8b41-4f816a6c137e",
        "word": "Envious",
        "meaning": "부러워하는 (남의 것이 탐나서)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "41938ae5-db38-4b5c-b771-8a0ad295e757",
        "word": "Resentful",
        "meaning": "원망하는, 앙심을 품은 (억울해서 화난)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "845d4331-e261-48bc-b27d-3ab0a16c70c7",
        "word": "Bitter",
        "meaning": "쓰라린, 비통해하는 (상처받아 냉소적인)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "deb1d78d-20bf-4625-8dce-cce9d06636c3",
        "word": "Vengeful",
        "meaning": "복수심에 불타는 (되갚아주려는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "38362ba7-1650-4f73-b1b2-50578dcb27ff",
        "word": "Spiteful",
        "meaning": "앙심 깊은 (괴롭히려는 악의가 있는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "abc562fd-54b3-4a4b-bb7c-dd009c44678a",
        "word": "Feud",
        "meaning": "불화, 반목 (오랫동안 지속된 싸움)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "44b48dd1-393e-45ed-9026-e2a23dcc0019",
        "word": "Rivalry",
        "meaning": "라이벌 의식, 경쟁 (서로 이기려는 관계)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "a4ac0436-77cb-49e8-b572-6376a429253c",
        "word": "Friction",
        "meaning": "마찰 (의견 충돌로 인한 삐걱거림)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "34eca3a7-8387-413f-8e33-4af895610211",
        "word": "Tension",
        "meaning": "긴장 (불편하고 팽팽한 분위기)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "ab71c88b-e28c-493a-8ad9-9b244004ba94",
        "word": "Conflict",
        "meaning": "갈등, 충돌 (직접적인 싸움)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "282ffd00-3fc6-4e05-867d-cc3e5be37465",
        "word": "Broken",
        "meaning": "깨진 (관계가 파탄 난)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "a28b3ca1-ac40-4aca-8300-4d83c5ebcfd4",
        "word": "Divorced",
        "meaning": "이혼한 (법적으로 갈라선)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "e890b615-ae10-40fd-8620-52723cd6babf",
        "word": "Separated",
        "meaning": "별거 중인 (헤어져 사는)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "f35d7842-2917-47d2-b9c8-f8b8b68978c9",
        "word": "Antagonistic",
        "meaning": "적대적인, 반감을 가진 (사사건건 반대하는)    (그)agonistes(배우,경쟁자)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "7fc08a1c-2b07-4c23-8392-7611e9fb8f41",
        "word": "Confrontational",
        "meaning": "대립을 일삼는 (싸움을 거는 성향)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    },
    {
        "card_id": "d67f72d1-0530-4252-a67e-cfdbbc6000b6",
        "word": "Unfriendly",
        "meaning": "비우호적인 (친절하지 않은)",
        "deck_id": "7a168e67-0544-4ef5-a6b3-69d1412c5330",
        "deck_title": "CONFLICT_DISTANCE"
    }
]

RELEVANT_TAGS = [
    "home",
    "restaurant",
    "dining",
    "social",
    "medical",
    "weather",
    "cooking",
    "friendship",
    "family",
    "ai"
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
- 위 태그들은 'CONFLICT_DISTANCE' 덱과 관련이 깊은 주제들입니다
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

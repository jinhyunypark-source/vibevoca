#!/usr/bin/env python3
"""
예문 생성 스크립트: SOCIAL_STATUS_CONNECTION

이 스크립트는 'SOCIAL_STATUS_CONNECTION' 덱의 단어들에 대해
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
    "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
    "deck_title": "SOCIAL_STATUS_CONNECTION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "b4ffb7cc-cbc3-461d-8d0d-a9d8ce40ba1e",
        "word": "Acquaintance",
        "meaning": "지인 (알긴 하지만 친하지는 않은)   (라)ad+ cognoscere(알다)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "e65ac611-00df-407d-a35f-f6a4952d25c5",
        "word": "Kin",
        "meaning": "친족 (혈연관계)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "f357d05d-b07e-405d-bbf1-9a6f53d3b6e8",
        "word": "Colleague",
        "meaning": "동료 (전문직/직장에서 함께 일하는)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "bf382097-9fd0-4043-a665-f5bc3c86b037",
        "word": "Co-worker",
        "meaning": "직장 동료 (같은 직장에서 일하는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "d19f4d51-eca3-44ca-9abc-4466e5c3578b",
        "word": "Predecessor",
        "meaning": "전임자 (앞서 그 자리에 있던 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "a1eac0c4-fa37-492e-8e3d-c1eaca5effca",
        "word": "Peer",
        "meaning": "또래, 동등한 사람 (나이/지위가 같은)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "83d20e89-6bb2-4465-b239-a2427c81f43c",
        "word": "Associate",
        "meaning": "동료, 제휴한 사람 (사업상 연결된)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "3708578c-2428-4126-a0c9-e951b9fd41dd",
        "word": "Superior",
        "meaning": "상급자 (지위가 높은 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "6bf9f0a4-0a80-43e3-b2c6-8e40d546485d",
        "word": "Subordinate",
        "meaning": "부하 직원, 하급자 (지위가 낮은 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "ab5bdbf4-b9a3-4a62-9441-6fa643cae6e9",
        "word": "Mentor",
        "meaning": "멘토, 스승 (조언과 지도를 주는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "7bba0e5e-334c-4609-9544-ec22b8999b19",
        "word": "Mentee",
        "meaning": "멘티 (지도를 받는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "4d3a2dcd-1461-417c-878a-9d952867e83c",
        "word": "Client",
        "meaning": "의뢰인, 고객 (전문 서비스를 받는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "5c25bab7-25ff-4946-8ebb-337a843ba49b",
        "word": "Customer",
        "meaning": "고객, 손님 (물건을 사는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "91edd18b-bc0d-48ac-ba31-749b16ed56be",
        "word": "Stranger",
        "meaning": "낯선 사람 (전혀 모르는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "2a714028-9e13-49ac-85ee-01eeff885d97",
        "word": "Outsider",
        "meaning": "외부인 (그룹에 속하지 않은)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "ddf43cba-8d8c-4a8b-835f-800115c20e87",
        "word": "Insider",
        "meaning": "내부자 (그룹 내 정보를 아는)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "6e9f4e5b-3454-4e10-89ad-7b87b5418e5d",
        "word": "Network",
        "meaning": "인맥, 네트워크 (연결된 사람들의 망)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "089363e7-c747-4707-8ece-4910b69ec4a2",
        "word": "Connection",
        "meaning": "연줄, 관계 (아는 사이/연결 고리)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "9a8fb038-8be7-4cbc-a9bb-8bc5b1ca4e9d",
        "word": "Contact",
        "meaning": "연락책, 지인 (연락 가능한 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "17457904-20e5-4aa9-bfe6-fdd17f2f05d8",
        "word": "Relation",
        "meaning": "친척 (가족 관계에 있는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "46d3d80d-6c91-4de6-8905-7b7115d5c11b",
        "word": "Neighbor",
        "meaning": "이웃 (근처에 사는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "81b31609-92d8-412a-b3dd-86923728023f",
        "word": "Roommate",
        "meaning": "룸메이트 (방을 같이 쓰는 사람)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "d1e3cb0f-0d2a-42ad-8459-e7be297f0252",
        "word": "Classmate",
        "meaning": "동급생 (같은 반 친구)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "2085ba9d-9bc0-4df7-9ae4-f40f4129fc18",
        "word": "Alumni",
        "meaning": "동창생 (같은 학교 졸업생)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "e968a6ba-9325-4936-85d7-7b809a9cab1b",
        "word": "Fellow",
        "meaning": "동료, 회원 (같은 처지나 학회의)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "57d05347-be27-428b-bf39-f2a5127379c7",
        "word": "Counterpart",
        "meaning": "상대방, 대응 관계에 있는 사람",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "50750fc3-2d7c-45ec-b7a5-0be9e9d9ae0e",
        "word": "Rival",
        "meaning": "라이벌, 경쟁자 (경쟁하는 관계)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "736c4b08-49ac-4e95-bd54-293a58fabefd",
        "word": "Competitor",
        "meaning": "경쟁자 (시합이나 시장에서의 경쟁)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "319c85df-c9f3-4be3-80db-3cff9a2d8597",
        "word": "Equal",
        "meaning": "동등한 사람 (지위나 능력이 같은)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    },
    {
        "card_id": "4a072904-bedd-40db-9999-0e3e37514691",
        "word": "Public",
        "meaning": "대중 (일반 사람들)",
        "deck_id": "c1f6aabe-8beb-449b-bf58-7635ace29643",
        "deck_title": "SOCIAL_STATUS_CONNECTION"
    }
]

RELEVANT_TAGS = [
    "home",
    "music",
    "dining",
    "career",
    "feeling",
    "journey",
    "family",
    "friendship",
    "mood",
    "job"
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
- 위 태그들은 'SOCIAL_STATUS_CONNECTION' 덱과 관련이 깊은 주제들입니다
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

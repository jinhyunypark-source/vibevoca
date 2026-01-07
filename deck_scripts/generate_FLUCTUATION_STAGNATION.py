#!/usr/bin/env python3
"""
예문 생성 스크립트: FLUCTUATION_STAGNATION

이 스크립트는 'FLUCTUATION_STAGNATION' 덱의 단어들에 대해
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
    "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
    "deck_title": "FLUCTUATION_STAGNATION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "70db595a-ab83-455f-890e-367f48c9d3df",
        "word": "Fluctuate",
        "meaning": "변동하다 (불규칙하게 오르내리다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "7b0cc823-ec1c-4db1-b876-ecb9030cfc5b",
        "word": "Vacillate",
        "meaning": "흔들리다 (결정을 못 내리고 오락가락하다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "4886efbe-0a98-42f3-bada-0bff33762370",
        "word": "Oscillate",
        "meaning": "진동하다 (추처럼 규칙적으로 왔다 갔다 하다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "e7b374fa-9ac0-423e-bb8c-38a0ed00f847",
        "word": "Swing",
        "meaning": "그네처럼 흔들리다 (크게 변하다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "a4e77078-9a98-49fe-af44-7dbd6d9ef007",
        "word": "Vary",
        "meaning": "달라지다 (일정하지 않다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "300d5416-c33f-47cc-8935-2b67a45922ae",
        "word": "Waver",
        "meaning": "약해지다, 흔들리다 (불안정하게 떨리다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "a3b7c9ed-9552-4258-9a39-cbc90e971d87",
        "word": "Alternate",
        "meaning": "번갈아 일어나다 (A-B-A-B 패턴)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "2a303c13-4dbc-46a9-8276-d1c0968ea559",
        "word": "Seesaw",
        "meaning": "일진일퇴하다 (시소처럼 위아래로)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "88d0f1a5-7430-4d54-b4e1-c2899392b679",
        "word": "Stagnate",
        "meaning": "침체하다 (고여서 흐르지 않다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "9304691e-1e0e-4848-9735-0369a394e980",
        "word": "Stall",
        "meaning": "교착 상태에 빠지다 (엔진이 꺼지듯 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "05c8bd38-3aff-4744-bb16-2145e8981c46",
        "word": "Plateau",
        "meaning": "정체기에 들다 (상승하다가 평평해지다)  like plate",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "38eacaef-b595-4c33-b420-a462685d7a81",
        "word": "Stabilize",
        "meaning": "안정되다 (흔들림을 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "30e7b128-7a68-497c-a9b1-695868a88d5a",
        "word": "Settle",
        "meaning": "자리를 잡다, 가라앉다 (움직임이 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "974b89cb-9ff7-49fb-9a8f-f08e977d6c28",
        "word": "Remain",
        "meaning": "여전히 ~이다 (변하지 않고 남다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "58315cf0-511f-4d99-a830-64fb8579f5b8",
        "word": "Persist",
        "meaning": "지속되다, 고집하다 (없어지지 않고 계속되다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "178e4098-b858-4266-9ce3-8b419249b0ba",
        "word": "Endure",
        "meaning": "지속되다, 견디다 (오래가다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "3502a6d3-a8d3-4ed7-a051-c8736569c7ff",
        "word": "Last",
        "meaning": "계속하다 (시간적으로 지속되다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "e0b9e89f-d893-4d58-947e-c4cb0f1d82d1",
        "word": "Freeze",
        "meaning": "동결하다 (움직임을 완전히 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "613ba90e-6e77-492c-aa92-f014c595544e",
        "word": "Halt",
        "meaning": "중단시키다 (가던 것을 세우다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "2aad289b-55f8-4586-8701-3fcb7bfe0303",
        "word": "Pause",
        "meaning": "일시 정지하다 (잠깐 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "981aaf6a-1899-408f-be99-a740e9ce3b4f",
        "word": "Suspend",
        "meaning": "유예하다, 매달다 (공중에 띄워 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "c2e6b986-301e-4667-8e66-c3ce147dd496",
        "word": "Linger",
        "meaning": "오래 머물다 (떠나지 않고 질질 끌다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "e3f19d32-54d4-4e28-ad32-441533393f8d",
        "word": "Hover",
        "meaning": "맴돌다 (수치나 위치가 제자리에서)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "092d8545-75c7-414f-9518-5de4e463cc0f",
        "word": "Drift",
        "meaning": "표류하다 (목적 없이 흘러가다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "258d8452-581d-4e37-a017-4cf5483707e3",
        "word": "Meander",
        "meaning": "굽이쳐 흐르다 (이리저리 천천히 가다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "aadb29df-00bf-42d5-acd5-44cac70ab34d",
        "word": "Deviate",
        "meaning": "일탈하다, 벗어나다 (경로에서 빠지다). de(떨어져) + via(길)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "e17ce51a-746d-458d-a0e7-781b4f5d017e",
        "word": "Diverge",
        "meaning": "갈라지다 (한 점에서 나뉘다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "fe52cf73-b647-48d2-b11b-9e68c0375e94",
        "word": "Converge",
        "meaning": "모여들다 (한 점으로 합쳐지다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "687e22ff-4942-4539-bda2-182e82864d11",
        "word": "Level off",
        "meaning": "수평을 유지하다 (상승/하락 후 멈추다)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    },
    {
        "card_id": "6d7a1301-5383-4db9-9339-40aa487d7309",
        "word": "Steady",
        "meaning": "꾸준한, 안정된 (변함없는)",
        "deck_id": "d839b445-4cd5-4a29-901e-9e4d433c4c6d",
        "deck_title": "FLUCTUATION_STAGNATION"
    }
]

RELEVANT_TAGS = [
    "exercise",
    "sport",
    "code",
    "feeling",
    "emotion",
    "nature",
    "conversation",
    "style",
    "food",
    "mood"
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
- 위 태그들은 'FLUCTUATION_STAGNATION' 덱과 관련이 깊은 주제들입니다
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

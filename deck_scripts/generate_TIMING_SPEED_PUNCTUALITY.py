#!/usr/bin/env python3
"""
예문 생성 스크립트: TIMING_SPEED_PUNCTUALITY

이 스크립트는 'TIMING_SPEED_PUNCTUALITY' 덱의 단어들에 대해
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
    "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
    "deck_title": "TIMING_SPEED_PUNCTUALITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d26ce6d7-aad9-46b9-90b9-2956b68caa67",
        "word": "Punctual",
        "meaning": "시간을 엄수하는 (정해진 시각에 딱 맞추는)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "b73b65dc-f3b0-4130-9fe8-eacf5f0f6fb3",
        "word": "Prompt",
        "meaning": "즉각적인, 지체 없는 (반응이 빠른)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "0acc52fe-cb12-458d-bf4f-70fb44bd6c9c",
        "word": "Timely",
        "meaning": "시기적절한 (딱 알맞은 때에 일어난)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "b77c08a9-60f8-4b19-a2fa-614f0a6a9e04",
        "word": "Tardy",
        "meaning": "느린, 지각한 (제시간보다 늦은)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "05217c64-c51d-4406-811e-b70dbc5c9a4b",
        "word": "Delayed",
        "meaning": "지연된 (예정보다 늦어진)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "5b5ea162-b57d-4a42-bac4-fe6c546137d1",
        "word": "Overdue",
        "meaning": "기한이 지난 (이미 늦은)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "9ccc17b2-5298-4c40-8574-d73eb4c96283",
        "word": "Belated",
        "meaning": "뒤늦은 (시기를 놓치고 나중에 한)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "3034b053-ce44-4762-8324-2bab706b686d",
        "word": "Premature",
        "meaning": "시기상조의, 너무 이른 (제때보다 이른)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "a1330928-7105-4fe2-aa88-ab410d90f19f",
        "word": "Precocious",
        "meaning": "조숙한 (나이에 비해 발달이 빠른)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "fb1c9b01-646a-4b2a-a8d3-8dc66dc8d408",
        "word": "Simultaneous",
        "meaning": "동시의 (같은 시각에 일어나는)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "f1e81c84-55e3-4c83-83f9-a121f95aa807",
        "word": "Synchronized",
        "meaning": "동기화된 (시간을 딱 맞춘)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "c0a8d195-7e7a-4e17-9778-d292c695b09c",
        "word": "Coincident",
        "meaning": "일치하는, 동시에 일어나는 (우연히 겹친)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "804c4b3a-073e-4628-aee5-43fbb459caba",
        "word": "Opportune",
        "meaning": "시의적절한 (기회 잡기에 좋은)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "aacf084d-66b6-42a8-acce-71a45520de98",
        "word": "Inopportune",
        "meaning": "시기가 나쁜 (때가 안 좋은)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "342348e2-f19f-4791-b501-979de371222d",
        "word": "Seasonable",
        "meaning": "계절에 맞는 (제철의)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "fa7bf6bb-b784-4dc2-939c-034772cf1847",
        "word": "Urgent",
        "meaning": "긴급한 (즉각적 행동이 필요한)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "63b508b1-d5c3-4a6c-9d26-26450b26d697",
        "word": "Pressing",
        "meaning": "압박하는, 긴박한 (무시할 수 없는)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "567986c6-3aab-44e9-bf66-f808d9f51eda",
        "word": "Immediate",
        "meaning": "즉시의 (시간차 없는)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "ab304a9f-c745-4e86-a38f-08c74cc3f81b",
        "word": "Instant",
        "meaning": "즉석의, 순간적인 (조리/준비 없이 바로)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "e9346d88-4e1b-423f-906f-6ca7027423b9",
        "word": "Swift",
        "meaning": "신속한 (움직임이 빠른)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "93aa2bdd-8d2e-44ef-9029-21db7cbc8949",
        "word": "Rapid",
        "meaning": "빠른 (속도가 높은)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "82f88c74-9e67-4e61-b771-7c4e00096029",
        "word": "Hasty",
        "meaning": "서두르는 (급하게 해서 엉성한)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "9ecf4784-6d2a-4632-837e-b7fa7907c945",
        "word": "Brisk",
        "meaning": "활발한, 빠른 (기분 좋게 빠른)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "31c40d02-3875-493d-9a26-ea161787fb82",
        "word": "Accelerated",
        "meaning": "가속화된 (점점 빨라지는)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "b7abaaa2-8821-46c3-9223-6aa34f3eb78e",
        "word": "Pace",
        "meaning": "속도 (걸음걸이나 진행 속도)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "87c9ca91-a7a2-4e46-a545-2d5864c16849",
        "word": "Tempo",
        "meaning": "템포, 박자 (활동의 빠르기)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "6dcd5e5f-e523-4427-a989-2454955acc53",
        "word": "Lag",
        "meaning": "지체, 뒤처짐 (시간 차이)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "4c79d1af-ec6a-483c-b152-0828039a63e4",
        "word": "Procrastinate",
        "meaning": "미루다, 꾸물거리다 (해야 할 일을 늦추다)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "ae0cdc43-5329-45b0-acd9-d6ea9d1ec003",
        "word": "Defer",
        "meaning": "미루다, 연기하다 (결정을 나중으로)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    },
    {
        "card_id": "a8d31d77-e6b6-4b8c-a140-3c28c7d17fb3",
        "word": "Postpone",
        "meaning": "연기하다 (일정을 뒤로 늦추다)",
        "deck_id": "96a43bac-82b3-4e96-ab4d-dcef434bf07e",
        "deck_title": "TIMING_SPEED_PUNCTUALITY"
    }
]

RELEVANT_TAGS = [
    "planning",
    "restaurant",
    "activity",
    "social",
    "hobby",
    "sport",
    "marketing",
    "home",
    "daily_life",
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
- 위 태그들은 'TIMING_SPEED_PUNCTUALITY' 덱과 관련이 깊은 주제들입니다
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

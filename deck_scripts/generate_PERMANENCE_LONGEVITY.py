#!/usr/bin/env python3
"""
예문 생성 스크립트: PERMANENCE_LONGEVITY

이 스크립트는 'PERMANENCE_LONGEVITY' 덱의 단어들에 대해
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
    "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
    "deck_title": "PERMANENCE_LONGEVITY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "518e65e3-41ce-48e4-a2c4-dca95f26dc79",
        "word": "Eternal",
        "meaning": "영원한 (시작과 끝이 없는 불변의 상태)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "29bc1f32-ef91-429f-b2ac-bf4f4970a7ad",
        "word": "Perpetual",
        "meaning": "끊임없는, 영구적인 (멈추지 않고 계속 반복되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "c773fc4b-acd4-4d3e-a3b8-3a4d789d1a07",
        "word": "Everlasting",
        "meaning": "영속적인, 변치 않는 (끝없이 지속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "770bbd34-1ba8-48f3-b4aa-a6aedc8208a7",
        "word": "Infinite",
        "meaning": "무한한 (시간이나 공간의 끝이 없는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "eac576d1-ccec-4eed-a246-f256f01fc4a5",
        "word": "Enduring",
        "meaning": "오래가는, 지속되는 (어려움을 견디고 살아남은)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "33f87e9f-d52b-4a17-a241-3dbcab95cf55",
        "word": "Permanent",
        "meaning": "영구적인 (일시적이지 않고 고정된)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "91704b61-4738-4bef-8003-56c850fb4573",
        "word": "Chronic",
        "meaning": "만성적인 (병이나 나쁜 상태가 오래가는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "ec007511-23f5-43f2-b24e-3790ecaf2880",
        "word": "Prolonged",
        "meaning": "장기적인, 연장된 (예상보다 길어진)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "f0ee768d-c685-4ca3-bd1e-7c72f8907d39",
        "word": "Protracted",
        "meaning": "오래 끈, 지연된 (지루하게 길어진)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "217fc8f7-11cf-4d09-b4e9-ece52ce0b583",
        "word": "Incessant",
        "meaning": "끊임없는 (주로 부정적, 귀찮게 계속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "c8a79b8e-9910-4e82-8f9e-d3908d88fbdb",
        "word": "Ceaseless",
        "meaning": "그치지 않는 (쉬지 않고 계속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "c74867a4-5c0a-45d0-a0e0-3f6cb24d32d6",
        "word": "Unending",
        "meaning": "끝이 없는 (지겨울 정도로 계속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "b63a0ee8-82eb-46f3-86f6-ff423cae22ec",
        "word": "Timeless",
        "meaning": "세월이 흘러도 변치 않는 (유행을 타지 않는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "9dbb9768-ac55-4c7a-be59-db849723f1b7",
        "word": "Immortal",
        "meaning": "불멸의 (죽지 않는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "cd9cabf8-5a7e-4d5f-a676-bf63a9e8e9c8",
        "word": "Abiding",
        "meaning": "변함없는, 지속적인 (감정이나 신념이 오래가는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "541e0326-a50e-4bc1-b495-d9c091884e64",
        "word": "Persisting",
        "meaning": "지속되는, 고집하는 (없어지지 않고 남은)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "76cfab5f-eb28-495c-a3fd-2eecbd1c9862",
        "word": "Lingering",
        "meaning": "질질 끄는, 남아 있는 (떠나지 않고 머무는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "f365c466-6cea-4564-99ce-15be59d21bd0",
        "word": "Constant",
        "meaning": "지속적인, 변함없는 (늘 그 상태인)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "aba580f2-8766-404e-a33c-dd77d6690567",
        "word": "Continuous",
        "meaning": "연속적인 (중단 없이 쭉 이어지는 선 같은)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "d9c8815f-8a5d-48db-a2a6-5054137982f6",
        "word": "Continual",
        "meaning": "빈번한, 자꾸 계속되는 (단속적으로 자꾸 일어나는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "0d6c7ec4-2284-4cf4-98aa-cf2d511bd622",
        "word": "Sustained",
        "meaning": "지속된 (일정한 수준을 유지한)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "576ec804-53d8-40d1-96af-3fa37b21cda7",
        "word": "Extended",
        "meaning": "연장된, 장기간의 (늘어난)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "3f36c9e3-60b2-4b92-837d-6de226f8cfcb",
        "word": "Longevity",
        "meaning": "장수, 오래 지속됨 (수명)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "645f2feb-428d-496f-94db-fb2fabe274e2",
        "word": "Perennial",
        "meaning": "다년생의, 끊임없는 (해마다 계속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "93be99e6-d413-4bb9-80be-f59a4527afb0",
        "word": "Indefinite",
        "meaning": "무기한의 (끝이 정해지지 않은)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "ccc9fca5-6453-410a-9d90-f8cdf1c216ce",
        "word": "Deep-seated",
        "meaning": "뿌리 깊은 (오래되어 고치기 힘든)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "bdc01649-daa8-4e1d-bfd7-2469c8422cc8",
        "word": "Inveterate",
        "meaning": "상습적인, 만성의 (습관이 몸에 밴)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "8da006bd-faa5-4e84-b51c-3c21d38aeadd",
        "word": "Standing",
        "meaning": "상설의, 고정적인 (계속 유효한)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "076a13c6-7769-4794-b257-ddac1b5bbe92",
        "word": "Lifelong",
        "meaning": "평생의 (일생 동안 계속되는)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    },
    {
        "card_id": "b795555c-029d-4cb8-b715-6072eaab2b01",
        "word": "Undying",
        "meaning": "영원한, 불멸의 (죽지 않는 감정)",
        "deck_id": "1279880a-ef0e-4421-aca8-4728ccf161cf",
        "deck_title": "PERMANENCE_LONGEVITY"
    }
]

RELEVANT_TAGS = [
    "code",
    "technology",
    "happy",
    "fashion",
    "environment",
    "business",
    "time",
    "mood",
    "conversation",
    "hobby"
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
- 위 태그들은 'PERMANENCE_LONGEVITY' 덱과 관련이 깊은 주제들입니다
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

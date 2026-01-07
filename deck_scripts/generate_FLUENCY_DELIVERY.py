#!/usr/bin/env python3
"""
예문 생성 스크립트: FLUENCY_DELIVERY

이 스크립트는 'FLUENCY_DELIVERY' 덱의 단어들에 대해
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
    "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
    "deck_title": "FLUENCY_DELIVERY",
    "total_words": 29
}

WORDS = [
    {
        "card_id": "1808e718-7b44-48cf-96d2-b5932f787f6d",
        "word": "Eloquent",
        "meaning": "웅변적인, 감동적인",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "2403c4f9-cce9-4565-8572-0d635e7d0522",
        "word": "Resonant",
        "meaning": "울림이 있는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "f6abbc8b-0bfa-4dcc-9e90-6c7382381dce",
        "word": "Spontaneous",
        "meaning": "즉흥적인",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "439dbf22-137c-4e6e-9ca8-c96f6f683d84",
        "word": "Improvised",
        "meaning": "즉석에서 지어낸",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "ac39e85d-970f-46ca-9373-7207364dc8e1",
        "word": "Stutter",
        "meaning": "말을 더듬다",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "99b087c0-374f-4f6d-a17b-d00051ae3fd1",
        "word": "Stammer",
        "meaning": "말을 더듬다 (주저함)",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "a2ae70b9-1579-4543-b114-b8ce72f77af2",
        "word": "Mumble",
        "meaning": "웅얼거리다",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "0dd1c4ac-a43e-4106-ad10-67a646dca7d1",
        "word": "Rambling",
        "meaning": "횡설수설하는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "e8e3a97d-3e9f-4689-b25a-cf5efd3e26c6",
        "word": "Slur",
        "meaning": "(발음을) 얼버무리다",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "50756213-16f5-4c39-82ea-97d2435b79c6",
        "word": "Deliberate",
        "meaning": "신중한, 또박또박한",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "b1e4c2d4-b2c4-41f7-b0d3-c64821e24c58",
        "word": "Fluent",
        "meaning": "유창한",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "a887d93a-13e5-4ea7-8fd1-c6169632de12",
        "word": "Monotone",
        "meaning": "단조로운",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "0d58c2eb-27a8-4cde-9a6f-1cd25ddf3698",
        "word": "Expressive",
        "meaning": "표현력이 풍부한",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "7ad76e77-a136-4d4a-bd78-e94255f641c9",
        "word": "Dynamic",
        "meaning": "역동적인",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "22576211-ddd4-474d-b1ca-dbc7b66c9e23",
        "word": "Animated",
        "meaning": "생기 있는, 활기찬",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "03c68ddd-3514-495d-868c-0fbaac6c2b94",
        "word": "Audible",
        "meaning": "들리는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "5acdd0b2-1e30-4430-a1c0-a7abf2fc0b0a",
        "word": "Inaudible",
        "meaning": "들리지 않는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "5a7d40bc-175b-4ca7-9638-a3994482c59f",
        "word": "Shrill",
        "meaning": "새된, 찢어지는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "7f3dc99a-bca3-4498-bc76-9b18b95f2ec0",
        "word": "Husky",
        "meaning": "허스키한",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "554610f0-b9e2-4638-929a-573f6bd8474c",
        "word": "Soft-spoken",
        "meaning": "조곤조곤한, 목소리가 부드러운",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "01e7b563-927c-4c1b-9c20-8bcca665526b",
        "word": "Outspoken",
        "meaning": "거침없이 말하는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "d96ceccd-41ac-472f-9c92-72851e0be572",
        "word": "Vocal",
        "meaning": "목소리를 높이는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "945f4f8c-ee8d-4785-80bd-7fe6ba625034",
        "word": "Silver-tongued",
        "meaning": "언변이 좋은",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "47ba30ed-66be-4f5c-b2f8-d2ab715cee8e",
        "word": "Tongue-tied",
        "meaning": "꿀 먹은 벙어리가 된",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "1e8c60e1-0cbf-4f06-a25c-655c30171201",
        "word": "Hesitant",
        "meaning": "주저하는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "d499e3b4-14fd-46b3-8c3d-9006d83eb49d",
        "word": "Pausing",
        "meaning": "중간에 멈추는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "15e034e2-1b45-41f3-9b90-6f7c2f8764e9",
        "word": "Rhythmic",
        "meaning": "리듬감 있는",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "45b82386-ee53-4fb9-88f2-94a4d5c60f4b",
        "word": "Fast-paced",
        "meaning": "속도가 빠른",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    },
    {
        "card_id": "2513567c-3301-4f9a-ad5b-2fb1c311e79a",
        "word": "Measured",
        "meaning": "신중한, 정제된",
        "deck_id": "00f1a693-c06d-46f5-8e76-d501050f4b76",
        "deck_title": "FLUENCY_DELIVERY"
    }
]

RELEVANT_TAGS = [
    "ai",
    "social",
    "digital",
    "mood",
    "hobby",
    "fashion",
    "office",
    "movie",
    "warm",
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
- 위 태그들은 'FLUENCY_DELIVERY' 덱과 관련이 깊은 주제들입니다
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

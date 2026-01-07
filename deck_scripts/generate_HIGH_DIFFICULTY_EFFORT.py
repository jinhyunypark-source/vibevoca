#!/usr/bin/env python3
"""
예문 생성 스크립트: HIGH_DIFFICULTY_EFFORT

이 스크립트는 'HIGH_DIFFICULTY_EFFORT' 덱의 단어들에 대해
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
    "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
    "deck_title": "HIGH_DIFFICULTY_EFFORT",
    "total_words": 29
}

WORDS = [
    {
        "card_id": "e77f4585-26b5-4a23-919a-90e04a14461e",
        "word": "Arduous",
        "meaning": "몹시 힘든, 고된 (오랜 시간 끈기와 노력이 필요한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "fc5d60a3-2b3b-4314-b1dc-7c10593bd439",
        "word": "Laborious",
        "meaning": "힘든, 공이 많이 드는 (시간과 노동력이 많이 드는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "b0278a51-2134-4a7a-a60d-16cf73747f73",
        "word": "Strenuous",
        "meaning": "격렬한, 힘이 많이 드는 (많은 에너지를 쏟아야 하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "4f7c4d47-c7fd-41cf-b94d-a2a70dfdb8d0",
        "word": "Grueling",
        "meaning": "녹초로 만드는, 엄한 (극한까지 몰아붙이는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "5b8bae85-2cef-4ba2-a13a-4e002d09d00e",
        "word": "Demanding",
        "meaning": "요구가 많은, 벅찬 (높은 수준의 노력/기술을 요하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "530c5cad-65f9-4d25-af69-0874035fb0b6",
        "word": "Formidable",
        "meaning": "어마어마한, 버거운 (상대하기 무섭고 벅찬)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "99dfa1d6-4009-43aa-ab39-434f101a290e",
        "word": "Onerous",
        "meaning": "아주 힘든, 부담스러운 (짐처럼 느껴지는 책임/의무)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "b71aef9e-6eaa-41cb-9d5d-917476751bba",
        "word": "Taxing",
        "meaning": "아주 힘든, 무리한 (심신을 지치게 하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "46ec8d96-1f2a-405d-b0f3-a519359a3c53",
        "word": "Backbreaking",
        "meaning": "등골이 휘는 (육체적으로 매우 고된)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "b3365c0a-659d-4983-9dd7-840dcbefe66c",
        "word": "Challenging",
        "meaning": "도전적인, 만만치 않은 (어렵지만 해볼 만한 가치가 있는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "8cb51063-a256-4feb-8523-931c82e24cf1",
        "word": "Burdensome",
        "meaning": "부담스러운 (짐이 되는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "57d394f9-b039-4360-bf9a-089962ceccf9",
        "word": "Punishing",
        "meaning": "살인적인, 극도로 힘든 (몸을 혹사시키는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "1a3df385-2aa3-4931-8fab-99befbc202d5",
        "word": "Rigorous",
        "meaning": "엄격한, 철저한 (빈틈없고 힘든 기준)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "7c7dd37a-d61c-41d2-ae26-329b3cd532dc",
        "word": "Exacting",
        "meaning": "힘든, 까다로운 (정확성을 엄격히 요구하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "4951bd13-3123-4ec5-bafb-ebc6e3b57bde",
        "word": "Tough",
        "meaning": "힘든, 거친 (어렵고 곤란한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "6e319580-47e4-4982-81cc-0e6beaabc8ac",
        "word": "Tricky",
        "meaning": "까다로운, 교묘한 (실수하기 쉽고 다루기 힘든)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "10a10b8c-5950-4d86-99e9-97e633ba1510",
        "word": "Thorny",
        "meaning": "골치 아픈, 가시밭길 같은 (문제나 논쟁이 많은)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "898aa0be-d96b-4033-b937-57f59ee24bee",
        "word": "Problematic",
        "meaning": "문제가 있는, 확실치 않은 (해결이 어려운)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "7cf0c531-5aa7-462c-9172-dfc80fd878f2",
        "word": "Uphill",
        "meaning": "힘겨운, 오르막의 (투쟁이나 노력이 필요한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "da848f7c-4a6f-4941-804a-2153a0d7cfc5",
        "word": "Insuperable",
        "meaning": "극복할 수 없는 (도저히 넘을 수 없는 장애물)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "942d5177-2ec5-43d3-9ee5-7efbd9019acb",
        "word": "Impossible",
        "meaning": "불가능한 (실현될 수 없는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "5735e282-b686-4a46-b2be-969219d2e0c4",
        "word": "Herculean",
        "meaning": "초인적인 (헤라클레스 같은 힘이 필요한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "801ecc91-51f7-4d35-9742-aab824b2ae8e",
        "word": "Painstaking",
        "meaning": "공들인, 힘든 (세심한 주의와 노력이 필요한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "9b31d3ec-3790-495e-9dc0-3242af3ccf15",
        "word": "Exhausting",
        "meaning": "진이 빠지는 (체력을 다 소모하게 하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "f53a698e-0952-4cf3-8ca6-cf18df55e2c8",
        "word": "Trying",
        "meaning": "괴로운, 시련을 주는 (인내심을 시험하는)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "471da5d0-ba71-4bdd-898f-951330a5bf91",
        "word": "Severe",
        "meaning": "심각한, 가혹한 (어려움의 정도가 심한)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "7ea22579-4d4a-464c-8148-15ffac332f85",
        "word": "Steep",
        "meaning": "가파른, 터무니없는 (너무 높거나 어려운)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "48875b03-bdf7-4698-ad38-04b0992f37d9",
        "word": "Rough",
        "meaning": "거친, 힘든 (순탄치 않은)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    },
    {
        "card_id": "400ab95a-50be-4777-b8c2-ff83571657d1",
        "word": "Crucial",
        "meaning": "결정적인 (어렵고 중대한 기로에 선)",
        "deck_id": "783c6a5b-7e66-4744-9378-0f4a0f9cc93c",
        "deck_title": "HIGH_DIFFICULTY_EFFORT"
    }
]

RELEVANT_TAGS = [
    "study",
    "education",
    "friendship",
    "medical",
    "develope",
    "startup",
    "internet",
    "entrepreneur",
    "style",
    "interview"
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
- 위 태그들은 'HIGH_DIFFICULTY_EFFORT' 덱과 관련이 깊은 주제들입니다
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

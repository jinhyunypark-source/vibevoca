#!/usr/bin/env python3
"""
예문 생성 스크립트: MINUTENESS_SMALLNESS

이 스크립트는 'MINUTENESS_SMALLNESS' 덱의 단어들에 대해
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
    "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
    "deck_title": "MINUTENESS_SMALLNESS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "78623627-03f6-4bc8-a5b7-95a064899f33",
        "word": "Tiny",
        "meaning": "아주 작은 (Small보다 더 작은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "5e856850-f4c3-4791-bfcd-df03fe059985",
        "word": "Miniscule",
        "meaning": "극소의 (너무 작아서 잘 안 보이는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "e245d526-5a77-4462-9886-94ea2db4151a",
        "word": "Microscopic",
        "meaning": "현미경으로 봐야 할 (눈에 안 보이는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "b001ea9d-2177-48c8-abfe-30851610966a",
        "word": "Minute",
        "meaning": "미세한, 상세한 (발음: 마이뉴트)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "9c08c6e2-d851-462e-925f-94d80c91a5e8",
        "word": "Diminutive",
        "meaning": "자그마한 (귀엽거나 약해 보일 정도로 작은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "a9c08107-7cba-4a0b-989c-b7c8cb4f22f5",
        "word": "Petite",
        "meaning": "아담한 (주로 여성의 체구가 작고 맵시 있는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "855bac37-a1cd-4084-af00-4f724668c57c",
        "word": "Compact",
        "meaning": "소형의, 콤팩트한 (작게 뭉쳐진)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "6ff72dbb-0974-4dfb-83c4-4eb79834ff1f",
        "word": "Miniature",
        "meaning": "축소된, 소형의 (실물을 작게 만든)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "fbc3f6f5-8028-4b74-8fbb-8a04ce5ea607",
        "word": "Teeny",
        "meaning": "정말 작은 (구어체) (아주아주 작은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "658c3716-1ac5-42db-8391-4a61be6bbe19",
        "word": "Wee",
        "meaning": "조그마한 (스코틀랜드 방언)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "fa9955f9-6079-4ddd-862b-0d2bfdea415f",
        "word": "Puny",
        "meaning": "작고 연약한, 하찮은 (보잘것없는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "889f3860-017f-4172-b4e5-b1176ba1dd27",
        "word": "Slight",
        "meaning": "약간의, 가냘픈 (정도가 약한)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "7accb0d9-2f4f-449f-b930-9e3c536b7a26",
        "word": "Marginal",
        "meaning": "미미한, 주변부의 (중요하지 않은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "ee2007ce-e30e-46c5-a38f-54219e6a0337",
        "word": "Negligible",
        "meaning": "무시해도 될 정도의 (양이 아주 적은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "8e551d97-6ed5-4ecf-baa0-f21a85e39d72",
        "word": "Minimal",
        "meaning": "최소한의 (가장 적은 양의)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "e98fd7ff-fff0-48a2-b091-a66318fdd4e3",
        "word": "Nominal",
        "meaning": "명목상의, 얼마 안 되는 (이름뿐인)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "4b26c32c-488b-4f0a-8ad2-548da3c5e5dd",
        "word": "Insubstantial",
        "meaning": "실체가 없는, 빈약한 (튼튼하지 않은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "fca878b2-7e06-48f2-93e5-256c426a219e",
        "word": "Trifling",
        "meaning": "하찮은 (가치가 거의 없는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "5304ca47-9274-47e6-b2da-6c26442d8950",
        "word": "Fine",
        "meaning": "가느다란, 미세한 (입자가 고운)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "f683ed75-bf44-47bd-aac8-e754994ad673",
        "word": "Thin",
        "meaning": "얇은, 가는 (두께가 없는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "bf94e331-d9f5-4e05-9887-fd2b01c567eb",
        "word": "Slender",
        "meaning": "날씬한, 가느다란 (길고 가는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "96138bcb-174f-41f8-9317-2345d4fed7f3",
        "word": "Narrow",
        "meaning": "좁은 (폭이 좁은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "2854ae15-e6f2-472c-b470-e6022ee9f2af",
        "word": "Limited",
        "meaning": "제한된 (양이 정해져 있는)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "4fc7350d-4838-42a4-bffe-ec855a70229d",
        "word": "Restricted",
        "meaning": "제한된, 좁은 (범위가 좁은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "6cbbbf22-28b7-4015-bade-2b55814d3b9d",
        "word": "Atomic",
        "meaning": "원자의, 극소의 (원자만큼 작은)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "576086f6-b8a5-4c19-ba36-82ce2e069b8f",
        "word": "Molecular",
        "meaning": "분자의 (분자 수준의)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "f2bd6b0a-58ed-4973-9f47-31e6d4d33db6",
        "word": "Nano",
        "meaning": "나노의 (10억분의 1, 아주 미세한)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "c16c4497-182c-4eb0-bdc7-6f5be1bb125d",
        "word": "Pocket-sized",
        "meaning": "주머니에 들어가는 (휴대용의)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "f0728092-9076-4a4e-8e18-8cd4a86d0e39",
        "word": "Bite-sized",
        "meaning": "한입 크기의 (작게 나눈)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    },
    {
        "card_id": "5b5a447a-29ef-4048-8a06-f108d2fccca7",
        "word": "Fractional",
        "meaning": "아주 적은, 단편적인 (부분적인)",
        "deck_id": "bfb3c473-65fe-4252-9dd2-16f0bf166eee",
        "deck_title": "MINUTENESS_SMALLNESS"
    }
]

RELEVANT_TAGS = [
    "medical",
    "digital",
    "movie",
    "restaurant",
    "interview",
    "develope",
    "university",
    "sad",
    "nature",
    "office"
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
- 위 태그들은 'MINUTENESS_SMALLNESS' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: COOPERATION_HARMONY

이 스크립트는 'COOPERATION_HARMONY' 덱의 단어들에 대해
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
    "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
    "deck_title": "COOPERATION_HARMONY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "0a3ca1f7-21b0-4c96-b01c-46ce08516252",
        "word": "Compatible",
        "meaning": "잘 맞는, 호환되는 (성격이나 의견이 잘 통하는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "f159eba3-e05c-47a6-8cb5-4fc9aa6c6eec",
        "word": "Harmonious",
        "meaning": "조화로운 (다툼 없이 평화로운)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "01a67991-ae24-47ba-9a2c-3edef2813305",
        "word": "Cooperative",
        "meaning": "협조적인 (기꺼이 돕는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "7d953e30-75b5-4e72-a65c-212d92a54910",
        "word": "Reciprocal",
        "meaning": "상호 간의 (주고받는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "d89789c3-14b1-47a4-b9e0-0abd40626cae",
        "word": "Cordial",
        "meaning": "화기애애한, 정중한 (따뜻하지만 격식 있는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "6c8ebdc6-a0be-4a46-8a2f-1451262bf3c5",
        "word": "Amicable",
        "meaning": "원만한 (우호적인 방식으로 해결하는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "513161c8-ed11-4fdf-bd30-cead79c6b148",
        "word": "Collaborative",
        "meaning": "협력적인 (함께 일해서 만드는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "f93b1d6d-3ac9-4c21-9125-790b4d188f02",
        "word": "Supportive",
        "meaning": "지지하는, 힘이 되는 (도와주고 응원하는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "703e465a-def0-49c7-aad6-17186363d660",
        "word": "Loyal",
        "meaning": "충성스러운, 의리 있는 (배신하지 않는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "316e3734-f4fc-48ee-86c7-7c945bc22128",
        "word": "Trustworthy",
        "meaning": "신뢰할 수 있는 (믿음직한)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "acad5701-a9e6-43bc-9a73-0a4894e8b59e",
        "word": "Reliable",
        "meaning": "믿을 만한 (일을 맡길 수 있는/일관된)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "4635c96e-d8ec-4e1f-a481-0ba8ec257ae7",
        "word": "Dependable",
        "meaning": "의지할 수 있는 (필요할 때 곁에 있는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "a88e3eae-d18a-47bd-be67-b412cd1b7ecf",
        "word": "Helpful",
        "meaning": "도움이 되는 (유용한)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "4de9a8d0-6bf6-42f2-bc40-1d03e956175d",
        "word": "Allied",
        "meaning": "동맹을 맺은 (같은 편인)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "0cbb09be-5662-48fc-a340-252e14018b5f",
        "word": "United",
        "meaning": "단결된 (하나로 뭉친)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "27d234db-08ea-48be-b3e2-10ae454ffa4e",
        "word": "Cohesive",
        "meaning": "화합하는, 결속력 있는 (단단히 뭉친)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "010e836a-6a6e-4c07-99aa-96d67a3d9ef2",
        "word": "Mutual",
        "meaning": "상호 간의, 공통의 (서로 똑같이 느끼는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "d345f638-7cfc-4f6c-90b8-df935cd156f1",
        "word": "Understanding",
        "meaning": "이해심 있는 (남의 사정을 봐주는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "0e7dd8b0-06e8-4014-a540-2c0069951e27",
        "word": "Sympathetic",
        "meaning": "공감하는, 동정적인 (마음을 알아주는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "597bb87c-312b-4e0b-9946-6af9fd29d0a0",
        "word": "Considerate",
        "meaning": "사려 깊은 (남을 배려하는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "c4762135-8508-4876-99f4-8a088e082e30",
        "word": "Tolerant",
        "meaning": "관대한 (다른 점을 용인하는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "8f617de2-1836-441d-bb0d-d3c49d183446",
        "word": "Accommodating",
        "meaning": "편의를 봐주는, 잘 맞춰주는",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "1537ad0b-c2eb-4ebd-937e-9227ef519f43",
        "word": "Agreeable",
        "meaning": "동조하는, 쾌활한 (잘 따르는/기분 좋은)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "427628fd-92ff-4ec7-8322-99742344fa02",
        "word": "Civil",
        "meaning": "예의 바른 (친하진 않아도 예의는 지키는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "eb0a60b0-52b5-4d76-854c-be6641189d5e",
        "word": "Polite",
        "meaning": "공손한 (예절을 지키는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "5291f880-6942-4ace-b0fe-896b5a315e5e",
        "word": "Courteous",
        "meaning": "정중한 (매우 예의 바르고 배려심 있는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "380596aa-30ac-4028-9508-bbc6c5914707",
        "word": "Friendly",
        "meaning": "우호적인 (친근한)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "2db1ccfc-3bfa-4c2c-8aa1-6ae2b38e3ce5",
        "word": "Constructive",
        "meaning": "건설적인 (도움이 되는 방향의)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "02dd54c7-0e42-4155-a88b-1eb05a073bf6",
        "word": "Synergistic",
        "meaning": "시너지 효과가 있는 (함께해서 더 큰 효과를 내는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    },
    {
        "card_id": "931ebad9-7868-4d60-bddf-2751cbe35ca0",
        "word": "Integrated",
        "meaning": "통합된 (서로 잘 섞이는)",
        "deck_id": "85e04ae3-8e14-4eb0-a76d-bcb762586648",
        "deck_title": "COOPERATION_HARMONY"
    }
]

RELEVANT_TAGS = [
    "school",
    "food",
    "friendship",
    "movie",
    "develope",
    "marketing",
    "outdoor",
    "restaurant",
    "university",
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
- 위 태그들은 'COOPERATION_HARMONY' 덱과 관련이 깊은 주제들입니다
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

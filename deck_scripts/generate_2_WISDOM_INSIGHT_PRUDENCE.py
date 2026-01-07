#!/usr/bin/env python3
"""
예문 생성 스크립트: 2_WISDOM_INSIGHT_PRUDENCE

이 스크립트는 '2_WISDOM_INSIGHT_PRUDENCE' 덱의 단어들에 대해
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
    "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
    "deck_title": "2_WISDOM_INSIGHT_PRUDENCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "4e79001b-db0f-43a0-a009-2b83c412985c",
        "word": "Deep",
        "meaning": "깊은, 난해한 (생각이 깊은)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "e225b6b7-a2c5-456f-9dd1-24d16c86c5a5",
        "word": "Sage",
        "meaning": "현명한, 성인 같은 (매우 깊은 지혜)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "b8e5ce46-7ddc-44b3-848d-00e69a4b52a2",
        "word": "Sagacious",
        "meaning": "총명한, 현명한 (예리한 판단력, 격식) > sage 현자",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "3d7a4680-3cac-42e2-b76e-d052bde4a577",
        "word": "Prudent",
        "meaning": "신중한 (미래를 대비하고 조심하는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "4e86bfb9-dd94-43e9-bcb2-30a918019f8d",
        "word": "Discriminating",
        "meaning": "안목 있는  and 차별하는.  crit(분리,나누다)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "84794798-40ac-4f74-9ecf-1a0772f2565f",
        "word": "criticize",
        "meaning": "비평하다",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "5bd21c20-b391-478f-91eb-4785489f0840",
        "word": "Discerning",
        "meaning": "식견이 있는 (좋은 것을 알아보는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "c9b40cca-d4d2-43c7-999d-8e95e626ff11",
        "word": "Judicious",
        "meaning": "판단력 있는 (신중하고 적절한)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "7cb2b8af-769a-4e45-b65d-5618bb69ce4f",
        "word": "Contemplative",
        "meaning": "사색/관조 하는  con(함께+template(신당)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "76c40bbf-bf06-41d3-872b-3c3883bcab5d",
        "word": "Pensive",
        "meaning": "수심에 잠긴 (약간 슬프게 깊은 생각)  (라)pendere 매달리다",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "33500cb1-7a7d-4cd0-9797-e87efedc4f57",
        "word": "pendium",
        "meaning": "시계추",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "e7c373b2-6e88-4776-90b2-5e2a75f28b65",
        "word": "Intuitive",
        "meaning": "직관적인 (설명보다 감각으로 아는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "1b5d8c61-65b4-4e93-84eb-f313572cc9d1",
        "word": "Sensible",
        "meaning": "분별 있는 (상식에 맞고 실용적인)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "6fce9b2d-259c-46d5-a814-6fa3a264672b",
        "word": "Reasonable",
        "meaning": "합리적인 (이치에 맞고 과하지 않은)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "3650141b-f0ed-469b-8946-a5c70d5f9d0a",
        "word": "Rational",
        "meaning": "이성적인 (감정에 휘둘리지 않는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "a53a36d8-a7f1-476d-8705-6637ad1edfb0",
        "word": "Logical",
        "meaning": "논리적인 (인과 관계가 맞는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "fb784c1f-7215-4efd-8366-3238ee9837ae",
        "word": "Sound",
        "meaning": "건전한, 타당한 (판단력이 흠잡을 데 없는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "c20bed36-b802-42a0-8ff7-ed8696f86d0b",
        "word": "Insightful",
        "meaning": "통찰력 있는 (본질을 꿰뚫어 보는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "39246dff-7cce-4334-85c7-16486593291b",
        "word": "Perceptive",
        "meaning": "지각력이 예민한 (남이 못 보는 것을 알아채는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "3146714c-c88e-4273-8ae7-adfc1853b9df",
        "word": "Prescient",
        "meaning": "예지력 있는 (일어날 일을 미리 아는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "960b53ad-01a9-4390-be62-a9069a78ce74",
        "word": "Observant",
        "meaning": "관찰력 있는 (주의 깊게 보고 놓치지 않는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "0276981b-dacf-4012-8795-1fa2cf94c167",
        "word": "Profound",
        "meaning": "심오한 (깊이가 있는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "205c79bc-3b26-4d3d-bc5d-87e40b4a8936",
        "word": "Philosophical",
        "meaning": "철학적인 (인생의 이치를 생각하는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "633a695b-6e3d-4195-9cb8-c4d75e3f8ca6",
        "word": "Enlightened",
        "meaning": "계몽된, 깨우친 (편견 없고 지혜로운)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "c2114dab-1189-4efe-a479-9d43728837d3",
        "word": "Visionary",
        "meaning": "선견지명 있는 (미래를 내다보는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "6f5dd3be-75e5-470b-ad29-e05043f6ecb7",
        "word": "Far-sighted",
        "meaning": "미래를 내다보는 (장기적인 안목)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "4dd0b7fa-f3d2-4ddd-bb08-6275085b8330",
        "word": "Thoughtful",
        "meaning": "사려 깊은 (신중하게 생각하는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "e90df609-312d-448f-8815-8020b6281348",
        "word": "Reflective",
        "meaning": "성찰하는 (자신을 되돌아보는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "54a1b64c-f2bf-480e-a38c-f77b847e8008",
        "word": "Meditative",
        "meaning": "명상적인 (깊은 생각에 잠긴)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    },
    {
        "card_id": "ec1d8a7e-1f20-435f-b71d-7cae7fab1557",
        "word": "Introspective",
        "meaning": "내성적인, 자기를 관찰하는 (내면을 들여다보는)",
        "deck_id": "79ea45bb-6bbf-4bc5-ad18-4859a9dd83a2",
        "deck_title": "2_WISDOM_INSIGHT_PRUDENCE"
    }
]

RELEVANT_TAGS = [
    "conversation",
    "code",
    "work",
    "startup",
    "school",
    "schedule",
    "mood",
    "home",
    "soccer",
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
- 위 태그들은 '2_WISDOM_INSIGHT_PRUDENCE' 덱과 관련이 깊은 주제들입니다
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

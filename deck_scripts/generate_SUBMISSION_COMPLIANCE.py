#!/usr/bin/env python3
"""
예문 생성 스크립트: SUBMISSION_COMPLIANCE

이 스크립트는 'SUBMISSION_COMPLIANCE' 덱의 단어들에 대해
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
    "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
    "deck_title": "SUBMISSION_COMPLIANCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "62e8216b-49e8-4a77-b6c8-1ee981950553",
        "word": "Subservient",
        "meaning": "굴종하는, 비굴한 (지나치게 남의 눈치를 보며 복종하는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "8152cdb5-b098-4462-bcb1-d8047f4a4b42",
        "word": "Submissive",
        "meaning": "순종적인 (권위에 저항 없이 따르는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "2d1d76b4-f364-4950-ba63-c2b70aa3f140",
        "word": "Obedient",
        "meaning": "말 잘 듣는 (규칙이나 명령을 지키는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "361c865e-eee3-43e9-99fd-96e6fa8a03fd",
        "word": "Compliant",
        "meaning": "준수하는, 고분고분한 (요구대로 따르는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "e42eab17-e65c-4a7f-962b-cc54a0c9c084",
        "word": "Docile",
        "meaning": "유순한, 다루기 쉬운 (성격이 온순한)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "06f87070-3e42-49f6-a4bb-c4c3ad2f6877",
        "word": "Acquiescent",
        "meaning": "묵인하는 (마지못해 따르는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "5a7ae911-88d5-4119-8815-018d4484ec88",
        "word": "Passive",
        "meaning": "수동적인 (스스로 행동하지 않고 당하는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "9a4ad2c1-5b9d-470b-9a0b-dad4d9052743",
        "word": "Meek",
        "meaning": "온순한, 기가 죽은 (자기를 내세우지 않는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "f358a3c8-02e1-482e-beff-0660f40a5221",
        "word": "Yielding",
        "meaning": "양보하는, 유연한 (압력에 굴복하는/잘 휘는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "7feff3ce-13f0-42c2-852f-64d378570be1",
        "word": "Resigned",
        "meaning": "체념한 (피할 수 없음을 받아들이는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "cf89c5d6-f239-4da3-b2e9-2e95c8113804",
        "word": "Deferential",
        "meaning": "경의를 표하는 (윗사람을 존중하여 따르는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "588a0510-e147-4d7d-8202-51f2657f893f",
        "word": "Inferior",
        "meaning": "하등의, 열등한 (지위나 질이 낮은)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "0738e0e0-f20c-4a15-89a9-4815c386d1bd",
        "word": "Subordinate",
        "meaning": "종속된, 부하의 (지위가 아래인)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "a5c6997f-9268-4f7c-b7b0-c77dc49c3bc4",
        "word": "Dependent",
        "meaning": "의존적인 (남에게 기대는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "9af1c906-640f-4ed1-a9b2-10ee58230865",
        "word": "Servile",
        "meaning": "굽실거리는, 노예 근성의 (자존심 없이 비굴한)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "33bccefd-44d1-4b6e-9c3d-cce17d4eb2f0",
        "word": "Slavish",
        "meaning": "노예적인, 맹종하는 (줏대 없이 따라 하는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "e6b65e39-08a8-4d4c-b3b6-4c542c386b35",
        "word": "Tame",
        "meaning": "길들여진 (야성이 없고 순한)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "ac710e64-c71d-4f26-81e2-bb86c5c1b695",
        "word": "Controlled",
        "meaning": "통제된, 억제된 (자유가 없는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "a5c44f38-7631-425b-90c8-edba3d7d6bc1",
        "word": "Obeisant",
        "meaning": "정중하게 복종하는 (격식, 경의를 표하는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "f530a7e8-3004-484a-a94a-ecad799a8983",
        "word": "Powerless",
        "meaning": "무력한 (힘이 없는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "e2594092-6c51-4fea-9874-6b72a2ac8c27",
        "word": "Weak",
        "meaning": "약한 (신체적/정신적으로 힘이 부족한)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "602ffa8d-aa46-4436-870f-66eed41c49fb",
        "word": "Vulnerable",
        "meaning": "취약한 (상처받기 쉬운)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "4723303b-5682-4a6a-be5d-4661deb57118",
        "word": "Defenseless",
        "meaning": "무방비의 (방어할 수 없는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "f46d725f-1701-4287-933b-0cad5b5a991b",
        "word": "Subject",
        "meaning": "지배를 받는, 신하 (왕이나 법의 통제하에 있는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "12333f67-ced3-41d7-b956-8b6b8786f837",
        "word": "Underling",
        "meaning": "아랫사람, 졸개 (비하하는 뉘앙스)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "acc1797f-49f2-419f-b6d4-e2217c4acb97",
        "word": "Follower",
        "meaning": "추종자, 팔로워 (리더를 따르는 사람)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "76ff0d9c-ae32-48ba-8f51-8bcf6c93219a",
        "word": "Pliant",
        "meaning": "유순한, 잘 휘는 (남의 말에 쉽게 좌우되는)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "ca56cb67-bf0a-40b1-904e-8b51cdf7b20e",
        "word": "Malleable",
        "meaning": "영향받기 쉬운, 가소성이 있는 (모양을 바꾸기 쉬운)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "f3971bba-8a66-434a-953f-88c72199dbd5",
        "word": "Timid",
        "meaning": "소심한 (겁이 많은)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    },
    {
        "card_id": "734acea2-3431-4092-83c3-fb739715bcec",
        "word": "Ungovernable",
        "meaning": "통제 불능의 (다스리기 힘든 - *반항적 뉘앙스*)",
        "deck_id": "7c5c4c23-531a-43ab-9938-d96a2767af3d",
        "deck_title": "SUBMISSION_COMPLIANCE"
    }
]

RELEVANT_TAGS = [
    "office",
    "restaurant",
    "code",
    "movie",
    "university",
    "marketing",
    "job",
    "art",
    "time",
    "environment"
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
- 위 태그들은 'SUBMISSION_COMPLIANCE' 덱과 관련이 깊은 주제들입니다
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

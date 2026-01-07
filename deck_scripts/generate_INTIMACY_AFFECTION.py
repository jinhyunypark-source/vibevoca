#!/usr/bin/env python3
"""
예문 생성 스크립트: INTIMACY_AFFECTION

이 스크립트는 'INTIMACY_AFFECTION' 덱의 단어들에 대해
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
    "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
    "deck_title": "INTIMACY_AFFECTION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "2788f9b5-cf41-41a2-8a23-6d884d797f42",
        "word": "Tender",
        "meaning": "상냥한, 부드러운 (조심스럽고 다정한)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "f8213c69-3dc9-49e6-affb-42d9541f8d81",
        "word": "Intimate",
        "meaning": "친밀한, 사적인 (매우 가깝고 깊은 관계)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "8df3f44d-83e7-4661-b845-37ded923bbd7",
        "word": "Fraternal",
        "meaning": "형제애의, 우애 깊은 (형제 같은)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "c7699e8b-ec39-4d7f-b103-33205a7782ad",
        "word": "Close",
        "meaning": "가까운 (정서적/물리적으로 친한)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "ba19fdf5-4c68-49ac-89f2-79900526c746",
        "word": "Affectionate",
        "meaning": "다정한, 애정 어린 (사랑을 표현하는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "aa143f06-0729-444b-9018-3d6ce0b04579",
        "word": "Loving",
        "meaning": "사랑하는, 애정이 깊은 (따뜻한 마음)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "69ec077c-04e5-45ae-92eb-9faecbdad509",
        "word": "Devoted",
        "meaning": "헌신적인 (깊은 사랑으로 충성하는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "25b430fb-4c0f-477e-ab0e-599e281dc383",
        "word": "Platonic",
        "meaning": "정신적인 사랑의 (육체적 관계가 없는 순수한)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "7261db9b-b38b-4405-b2b6-07d2f56a7729",
        "word": "Romantic",
        "meaning": "로맨틱한, 연애의 (남녀 간의 사랑)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "df5709cf-7f22-4865-ac41-cd5223261037",
        "word": "Passionate",
        "meaning": "열정적인 (감정이 격렬하고 뜨거운)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "0ab6bb26-7196-4d10-a24b-b8e65d390167",
        "word": "Inseparable",
        "meaning": "떼려야 뗄 수 없는 (늘 붙어 다니는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "03beadf6-fe85-40e9-aa85-6430dc2710d8",
        "word": "Bonded",
        "meaning": "유대감이 형성된 (깊이 연결된)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "ba062bc5-da6e-4b9f-b344-230400dba927",
        "word": "Attached",
        "meaning": "애착을 가진 (정서적으로 달라붙은)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "168e56ab-7163-4a2c-b324-13acdfa36de4",
        "word": "Close-knit",
        "meaning": "긴밀하게 맺어진 (구성원 간 사이가 끈끈한)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "33a9748d-431e-4506-a5c7-2eaab46697bc",
        "word": "Familial",
        "meaning": "가족적인 (가족 같은 유대감의)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "73645137-0454-4b9c-8a46-3db38e7954a4",
        "word": "Maternal",
        "meaning": "모성애의, 어머니 같은 (보살피는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "28e79aef-1245-499b-98aa-5b6f9addd5be",
        "word": "Confidant",
        "meaning": "(라)fides 믿음,  절친한 친구, 막역한 사이 (비밀을 털어놓는 상대)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "c7d085a9-721c-4c4d-881b-bed54b8c148a",
        "word": "Paternal",
        "meaning": "부성애의, 아버지 같은 (보호하는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "9b955d7d-983d-4091-8e1a-e011a04bab41",
        "word": "Cherished",
        "meaning": "소중히 여겨지는 (아끼고 사랑받는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "5c047685-3dcb-456c-beac-9a0a3ea935d8",
        "word": "Beloved",
        "meaning": "사랑하는, 총애받는 (매우 사랑받는 대상)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "b96a1350-8dd5-42e9-83dc-2fed6992d617",
        "word": "Adoring",
        "meaning": "흠모하는, 아주 좋아하는 (사랑과 존경이 섞인)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "72dd24cb-5f59-44e4-8e0b-497b3e803017",
        "word": "Dear",
        "meaning": "소중한, 친애하는 (가깝고 아끼는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "a93ba96e-d516-45a3-b205-01f57a712b28",
        "word": "Fond",
        "meaning": "좋아하는, 다정한 (은근한 애정)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "0faf3648-047b-4df1-9885-5260da309c2c",
        "word": "Warm",
        "meaning": "따뜻한 (정이 많고 친절한)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "82ed3114-2afb-46fd-89bc-346bfcde660d",
        "word": "Soulmate",
        "meaning": "소울메이트, 영혼의 단짝 (영혼이 통하는 상대)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "ffbe7cb5-5afc-4798-94e4-382b51a2d75f",
        "word": "Companion",
        "meaning": "동반자, 말동무 (함께 시간을 보내는 사람)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "2cc016c4-4d49-4092-a9d3-6a10b7025363",
        "word": "Partner",
        "meaning": "반려자, 파트너 (삶이나 일을 함께하는)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "f34a4f4f-3aba-42dc-b31c-eb003bf93a97",
        "word": "Spouse",
        "meaning": "배우자 (남편이나 아내, 법적 용어)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "0da4e812-4f68-4042-9a82-00336d1fef6a",
        "word": "Significant other",
        "meaning": "연인, 배우자 (중요한 타인/파트너)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    },
    {
        "card_id": "a9658d44-09bd-4f90-ab07-7001d4c431a3",
        "word": "Buddy",
        "meaning": "친구, 단짝 (구어체) (편한 친구)",
        "deck_id": "36aed428-e1b3-48f1-98c8-d7279486d05a",
        "deck_title": "INTIMACY_AFFECTION"
    }
]

RELEVANT_TAGS = [
    "home",
    "exercise",
    "entrepreneur",
    "conversation",
    "outdoor",
    "mood",
    "study",
    "code",
    "office",
    "shopping"
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
- 위 태그들은 'INTIMACY_AFFECTION' 덱과 관련이 깊은 주제들입니다
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

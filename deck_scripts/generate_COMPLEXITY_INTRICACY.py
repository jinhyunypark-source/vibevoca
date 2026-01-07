#!/usr/bin/env python3
"""
예문 생성 스크립트: COMPLEXITY_INTRICACY

이 스크립트는 'COMPLEXITY_INTRICACY' 덱의 단어들에 대해
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
    "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
    "deck_title": "COMPLEXITY_INTRICACY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "65d97fc6-1897-4dd6-ae8a-f3fb24a1e159",
        "word": "Complex",
        "meaning": "복잡한 (여러 부분이 섞여 있어 이해가 필요한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "d34da5bc-52ff-4e98-a51f-9f1ea87cace5",
        "word": "Complicated",
        "meaning": "복잡한 (이해하거나 풀기 까다로운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "b8c369a0-30f6-4fc8-8aef-83530d43ffb6",
        "word": "Intricate",
        "meaning": "얽히고설킨, 정교한 (세부 사항이 많고 미세한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2637a38b-66a3-42eb-9926-e009a77302b1",
        "word": "Convoluted",
        "meaning": "대단히 난해한, 꼬인 (너무 꼬여서 이해하기 힘든)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "a7eb4c72-eac7-4794-bf39-96a5e56b1082",
        "word": "Labyrinthine",
        "meaning": "미로 같은 (길을 잃을 만큼 복잡한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "b5c5d959-809d-48e8-9bac-cb92a18931b7",
        "word": "Tortuous",
        "meaning": "구불구불한, 비틀린 (길이나 논리가 꼬인)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "7651a87d-902a-4ce9-b9a0-818310d5d7a7",
        "word": "Abstruse",
        "meaning": "난해한 (심오해서 이해하기 어려운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2321be35-bedd-4442-a82e-eef535942062",
        "word": "Involved",
        "meaning": "복잡한, 뒤얽힌 (많은 요소가 관련되어 까다로운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2ddb434b-8e18-49aa-9465-04eff5c0f25a",
        "word": "Knotty",
        "meaning": "매듭이 많은, 얽힌 (풀기 어려운 문제)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "32c14984-feaf-4cdf-8fc8-71b220a1e24f",
        "word": "Elaborate",
        "meaning": "정교한, 공들인 (복잡하게 짜인)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "4d552773-0fc9-4fd1-a196-b39f5f283b3a",
        "word": "Tangled",
        "meaning": "뒤엉킨 (실타래처럼 꼬인)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "a8294456-7166-4636-8525-0688e24360f5",
        "word": "Messy",
        "meaning": "지저분한, 골치 아픈 (상황이 정리되지 않은)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2c25c202-033b-4ea6-a340-1f6bed4f3c4b",
        "word": "Baffling",
        "meaning": "도저히 이해할 수 없는 (완전히 당황하게 하는)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "187f4a8d-0535-462a-866b-27786ce4c35b",
        "word": "Chaotic",
        "meaning": "혼란스러운 (무질서하고 복잡한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "1e6a2342-ee73-4ba3-a649-758d741ff8cd",
        "word": "Bewildering",
        "meaning": "어리둥절하게 만드는 (너무 복잡해서 당혹스러운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "513b7ec3-651e-4d95-8eec-68ca594a56f5",
        "word": "Puzzling",
        "meaning": "이해하기 힘든, 곤혹스러운 (수수께끼 같은)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "e2d61222-53cf-4471-b295-b1cdc4448e5d",
        "word": "Mystifying",
        "meaning": "신비한, 알 수 없는 (기이해서 복잡한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "adaf7fa0-695f-480a-b994-d75116db0122",
        "word": "Cryptic",
        "meaning": "수수께끼 같은, 아리송한 (의미가 숨겨진)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "988b3826-85a2-422b-b839-239956eee80a",
        "word": "Enigmatic",
        "meaning": "불가사의한 (신비롭고 이해하기 어려운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "d473628b-66d8-4be3-b8c3-0887c446c0d0",
        "word": "Obscure",
        "meaning": "모호한, 이해하기 힘든 (뜻이 불분명한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "5a4c592b-c1f5-4e86-99d5-b221d740e844",
        "word": "Recondite",
        "meaning": "심오한, 난해한 (많이 알려지지 않아 어려운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2d822e32-6c67-42f4-983f-839d5c9be717",
        "word": "Impenetrable",
        "meaning": "파악할 수 없는 (뚫고 들어갈 수 없는)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "06b19e35-d12d-4227-8918-b094841b6440",
        "word": "Sophisticated",
        "meaning": "정교한, 복잡한 (고도로 발달된)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "65bbd8bb-dadf-43e2-a0ea-8b2e347fb215",
        "word": "Multifaceted",
        "meaning": "다면적인 (여러 측면이 있는)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "98be6365-466a-45fe-867f-1efe3d4e425a",
        "word": "Multidimensional",
        "meaning": "다차원의 (여러 차원이 얽힌)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "b06e5ea6-12a5-4f2a-9276-ce7db3881577",
        "word": "Byzantine",
        "meaning": "비잔틴 양식의, 복잡한 (권모술수가 횡행하고 구조가 복잡한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "906f3852-70f8-4b90-91b6-a26f6bdeefa0",
        "word": "Perplexing",
        "meaning": "착잡한, 복잡한 (당혹스러운)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "2f432d55-9133-416c-b3c8-c71103154dd6",
        "word": "Disorienting",
        "meaning": "혼란스러운 (방향을 잃게 만드는)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "480418b0-b0ef-45d4-88e2-24ef7fda5c2d",
        "word": "Dense",
        "meaning": "난해한 (내용이 빽빽하고 어려움)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    },
    {
        "card_id": "e18a2a37-b037-4d9b-93d1-3a7398778a2d",
        "word": "Tricky",
        "meaning": "까다로운 (단순해 보이나 복잡한)",
        "deck_id": "46ea95c1-c706-478f-bc40-2839c8c98840",
        "deck_title": "COMPLEXITY_INTRICACY"
    }
]

RELEVANT_TAGS = [
    "medical",
    "schedule",
    "weather",
    "education",
    "warm",
    "fashion",
    "sport",
    "food",
    "dining",
    "travel"
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
- 위 태그들은 'COMPLEXITY_INTRICACY' 덱과 관련이 깊은 주제들입니다
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

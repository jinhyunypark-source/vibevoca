#!/usr/bin/env python3
"""
예문 생성 스크립트: SOUND_AUDITORY

이 스크립트는 'SOUND_AUDITORY' 덱의 단어들에 대해
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
    "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
    "deck_title": "SOUND_AUDITORY",
    "total_words": 21
}

WORDS = [
    {
        "card_id": "29b7aa26-8c8d-4986-90a3-1e952cb8ace8",
        "word": "Soothing",
        "meaning": "달래주는, 진정시키는",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "1f1483ec-9bcb-4bc2-a610-14d2cca67d85",
        "word": "Mellow",
        "meaning": "그윽한, 부드러운",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "acb34d17-bf6a-4b54-9bd3-aff07b085800",
        "word": "Resonant",
        "meaning": "울림이 있는",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "21c01dad-1d40-4403-97f8-222f4a880d08",
        "word": "Deafening",
        "meaning": "귀청이 터질 듯한",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "b0f061bc-4f1a-4ee1-854e-6699abac047d",
        "word": "Raucous",
        "meaning": "시끌벅적한, 거친 (라)raucus시끄러운",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "1697e969-120e-47f8-aab8-e298546d2769",
        "word": "Clamorous",
        "meaning": "떠들썩한  > claim",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "ba2ed596-4169-47c7-aff2-a6399d922b32",
        "word": "Muffled",
        "meaning": "소리를 죽인, 먹먹한",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "061ef4df-9d8b-40e5-8029-a9bb70db833d",
        "word": "Faint",
        "meaning": "희미한",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "66cc9f42-8330-4112-bb22-d7974a0f3874",
        "word": "Grating",
        "meaning": "귀에 거슬리는  격자>창살> 귀에거슬리는",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "f30bbeb9-7fca-44cb-8c72-7334525e0027",
        "word": "Hoarse",
        "meaning": "(목이) 쉰",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "632f878e-3c4b-44d3-b352-780a99a61a4d",
        "word": "Cacophonous",
        "meaning": "불협화음의  (그)cakos 나쁘다. + phone",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "c7d3398e-c4ed-4bf7-b2b8-bd1f99aa0a58",
        "word": "Shrill",
        "meaning": "새된, 꽥 하는",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "41beeb2a-3087-4461-be49-aa46ebb00fb8",
        "word": "Piercing",
        "meaning": "귀를 찢는 듯한",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "2df896f0-01cc-4e02-afe0-6a4f623ea308",
        "word": "Rasping",
        "meaning": "거슬리는, 쇳소리의",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "4db535e0-4495-4204-8068-df94f3a161d9",
        "word": "Melodious",
        "meaning": "선율이 아름다운",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "d8664a32-ea6d-49fe-87e7-2ead9baef8a4",
        "word": "Harmonious",
        "meaning": "조화로운",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "6f42b7b0-b8d8-4f81-840f-f5703e4f3f9b",
        "word": "Husky",
        "meaning": "허스키한",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "b4e67c19-625c-4cc1-bce6-17baca465f2f",
        "word": "Monotone",
        "meaning": "단조로운",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "ab975b6f-64ab-4556-8b23-9da2b7910c1e",
        "word": "Audible",
        "meaning": "들리는",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "7b619102-7a58-4c44-9c90-de68561e845e",
        "word": "Acoustic",
        "meaning": "음향의, 전자 장치를 안 쓴",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    },
    {
        "card_id": "1e242ca9-5ed3-402f-b0ed-3656298689fc",
        "word": "Thundering",
        "meaning": "우레 같은",
        "deck_id": "8001a732-513f-4649-82bb-303533ac9ef0",
        "deck_title": "SOUND_AUDITORY"
    }
]

RELEVANT_TAGS = [
    "health",
    "smartphone",
    "soccer",
    "conversation",
    "university",
    "business",
    "style",
    "nature",
    "home",
    "ai"
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
- 위 태그들은 'SOUND_AUDITORY' 덱과 관련이 깊은 주제들입니다
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

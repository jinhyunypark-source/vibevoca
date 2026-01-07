#!/usr/bin/env python3
"""
예문 생성 스크립트: AUTONOMY_LENIENCY

이 스크립트는 'AUTONOMY_LENIENCY' 덱의 단어들에 대해
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
    "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
    "deck_title": "AUTONOMY_LENIENCY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "4cbc828b-5313-403d-b496-ac46f479c0ae",
        "word": "Just",
        "meaning": "정의로운 (올바른)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "ba3f9271-8d82-42e4-8203-3e804e7a77cc",
        "word": "Lenient",
        "meaning": "관대한 (처벌이 엄하지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "ac65b454-35a3-495b-a3c3-80fd3fe92817",
        "word": "Permissive",
        "meaning": "허용적인 (자유방임적인)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "4e9daf79-6965-4e52-b3d7-ca3662c771dd",
        "word": "Egalitarian",
        "meaning": "평등주의의 (모두가 동등한)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "904028f4-292d-48fe-8b42-6acbe7205109",
        "word": "Tolerant",
        "meaning": "관용적인 (다름을 참아주는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "4895ba9d-029a-4744-afd1-7a333d44391c",
        "word": "Liberal",
        "meaning": "자유주의적인 (규제가 적은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "16161302-307b-498d-960b-419189619b1f",
        "word": "Compassionate",
        "meaning": "연민 어린 (동정심 있는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "30f49383-d125-48ca-949b-e3a030ccddd6",
        "word": "Indulgent",
        "meaning": "멋대로 하게 놔두는 (오냐오냐하는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "f8ebc6a0-1f12-4ab7-8be5-6f6d496d74e5",
        "word": "Free",
        "meaning": "자유로운 (속박이 없는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "28181484-7e22-4c6b-9c95-eae561f5ed28",
        "word": "Independent",
        "meaning": "독립적인 (남에게 의존하지 않는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "45860f89-4560-4614-a5bd-a42cd6a39afd",
        "word": "Autonomous",
        "meaning": "자치의, 자율적인 (스스로 다스리는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "ca76fc75-831b-4b7c-a271-266a83054a39",
        "word": "Sovereign",
        "meaning": "자주적인 (간섭받지 않는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "052b9930-43de-4ebb-a6be-18dc3ccf8a9c",
        "word": "Liberated",
        "meaning": "해방된 (억압에서 풀려난)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "ebd05623-f8f3-4e4e-bf84-05569bab100c",
        "word": "Unrestricted",
        "meaning": "제한이 없는 (자유로운)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "c7e7f43f-7124-49d4-b51d-9d86ccffd587",
        "word": "Unbound",
        "meaning": "얽매이지 않은 (풀려난)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "9137a0ea-67aa-436c-b452-8753c66176ef",
        "word": "Loose",
        "meaning": "느슨한 (엄격하지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "63cc7e7b-4b20-4460-b585-a597fb94dc57",
        "word": "Flexible",
        "meaning": "융통성 있는 (상황에 맞춰 바꾸는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "6a48c93c-73d0-4307-93d9-44c438390cd6",
        "word": "Open-minded",
        "meaning": "개방적인 (편견 없는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "70e65990-6120-4101-9889-7884a5498532",
        "word": "Democratic",
        "meaning": "민주적인 (모두가 평등하게 참여하는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "ab0f521f-b45e-496c-bf35-b12215f83229",
        "word": "Fair",
        "meaning": "공정한 (치우치지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "2855d822-2394-46ec-90ee-8d0c799bd439",
        "word": "Magnanimous",
        "meaning": "도량이 넓은 (적에게도 관대한)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "118f0b22-5522-43b2-9809-b743cd9d66cc",
        "word": "Forgiving",
        "meaning": "용서하는 (잘 봐주는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "61734e0e-2b1b-40c0-a726-740eec198f0e",
        "word": "Merciful",
        "meaning": "자비로운 (고통을 줄여주는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "c54b0556-e203-44ce-b9ad-9e532fbbc20c",
        "word": "Soft",
        "meaning": "무른, 온화한 (엄하지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "4833f7ba-a98e-4fdb-93f8-c31e0eab066e",
        "word": "Gentle",
        "meaning": "온화한 (거칠지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "28495d6c-f942-4d7f-829c-ceba55615686",
        "word": "Lax",
        "meaning": "해이한, 느슨한 (규율이 엉성한 - 부정적)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "58a3515f-f85b-4467-b4e1-4b2baa09b312",
        "word": "Easy-going",
        "meaning": "태평한, 느긋한 (까다롭지 않은)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "9f42ddc1-0688-489a-a7d6-966f1e253c44",
        "word": "Empowering",
        "meaning": "권한을 주는 (자신감을 북돋우는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "e07ae807-30ab-4d53-91e1-c5692d384dbd",
        "word": "Enfranchised",
        "meaning": "참정권을 얻은 (권리가 생긴)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    },
    {
        "card_id": "e1df2134-2e84-42b1-8f4b-46e4cfb66b27",
        "word": "Self-governing",
        "meaning": "자치적인 (스스로 통치하는)",
        "deck_id": "32994a99-f00b-4ee9-9870-9e855a09a2b6",
        "deck_title": "AUTONOMY_LENIENCY"
    }
]

RELEVANT_TAGS = [
    "develope",
    "business",
    "office",
    "happy",
    "communication",
    "warm",
    "entrepreneur",
    "environment",
    "outdoor",
    "sad"
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
- 위 태그들은 'AUTONOMY_LENIENCY' 덱과 관련이 깊은 주제들입니다
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

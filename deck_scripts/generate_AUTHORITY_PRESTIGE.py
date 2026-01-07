#!/usr/bin/env python3
"""
예문 생성 스크립트: AUTHORITY_PRESTIGE

이 스크립트는 'AUTHORITY_PRESTIGE' 덱의 단어들에 대해
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
    "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
    "deck_title": "AUTHORITY_PRESTIGE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d4017ef0-67a3-483e-bf74-6b70187d1042",
        "word": "Influential",
        "meaning": "영향력 있는 (타인의 생각/행동을 바꾸는 힘)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "e5518660-a497-4936-be68-a3ea8d316b83",
        "word": "Authoritative",
        "meaning": "권위 있는, 믿을 만한 (전문적이고 신뢰가 가는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "d37de74a-7569-4d75-a1f5-6088eb0350a1",
        "word": "Respected",
        "meaning": "존경받는 (사람들이 우러러보는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "baf146bf-31ac-4105-a9c5-ff6e777c490c",
        "word": "Prestigious",
        "meaning": "명망 있는 (지위가 높고 유명한)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "cbe8abfb-0429-4bfa-b04a-e2ca6f524a88",
        "word": "Esteemed",
        "meaning": "존중받는 (격식 있게 높이 평가되는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "96726822-18de-48f1-b265-e31f4046a7c5",
        "word": "Renowned",
        "meaning": "저명한 (능력으로 널리 알려진)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "1ceb9930-7060-4d03-be8b-fc009f71e576",
        "word": "Prominent",
        "meaning": "저명한, 두드러진 (중요하고 눈에 띄는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "9ea4e635-4064-497e-9c8d-f57da7f8eb60",
        "word": "Legitimate",
        "meaning": "정당한, 합법적인 (법이나 규칙에 맞는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "229ff9ab-a58f-4d87-9787-0440cdad98a5",
        "word": "Prevalent",
        "meaning": "널리 퍼진 (일반적인 영향력)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "d310727d-1663-4d39-b03f-181e4d436a57",
        "word": "Distinguished",
        "meaning": "기품 있는, 뛰어난 (성공적이고 위엄 있는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "a5af284c-1ca2-4caf-9b47-889be9b2ae5c",
        "word": "Eminent",
        "meaning": "저명한, 탁월한 (분야에서 독보적인)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "51250d87-2b18-4507-bfa1-17227660c815",
        "word": "Persuasive",
        "meaning": "설득력 있는 (말로 사람을 움직이는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "f0ff1faf-468a-4a81-ad0d-128a387c6f1d",
        "word": "Charismatic",
        "meaning": "카리스마 있는 (사람을 끌어당기는 매력)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "b867aaaf-4c2e-40ca-b680-bdeb374c531f",
        "word": "Inspiring",
        "meaning": "영감을 주는 (고무적인)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "45e75223-10bd-49d8-b470-2866ec94b000",
        "word": "Convincing",
        "meaning": "납득이 가는 (믿게 만드는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "c5395fb3-2340-4f6a-9d99-12527bd39b26",
        "word": "Impactful",
        "meaning": "영향력이 강한 (강한 충격을 주는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "139c2c93-b38f-4030-bba3-e7a561683cfb",
        "word": "Significant",
        "meaning": "중요한, 의미 있는 (무시할 수 없는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "cd19bb74-2349-4d32-8283-cc8206d5aae4",
        "word": "Pivotal",
        "meaning": "중추적인 (방향을 결정짓는 핵심적인)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "7aed1ba5-7978-4337-9960-3804763dd5e4",
        "word": "Weighty",
        "meaning": "중대한, 무게감 있는 (영향력이 큰)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "03f44def-8f3c-49a3-895f-d75cc7300a72",
        "word": "Credible",
        "meaning": "신뢰할 수 있는 (믿음이 가는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "dda4ed8c-6581-4712-b451-d98ba9b0055f",
        "word": "Official",
        "meaning": "공식적인 (공인을 받은)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "ebc9f5eb-b129-49e9-a9b3-b2ac512b8a16",
        "word": "Authorized",
        "meaning": "권한을 부여받은 (허가된)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "4c06b7fc-a231-4879-9909-97fed336b3c1",
        "word": "Licensed",
        "meaning": "면허가 있는 (자격증을 가진)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "1fea6d6d-267e-4564-8fb0-78caf69875eb",
        "word": "Empowered",
        "meaning": "권한을 가진 (힘을 부여받은)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "1060573f-bbb7-4a02-a722-a28e5f9ecd89",
        "word": "Recognized",
        "meaning": "인정받는 (공인된)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "6bc1e3a3-ecb9-4bb6-a127-dd4cb741ad71",
        "word": "Leading",
        "meaning": "선도하는 (가장 앞선)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "c95982c7-1116-42f1-a909-b3ebfd327eb8",
        "word": "Viral",
        "meaning": "입소문이 난 (빠르게 퍼지는 영향력)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "10985947-419c-4f68-a24f-fd4a07cecea7",
        "word": "Magnetic",
        "meaning": "자석 같은 (사람을 끌어당기는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "13eac54b-77ed-4df5-97c1-7ccf45ac4e4f",
        "word": "Compelling",
        "meaning": "강력한, 설득력 있는 (거부할 수 없는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    },
    {
        "card_id": "2dbe4189-962c-4344-b922-641f7be227fc",
        "word": "Effectual",
        "meaning": "효과적인, 효력이 있는 (실질적 힘을 발휘하는)",
        "deck_id": "270deafe-06b3-4560-b863-ac93a3676f48",
        "deck_title": "AUTHORITY_PRESTIGE"
    }
]

RELEVANT_TAGS = [
    "environment",
    "feeling",
    "interview",
    "digital",
    "movie",
    "smartphone",
    "place",
    "art",
    "dining",
    "learning"
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
- 위 태그들은 'AUTHORITY_PRESTIGE' 덱과 관련이 깊은 주제들입니다
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

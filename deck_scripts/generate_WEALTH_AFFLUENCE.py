#!/usr/bin/env python3
"""
예문 생성 스크립트: WEALTH_AFFLUENCE

이 스크립트는 'WEALTH_AFFLUENCE' 덱의 단어들에 대해
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
    "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
    "deck_title": "WEALTH_AFFLUENCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "013eb8b7-7ecf-4536-98ff-8c90fe63b8e8",
        "word": "Rich",
        "meaning": "부유한 (가장 일반적인 표현)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "0f44e162-e4f6-429d-b1a3-b4bb6b4dd74f",
        "word": "Wealthy",
        "meaning": "재산이 많은 (Rich보다 격식 있고 장기적 부)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "b69ec1b3-12bf-4632-b48d-06ef60201a74",
        "word": "Affluent",
        "meaning": "부유한, 풍족한 (생활 수준이 높은)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "1dc55086-3657-4bb0-98ed-db19d3305c30",
        "word": "Prosperous",
        "meaning": "번영하는 (사업이 잘되어 돈이 많은)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "77e8c706-2431-4d43-9665-31979517a9e3",
        "word": "Opulent",
        "meaning": "엄청나게 부유한 (호화롭고 사치스러운)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "bdd245d5-c37e-4eae-adb6-f54b173668a5",
        "word": "Minted",
        "meaning": "갓 찍어낸 듯 돈이 많은 (속어: 갑부인)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "12da92b4-6494-4311-a4ea-afa6b4330468",
        "word": "Filthy rich",
        "meaning": "떼부자 (돈이 너무 많아 불쾌할 정도인)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "0fb884df-7772-4049-a41b-951b2867348e",
        "word": "Well-off",
        "meaning": "유복한 (부족함 없이 사는)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "d65f80aa-b234-4013-89be-4668c6562c5a",
        "word": "Well-to-do",
        "meaning": "잘사는 (사회적 지위가 있고 넉넉한)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "7fde16a8-10e7-4aa1-8553-570b3c2489cf",
        "word": "Means",
        "meaning": "재력, 수단 (돈)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "1d34b47a-5d05-4570-bfda-e45a71818c03",
        "word": "Solvent",
        "meaning": "지불 능력이 있는 (빚을 갚을 돈이 있는)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "8e5db6ec-cc33-4a97-9edc-7800addc8af2",
        "word": "Loaded",
        "meaning": "돈이 썩어나는 (속어: 돈이 아주 많은)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "54fa99d9-5e23-4852-bebf-600c0f65bfeb",
        "word": "Flush",
        "meaning": "돈이 두둑한 (일시적으로 현금이 많은)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "baf63b51-bf25-42b8-a069-1a2892c91f04",
        "word": "Rolling in it",
        "meaning": "돈방석에 앉은 (돈이 넘쳐나는)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "e4495b11-e5c3-4916-99e9-98b81bc73dc4",
        "word": "Privileged",
        "meaning": "특권층의 (돈과 권력을 가진)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "9cba7529-306b-4489-882c-9d587b433dff",
        "word": "Comfortable",
        "meaning": "넉넉한 (걱정 없을 만큼 충분한)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "5ce8f6f8-8929-4ddf-8129-41819fa40bd6",
        "word": "Propertied",
        "meaning": "재산이 있는 (부동산 등을 소유한)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "622f3ce3-5751-42f0-927c-1badf3b87770",
        "word": "High-net-worth",
        "meaning": "순자산이 높은 (금융 용어: 고액 자산가)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "5a23555f-69d2-47e6-836b-54d03e8078e4",
        "word": "Upscale",
        "meaning": "부유층을 위한, 고급의",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "93cb6e37-f48f-439c-b4e1-f49b4bca5993",
        "word": "Elite",
        "meaning": "엘리트의 (부와 권력을 가진 소수)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "bb11bc64-519a-41c7-8e0b-86166c69d9c7",
        "word": "Moneyed",
        "meaning": "돈 많은 (재산가인)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "f52ed23d-d9ed-49fd-903e-741aa348466b",
        "word": "Nouveau riche",
        "meaning": "졸부 (벼락부자 - 약간 비하적)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "c10cc913-1cf9-4768-8351-42dbe4be6bd3",
        "word": "Tycoon",
        "meaning": "거물 (실업계의 대부)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "5b9be4ef-52d9-498c-aabe-64bfce55e3f8",
        "word": "Magnate",
        "meaning": "왕, 거물 (특정 산업의 유력자)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "f4b430e3-3253-4567-aadc-39bc0c763078",
        "word": "Millionaire",
        "meaning": "백만장자 (부자)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "d197e683-a83c-4568-9110-6b051436dc34",
        "word": "Billionaire",
        "meaning": "억만장자 (엄청난 부자)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "ab449fe0-d86c-4c12-8efc-669ff85c0db5",
        "word": "Fortune",
        "meaning": "큰 재산, 거금",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "89ac4edd-569a-4a2e-abfa-3ea39c5c7bcd",
        "word": "Asset",
        "meaning": "자산 (돈이 되는 것)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "09d51f56-8aa9-43ab-b91f-1dda0964d2e5",
        "word": "Capital",
        "meaning": "자본금 (사업 밑천)",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    },
    {
        "card_id": "ee7b5233-0dd3-4fa7-a655-410d9015c79c",
        "word": "Inheritance",
        "meaning": "유산, 상속 재산",
        "deck_id": "4c9286ae-c556-4aa5-93e7-cd2db8a82d9e",
        "deck_title": "WEALTH_AFFLUENCE"
    }
]

RELEVANT_TAGS = [
    "emotion",
    "daily_life",
    "travel",
    "digital",
    "wellness",
    "food",
    "time",
    "cooking",
    "sport",
    "university"
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
- 위 태그들은 'WEALTH_AFFLUENCE' 덱과 관련이 깊은 주제들입니다
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

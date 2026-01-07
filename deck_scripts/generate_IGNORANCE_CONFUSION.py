#!/usr/bin/env python3
"""
예문 생성 스크립트: IGNORANCE_CONFUSION

이 스크립트는 'IGNORANCE_CONFUSION' 덱의 단어들에 대해
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
    "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
    "deck_title": "IGNORANCE_CONFUSION",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "9fb063d3-df46-4b57-a4b2-b3dd9cc3f543",
        "word": "Ignorant",
        "meaning": "무지한 (배우지 못했거나 정보가 없는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "2a3ff85c-54a5-4162-a329-639fb8a60091",
        "word": "Uneducated",
        "meaning": "교육받지 못한 (학교 교육 부재)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "a22db2a1-dedc-4e0b-ab13-cb99fe6b83a7",
        "word": "Illiterate",
        "meaning": "문맹의 (글을 읽고 쓸 줄 모르는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "56c1b657-24e8-4a22-82c7-0cbbc162cd3b",
        "word": "Uninformed",
        "meaning": "정보통이 아닌 (지식/정보가 부족한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "8dddb6ca-7e50-4905-9503-1c7a5a991a57",
        "word": "Unaware",
        "meaning": "알지 못하는 (자각하지 못한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "6e62f520-36af-47c7-ac62-ad4c1cac4716",
        "word": "Oblivious",
        "meaning": "의식하지 못하는 (주변 상황을 까먹고 있는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "d5061e38-20e0-4aff-b8b1-b893cbcaced1",
        "word": "Naive",
        "meaning": "순진한 (경험이 없어 세상 물정 모르는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "3a4d98c5-0d6e-4939-9fd0-62e6d760f8aa",
        "word": "Gullible",
        "meaning": "잘 속는 (남의 말을 너무 쉽게 믿는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "40f72f50-1289-4f35-a123-6b2c87959aa2",
        "word": "Credulous",
        "meaning": "쉽게 믿는 (의심할 줄 모르는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "bfb49e59-bcd3-4530-8b9d-110255f2549d",
        "word": "Innocent",
        "meaning": "무고한, 천진난만한 (악의가 없는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "1ddde93c-c99e-4708-b89e-e76883ed4ebc",
        "word": "Green",
        "meaning": "풋내기의 (경험이 부족한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "d4070a1f-ff02-4c9a-adb1-5258e6d1130f",
        "word": "Inexperienced",
        "meaning": "경험 없는 (미숙한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "0ec5eb3b-8655-4e62-bf19-d3f0e72848dc",
        "word": "Amateurish",
        "meaning": "아마추어 같은 (전문성이 떨어지는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "fd59b265-ac7c-4ed5-ae79-af9b2c58c454",
        "word": "Clumsy",
        "meaning": "서투른 (동작이 어설픈)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "0eaf9526-f970-4db3-a513-ed957b9c4b2e",
        "word": "Inept",
        "meaning": "솜씨 없는, 서툰 (적성이 없는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "9b8209c7-0606-4aac-8f72-4812d6946961",
        "word": "Incompetent",
        "meaning": "무능한 (일을 처리할 능력이 없는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "5f27df26-abdc-44ab-8080-822a80489c74",
        "word": "Confused",
        "meaning": "혼란스러운 (이해하지 못해 헷갈리는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "b96bdc71-2431-4ce2-a5e5-7e88d6e8ef07",
        "word": "Puzzled",
        "meaning": "어리둥절한 (이해가 안 가서 궁금한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "d876ead8-fbf4-4400-8167-8e9784fd8f5b",
        "word": "Perplexed",
        "meaning": "당혹스러운 (복잡해서 난처한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "04a114bc-efb9-48f9-9b38-ccc25d732985",
        "word": "Baffled",
        "meaning": "도저히 이해할 수 없는 (완전히 당황한)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "843d62aa-f2e8-4a55-8164-87b3593d2adf",
        "word": "Bewildered",
        "meaning": "어리둥절해하는 (너무 많거나 놀라서 정신없는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "cde9afd5-ba13-4545-84e7-f0dee0451bbf",
        "word": "Disoriented",
        "meaning": "방향 감각을 잃은 (어디가 어딘지 모르는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "0239f36a-cc56-437c-9890-dbe2b4101858",
        "word": "Dazed",
        "meaning": "멍한 (충격 등으로 정신이 나간)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "628a966b-c638-4d69-a7ea-09041d06ce98",
        "word": "Absent-minded",
        "meaning": "건망증이 있는, 멍한 (정신을 다른 데 파는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "b8a51c5d-3175-4192-9bef-15f9cea72b57",
        "word": "Forgetful",
        "meaning": "잘 잊어버리는 (기억력이 나쁜)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "539e2353-ff59-48aa-97d9-a3a184ff183b",
        "word": "Scatterbrained",
        "meaning": "정신산란한 (집중 못 하고 덜렁대는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "58b1d28d-e542-4846-b2f7-e8d1b4fd8f0b",
        "word": "Irrational",
        "meaning": "비이성적인 (논리가 통하지 않는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "d1d8a506-7e1a-4188-a7ac-10278aeadfd7",
        "word": "Illogical",
        "meaning": "비논리적인 (앞뒤가 안 맞는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "0e0ae893-5d07-41e2-8d96-643de364f6d9",
        "word": "Unreasonable",
        "meaning": "불합리한, 무리한 (이치에 닿지 않는)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    },
    {
        "card_id": "4a770e94-1d0d-41e6-8bec-9f7e7e183bf7",
        "word": "Biased",
        "meaning": "편향된 (공정하지 못하고 한쪽으로 치우친 판단)",
        "deck_id": "09d28c03-555d-47ea-b2ea-f6836ba680c0",
        "deck_title": "IGNORANCE_CONFUSION"
    }
]

RELEVANT_TAGS = [
    "movie",
    "mood",
    "shopping",
    "school",
    "travel",
    "study",
    "code",
    "dining",
    "sport",
    "happy"
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
- 위 태그들은 'IGNORANCE_CONFUSION' 덱과 관련이 깊은 주제들입니다
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

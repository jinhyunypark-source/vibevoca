#!/usr/bin/env python3
"""
예문 생성 스크립트: START_END_RECOVERY

이 스크립트는 'START_END_RECOVERY' 덱의 단어들에 대해
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
    "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
    "deck_title": "START_END_RECOVERY",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "d0dc97d0-deae-4f7d-ad20-0885c54a9ec2",
        "word": "Initiate",
        "meaning": "개시하다 (공식적으로 시작하다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "5b759626-15ee-49db-b14a-941a88057021",
        "word": "Commence",
        "meaning": "시작되다 (격식 있는 시작)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "3bed8469-62aa-4a6a-b45d-1c76348cec9d",
        "word": "Launch",
        "meaning": "출시하다, 발사하다 (세상에 내놓다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "420e6e9e-d6cd-4039-8851-9873855915ef",
        "word": "Trigger",
        "meaning": "촉발하다 (방아쇠를 당기듯 일으키다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "f7536d07-4c6f-445f-8e80-5c93097188ef",
        "word": "Spark",
        "meaning": "불러일으키다 (불꽃을 튀기다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "c181979a-d3e0-494f-8162-c78571c3ca8a",
        "word": "Originate",
        "meaning": "비롯되다 (기원을 두다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "81774e2d-a59d-45b5-b9b7-d97589e31cc7",
        "word": "Generate",
        "meaning": "발생시키다 (만들어내다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "37b07c86-c107-4011-93b8-5ed5e0a1e7b6",
        "word": "Establish",
        "meaning": "설립하다, 확립하다 (기반을 다지다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "e4f7b4d0-e14e-451f-8d06-382f647b6aed",
        "word": "Terminate",
        "meaning": "종료하다 (끝을 맺다/해고하다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "93517a72-ef35-4d14-af2d-38025a2402af",
        "word": "Cease",
        "meaning": "중단하다 (그치다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "8ae04870-7a20-4474-bfda-c515e4bcf863",
        "word": "Conclude",
        "meaning": "결론 짓다, 마치다 (마무리하다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "c7c43ed2-ca23-4ed3-9cfd-d47b2b5e9c3d",
        "word": "Abolish",
        "meaning": "폐지하다 (법이나 제도를 없애다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "93e50b7f-cba2-45c1-8a1a-7012a5cc8a5a",
        "word": "Eradicate",
        "meaning": "근절하다 (뿌리째 뽑다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "678f5651-60ff-4245-a482-f07bc0b773fe",
        "word": "Eliminate",
        "meaning": "제거하다 (없애다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "1af79931-10d3-4c50-8039-be4f16822185",
        "word": "Extinguish",
        "meaning": "끄다, 소멸시키다 (불을 끄듯 없애다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "f642a406-deb1-4f34-aa54-ba60327fedfd",
        "word": "Vanish",
        "meaning": "사라지다 (갑자기 없어지다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "13f48ab0-caa6-46e2-ac35-31306f79ab8a",
        "word": "Recover",
        "meaning": "회복하다 (원래 상태를 되찾다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "dd90f7bb-4fd2-4705-af11-af9449016a6e",
        "word": "Restore",
        "meaning": "복구하다 (이전의 좋은 상태로 돌리다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "05628f51-a2b6-49ae-b2da-e5e272498aa1",
        "word": "Revive",
        "meaning": "되살리다 (생기를 불어넣다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "57a7fb72-3f1c-4e80-beb7-057c7985475f",
        "word": "Rejuvenate",
        "meaning": "다시 젊게 하다 (활력을 되찾다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "c26977f8-c0fa-4ce8-8773-d65dc1ca033d",
        "word": "Resurrect",
        "meaning": "부활시키다 (죽은 것을 살려내다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "415d4183-488f-48fd-8626-233ad2801890",
        "word": "Rehabilitate",
        "meaning": "재활하다, 명예를 회복하다",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "957bdce5-f211-4009-918c-c4257daf17c5",
        "word": "Retrieve",
        "meaning": "되찾다, 회수하다 (잃어버린 것을 가져오다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "c9f6a6b9-8f48-442f-b051-85fa6ae987da",
        "word": "Redeem",
        "meaning": "만회하다, 상환하다 (잘못을 덮거나 갚다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "0c785a9d-1e66-40a5-a8f2-e391aea40456",
        "word": "Salvage",
        "meaning": "구조하다 (난파선/재난에서 건지다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "de646463-90de-4613-ad6a-1d5bf6bf844b",
        "word": "Bounce back",
        "meaning": "다시 회복하다 (공처럼 튀어 오르다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "13ea0ad6-0b6e-4828-9b44-60a2edf7cc5d",
        "word": "Rally",
        "meaning": "(세력을) 규합하다, 반등하다",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "0d5a691f-5513-40f5-9205-f47ecdddb964",
        "word": "Recuperate",
        "meaning": "회복하다 (병이나 피로에서 요양하다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "dafebf7e-b7c6-4022-aa21-fa7ab0ecbc84",
        "word": "Heal",
        "meaning": "치유하다 (상처가 낫다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    },
    {
        "card_id": "c1a61fae-5239-4b8a-93d7-6ef217b4f106",
        "word": "Regenerate",
        "meaning": "재생하다 (조직이나 사회를 다시 살리다)",
        "deck_id": "9df3e72d-4661-494a-8a7a-eac78cb323c8",
        "deck_title": "START_END_RECOVERY"
    }
]

RELEVANT_TAGS = [
    "school",
    "music",
    "friendship",
    "daily_life",
    "internet",
    "meeting",
    "work",
    "smartphone",
    "learning",
    "outdoor"
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
- 위 태그들은 'START_END_RECOVERY' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: SIGNIFICANCE_DEPTH

이 스크립트는 'SIGNIFICANCE_DEPTH' 덱의 단어들에 대해
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
    "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
    "deck_title": "SIGNIFICANCE_DEPTH",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "774ccb9f-85d1-4ba6-8125-4d47d496b317",
        "word": "Incidental",
        "meaning": "부수적인 (중요한 것에 딸려오는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "3d41d582-0176-43d1-a86c-2cf907ea3ef5",
        "word": "Critical",
        "meaning": "대단히 중요한, 위태로운 (생사가 걸린)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "52ec4f87-8061-46a2-89bc-9a69a691c1ec",
        "word": "Trivial",
        "meaning": "사소한, 하찮은 (신경 쓸 필요 없는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "7a3aacdc-d22f-4c10-9d98-48e2a7c41291",
        "word": "Minor",
        "meaning": "작은, 별로 중요치 않은 (심각하지 않은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "92c4014b-8c9c-43cb-a0f6-772437ff6099",
        "word": "Petty",
        "meaning": "안 중요한, 옹졸한 (작고 시시한)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "fc9182dc-2d93-4e26-92a0-751fd2cd8dd8",
        "word": "Slight",
        "meaning": "약간의 (정도가 미미한)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "81ee2eb0-db57-4110-85ff-81d11856c8d7",
        "word": "Negligible",
        "meaning": "무시해도 될 정도의 (양이 아주 적은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "5ac5fe25-9ce6-424d-b7e3-6f368b7bfe72",
        "word": "Insignificant",
        "meaning": "대수롭지 않은 (의미가 없는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "dc785122-2776-465b-8b2d-3a98b849fd89",
        "word": "Marginal",
        "meaning": "미미한, 주변부의 (중요하지 않은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "17fd1c15-7fff-42d5-8523-869316c2d93d",
        "word": "Superficial",
        "meaning": "표면적인 (깊이가 없는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "3dd7e7d3-b780-4a98-b523-09e2e317cad4",
        "word": "Frivolous",
        "meaning": "경박한, 하찮은 (진지하지 않은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "5670aefc-d549-4f00-b2e3-b219f1f4991f",
        "word": "Trifling",
        "meaning": "하찮은 (가치가 거의 없는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "3d33bd0b-4d43-4856-8ccd-faa513250b9d",
        "word": "Crucial",
        "meaning": "결정적인 (성패를 좌우하는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "1f6c9a20-b295-4f47-9609-092fa7ef9ce8",
        "word": "Vital",
        "meaning": "필수적인, 생명의 (없으면 안 되는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "6899edaf-1883-4ea9-be4e-effc2c6b6cfc",
        "word": "Pivotal",
        "meaning": "중추적인 (회전축처럼 방향을 바꾸는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "6f7b003c-52dd-4260-b3c1-748112bd69b4",
        "word": "Essential",
        "meaning": "본질적인, 필수적인 (가장 기본이 되는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "e1b0f669-ff66-44a1-b1ef-93070286c773",
        "word": "Major",
        "meaning": "주요한, 큰 (규모나 중요도가 큰)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "333b7e8c-5041-4b2b-9b87-38285eee4048",
        "word": "Serious",
        "meaning": "심각한, 진지한 (가볍지 않은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "616a5a05-d96c-40ad-b3ea-4ea95a1e213c",
        "word": "Grave",
        "meaning": "중대한, 엄숙한 (매우 심각하고 무거운)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "dccee112-9a35-4150-9703-5e631543fcc7",
        "word": "Acute",
        "meaning": "극심한, 급성의 (문제의 정도가 날카롭고 심한)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "a303b4e9-16c7-47fb-b3c7-cb0497ac66d8",
        "word": "Severe",
        "meaning": "가혹한, 심한 (엄격하고 고통스러운)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "728d2825-96b7-4cc6-985e-1a3a68ab8274",
        "word": "Profound",
        "meaning": "심오한, 엄청난 (깊이가 있고 영향이 큰)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "13892e3f-6569-4130-b2da-493f27c65f25",
        "word": "Deep",
        "meaning": "깊은 (표면적이지 않은)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "cc2d14ac-53f9-4054-a496-96fc1a2d313c",
        "word": "Weighty",
        "meaning": "중대한, 무거운 (영향력이 큰)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "7bddc203-9af9-4a7c-b451-e7a7f515546f",
        "word": "Monumental",
        "meaning": "기념비적인, 엄청난 (역사에 남을 만큼 큰)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "01210d44-dc77-4184-a5f9-1c109110cb77",
        "word": "Consequential",
        "meaning": "중대한 결과가 따르는 (중요한)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "7e29136c-f559-466c-b0c7-c5d6ad619774",
        "word": "Substantial",
        "meaning": "상당한, 실질적인 (양이나 중요성이 꽤 되는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "69dff655-5634-45d9-b46b-09078819150f",
        "word": "Pressing",
        "meaning": "긴박한 (당장 처리해야 하는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "4c5af2c3-6932-419c-8322-258f61b18892",
        "word": "Urgent",
        "meaning": "시급한 (지체할 수 없는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    },
    {
        "card_id": "704cc007-1330-4af5-826a-c5d528a74bd2",
        "word": "Paramount",
        "meaning": "최고로 중요한 (다른 무엇보다 우선하는)",
        "deck_id": "61e13492-8645-4361-a1f1-3dc43a1b0365",
        "deck_title": "SIGNIFICANCE_DEPTH"
    }
]

RELEVANT_TAGS = [
    "home",
    "soccer",
    "sad",
    "schedule",
    "feeling",
    "travel",
    "medical",
    "smartphone",
    "technology",
    "cooking"
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
- 위 태그들은 'SIGNIFICANCE_DEPTH' 덱과 관련이 깊은 주제들입니다
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

#!/usr/bin/env python3
"""
예문 생성 스크립트: FINANCIAL_STATUS

이 스크립트는 'FINANCIAL_STATUS' 덱의 단어들에 대해
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
    "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
    "deck_title": "FINANCIAL_STATUS",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "a212ea46-88c5-4d38-aaba-0142be31c701",
        "word": "Lucrative",
        "meaning": "수익성이 좋은 (돈벌이가 잘되는)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "4a010df7-40fa-48ab-b914-8effec3c78ea",
        "word": "Profitable",
        "meaning": "이익이 되는 (수익을 내는)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "5fd0b328-4bca-41bb-9a6d-0da9b51b54aa",
        "word": "Gainful",
        "meaning": "유급의, 돈이 되는 (일자리가 있는)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "be5fb73f-0efe-4896-b1db-17e1fe75505f",
        "word": "Remunerative",
        "meaning": "보수가 좋은 (돈을 많이 주는 - 격식)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "e8cf0446-e3cc-4f01-851a-1a48db71626a",
        "word": "Rewarding",
        "meaning": "보람 있는, 수익이 나는 (만족감+돈)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "a6576284-d193-4e58-bc04-0099b9fbca8e",
        "word": "Worthwhile",
        "meaning": "가치 있는 (시간/돈 쓸 만한)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "4627adce-452a-4940-8029-08759683f083",
        "word": "Salary",
        "meaning": "봉급, 월급 (전문직/사무직의 고정급)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "35ef856f-4646-4a63-ac27-37aac1d19e84",
        "word": "Wage",
        "meaning": "임금 (노동직/시간제 급여)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "955828a5-82c9-400c-88cc-9ab53908ac66",
        "word": "Income",
        "meaning": "소득, 수입 (들어오는 모든 돈)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "81c79d47-d8b2-4b35-8124-e4fb305d7088",
        "word": "Earnings",
        "meaning": "벌이, 수익 (일해서 번 돈/기업 수익)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "b44f35b6-643a-45b6-8822-745cace3d9f9",
        "word": "Revenue",
        "meaning": "매출, 세입 (비용 빼기 전 총수입)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "720b4d29-8f5a-4273-8f85-759de0cbd5a8",
        "word": "Profit",
        "meaning": "이익, 순이익 (매출에서 비용 뺀 돈)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "ddccbf4b-ac1c-4f39-a699-37332c4b664b",
        "word": "Margin",
        "meaning": "마진, 이윤의 폭 (원가와 판매가의 차이)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "d10cffd8-a0b9-41ff-8381-6ae7fcefe8f3",
        "word": "Dividend",
        "meaning": "배당금 (주주에게 나눠주는 이익)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "0c139d7d-4cc6-466e-92c1-ac1a4a34b79d",
        "word": "Interest",
        "meaning": "이자 (돈을 빌려준 대가)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "ca0155dc-12fc-46d2-a269-91241460d361",
        "word": "Yield",
        "meaning": "수익률, 산출하다 (투자 대비 성과)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "52299d2c-5ce2-4dc3-9b9c-e442ef4f9968",
        "word": "Return",
        "meaning": "수익 (투자에서 돌아오는 돈)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "0776cb79-1bbf-4951-b742-b1c884f89054",
        "word": "Capital",
        "meaning": "자본 (사업 자금)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "8ab23de7-2bcb-4ab0-85f7-8395ef3f22c5",
        "word": "Funding",
        "meaning": "자금 조달, 재정 지원",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "507005ce-e1b7-4262-87df-e482632504e8",
        "word": "Investment",
        "meaning": "투자 (이익을 위해 돈을 씀)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "18313049-e637-42f0-a357-113c0aaac492",
        "word": "Loan",
        "meaning": "대출 (빌린 돈)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "a42ccbe0-9ffe-41fc-abbc-e9adb5e28d52",
        "word": "Debt",
        "meaning": "빚, 부채",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "7c39a357-b021-4d10-b025-168822c859c6",
        "word": "Credit",
        "meaning": "신용, 외상",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "afa5e9cb-1f30-47a8-a35e-824ade140a13",
        "word": "Mortgage",
        "meaning": "주택 담보 대출",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "f198d186-9767-4e80-b580-8bd07f2118bc",
        "word": "Tax",
        "meaning": "세금",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "f2a6a2b8-c556-4b84-8494-d638962ab637",
        "word": "Duty",
        "meaning": "관세, 의무 (수입품에 붙는 세금)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "1a97397a-f2ad-445b-a631-a18a9ab4329e",
        "word": "Tariff",
        "meaning": "관세 (국가 간 무역 세금)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "df1db263-1ff6-4b5e-8ff1-1b21b1f5d610",
        "word": "Fiscal",
        "meaning": "재정의, 회계의 (국가 살림/회계 연도)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "dced82fd-72f7-4860-bee3-ae12b6c7ca12",
        "word": "Monetary",
        "meaning": "통화의, 화폐의 (돈의 유통과 관련된)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    },
    {
        "card_id": "64259e2e-af13-4e62-a8dc-6cd82fd9d88e",
        "word": "Financial",
        "meaning": "재정적인, 금융의 (돈 관리 전반)",
        "deck_id": "06df4fff-7a4a-4097-9055-5098b523def1",
        "deck_title": "FINANCIAL_STATUS"
    }
]

RELEVANT_TAGS = [
    "relationship",
    "technology",
    "interview",
    "health",
    "communication",
    "marketing",
    "meeting",
    "warm",
    "art",
    "study"
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
- 위 태그들은 'FINANCIAL_STATUS' 덱과 관련이 깊은 주제들입니다
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

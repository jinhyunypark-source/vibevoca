#!/usr/bin/env python3
"""
예문 생성 스크립트: TOUCH_TEXTURE

이 스크립트는 'TOUCH_TEXTURE' 덱의 단어들에 대해
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
    "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
    "deck_title": "TOUCH_TEXTURE",
    "total_words": 23
}

WORDS = [
    {
        "card_id": "65e58107-4e73-45a9-b910-f68e9a06dce9",
        "word": "Silky",
        "meaning": "비단 같은",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "c33bb78d-8d17-49c0-b115-153f84dab07c",
        "word": "Velvety",
        "meaning": "벨벳 같은",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "2dfbf5f8-9432-4741-8e2d-eaac1d6e59e3",
        "word": "Sleek",
        "meaning": "매끄러운",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "2862b179-7ac3-499d-8ffe-2189dcbcc1e8",
        "word": "Supple",
        "meaning": "유연한, 탄력 있는.  sub+pli(구부리다)",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "5f53a896-0bab-4fbe-82fb-ee4bdeb775e1",
        "word": "[supple](https://www.google.com/search?q=supple_sca_esv=5ea70eeef6a2a5b7_rlz=1C5CHFA_enKR1185KR1185_sxsrf=AE3TifMncPwbcYuEJE04QBefCVP_avfAWw%3A1765085439607_ei=_xA1aeXjJO6y0-kPoIOu6QU_ved=2ahUKEwjn6qHe36qRAxVv1jQHHSyPOTsQgK4QegQIAxAG_uact=5_oq=Supple+%EC%96%B4%EC%9B%90_gs_lp=Egxnd3Mtd2l6LXNlcnAiDVN1cHBsZSDslrTsm5AyBhAAGAcYHjIGEAAYDRgeMgQQABgeMggQABiABBiiBDIIEAAYgAQYogQyBRAAGO8FSOcJUNMCWKEIcAJ4AJABAJgBggGgAfABqgEDMC4yuAEDyAEA-AEC-AEBmAIEoAKAAsICCBAAGLADGO8FwgILEAAYgAQYsAMYogSYAwCIBgGQBgWSBwMyLjKgB7YHsgcDMC4yuAf4AcIHBTAuMy4xyAcKgAgA_sclient=gws-wiz-serp_mstk=AUtExfCu7yfUGZUVWmeRCrvQ5TxBuPrdlXhwQtWLbzOUgQzhAxmmTEJd_jrJmTBCb_Ucq3_o4oA28lcF_7xzQXQJTlAoc_NjsWjhMDyald09V8VoSqUtJ8SSLwjTaGuR1RIBOekL15Fi7VU1WvxP1APEObqBkaSaDJ2F76U6ngEnQA1sexMh5jHhhY3BVojM5UGqw79vBoJnpwOzlEH8HrwK0QsDAYAfqDicrGAKDC_vSd9YbKkTsWS2uApjx1wW90M8Oj9XpSLGKvL0LPp21YLnmBNH_csui=3)ment",
        "meaning": "보충하다.",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "bdaee441-3669-4778-9716-5a3000cf12ff",
        "word": "Fluffy",
        "meaning": "푹신한, 솜털 같은",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "7069dfd5-3df3-4aa0-82c8-37f3833416da",
        "word": "Coarse",
        "meaning": "거친 (입자가 굵은)",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "53e99fba-fdfd-4d41-baa9-e70e307d9bbf",
        "word": "Rough",
        "meaning": "거친, 울퉁불퉁한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "702242ea-8b5d-4ea8-ac79-b930eede58f8",
        "word": "Prickly",
        "meaning": "가시 같은, 따끔거리는  (고)prik 찌르다",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "effaed06-79cb-4572-bf7a-d648818886e5",
        "word": "Bristly",
        "meaning": "까슬까슬한 (털)",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "c5f2c2f3-992c-4788-8f2d-0e62e3d73d2d",
        "word": "Gritty",
        "meaning": "모래 같은, 꺼끌꺼끌한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "64c08e79-b2f8-4808-8a97-c6812b422723",
        "word": "grit",
        "meaning": "모래",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "255bd083-5283-4fc7-bd04-a0874ff38e3d",
        "word": "Abrasive",
        "meaning": "연마하는, 거친",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "622bfb0b-cbaa-4776-8d17-5e2ae76ba4fb",
        "word": "Clammy",
        "meaning": "축축한 (기분 나쁜)  clam(끈적)/ clay(점토)",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "4b1a2b69-b55f-4f78-b7b7-7a39e7b149f5",
        "word": "Viscous",
        "meaning": "점성이 있는, 끈적한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "77644785-2319-40c8-addc-fbbe12f1f4fd",
        "word": "Damp",
        "meaning": "눅눅한, 축축한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "2e3d4e03-6da2-490c-bd77-0fcd231e59ad",
        "word": "Slimy",
        "meaning": "미끈거리는, 끈적한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "91215351-8144-4039-a3d7-ff163ea071f7",
        "word": "Sticky",
        "meaning": "끈적끈적한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "3356a1b7-97e5-4ce2-9671-ed9afb38f47a",
        "word": "Tepid",
        "meaning": "미지근한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "bbe62faa-f28d-4954-aeda-31c599e1971d",
        "word": "Frigid",
        "meaning": "몹시 차가운",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "694427be-8d6b-4646-8d8c-26b1f0e38a70",
        "word": "Brittle",
        "meaning": "부서지기 쉬운",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "531ae140-2224-467b-89dc-aa6a1e4ec714",
        "word": "Fragile",
        "meaning": "깨지기 쉬운, 연약한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    },
    {
        "card_id": "2eb87c77-0cc1-4a73-971b-55861c063fc1",
        "word": "Jagged",
        "meaning": "삐죽삐죽한",
        "deck_id": "197423b4-974e-400c-b010-00aabc920e4c",
        "deck_title": "TOUCH_TEXTURE"
    }
]

RELEVANT_TAGS = [
    "entrepreneur",
    "meeting",
    "activity",
    "smartphone",
    "daily_life",
    "technology",
    "relationship",
    "university",
    "ai",
    "movie"
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
- 위 태그들은 'TOUCH_TEXTURE' 덱과 관련이 깊은 주제들입니다
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

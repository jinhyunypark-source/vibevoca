#!/usr/bin/env python3
"""
예문 생성 스크립트: INTELLIGENCE_BRILLIANCE

이 스크립트는 'INTELLIGENCE_BRILLIANCE' 덱의 단어들에 대해
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
    "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
    "deck_title": "INTELLIGENCE_BRILLIANCE",
    "total_words": 30
}

WORDS = [
    {
        "card_id": "b2ac7876-8cdf-4a1a-8ea4-d352a39ccd62",
        "word": "Knowledgeable",
        "meaning": "아는 것이 많은 (박식한)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "60ec890a-27cd-4362-96de-7887eaafa27d",
        "word": "Intelligent",
        "meaning": "지능적인 (가장 일반적이고 격식 있는 표현)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "f33874e8-9831-4ed2-8ed2-762327e05592",
        "word": "Smart",
        "meaning": "똑똑한 (똑바르고 깔끔하게 머리가 좋은)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "22f32728-5603-4151-a8f9-6af26c88750f",
        "word": "Bright",
        "meaning": "총명한, 영리한 (잠재력이 있고 눈이 반짝이는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "c2e6edfc-1826-43b5-ab1f-353307099f62",
        "word": "Brilliant",
        "meaning": "명석한, 훌륭한 (지능이 빛날 정도로 뛰어난)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "98d97916-4bbb-45b7-aada-de8acc3380f3",
        "word": "Genius",
        "meaning": "천재적인 (범접할 수 없는 재능)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "52579a16-46b4-45f3-8526-24c5c5d855ae",
        "word": "Resourceful",
        "meaning": "기지 넘치는, 수완 좋은 (자원을 잘 활용하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "f5e8cde7-c765-4c21-89c1-5b463da50339",
        "word": "Erudite",
        "meaning": "박식한, 학식 있는ex(바깥)[rudis(미숙한)](rudis(%EB%AF%B8%EC%88%99%ED%95%9C)%202c23415d9fe7801ba725ceb7c3eb0e84.md)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "b22409ee-936a-4f76-afed-8876daf75ad3",
        "word": "rudimentary",
        "meaning": "기초적인",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "6c075a7b-5988-44b8-8fe4-86c0b0c1cb56",
        "word": "Cerebral",
        "meaning": "이성적인, 머리를 쓰는 (감정보다 두뇌 활동을 중시하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "b775c8e9-a7e7-417c-8066-8078996ee58a",
        "word": "Gifted",
        "meaning": "타고난 재능이 있는 (신이 주신 선물 같은)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "df66c54f-211e-4d97-b50c-2f77dfdcbf09",
        "word": "Talented",
        "meaning": "재주가 있는 (특정 분야에 능력이 있는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "83a0372a-af20-491b-a120-06a12e3b55bd",
        "word": "Sharp",
        "meaning": "날카로운, 예리한 (두뇌 회전이 빠르고 정확한)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "99469aa6-62c2-4072-b6c7-38443368296c",
        "word": "Quick-witted",
        "meaning": "두뇌 회전이 빠른 (즉각적으로 반응하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "308df539-54fd-4126-949e-4c0f823c4ec9",
        "word": "Brainy",
        "meaning": "머리가 좋은 (구어체) (공부 잘하는 뉘앙스)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "d980a800-15e3-4276-96c1-1004b832055e",
        "word": "Intellectual",
        "meaning": "지적인 (학문적이고 깊이 생각하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "45c8a895-4285-4cdb-98f4-0fb8b4703e1b",
        "word": "Academic",
        "meaning": "학구적인 (학교 공부나 이론에 강한)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "7ff36eab-1762-4f5f-b852-a227d962c4b6",
        "word": "Clever",
        "meaning": "영리한 (머리를 잘 굴리는, 솜씨 좋은)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "ffb4c506-b601-4559-9d2c-246885bbf11f",
        "word": "Ingenious",
        "meaning": "기발한, 독창적인 (창의적으로 문제를 해결하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "35f026ae-fcfd-4ec2-9a6b-782140032454",
        "word": "Capable",
        "meaning": "유능한 (일을 처리할 능력이 있는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "43ba3949-3391-4ade-b60f-da29b1ad0fd8",
        "word": "Competent",
        "meaning": "능숙한, 적임의 (필요한 수준의 능력을 갖춘)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "5b368227-c990-48e1-be81-7c84f93aeac6",
        "word": "Proficient",
        "meaning": "능란한, 숙달된 (훈련을 통해 잘하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "2f6e8896-d680-420c-9e3d-895782b518e2",
        "word": "Skilled",
        "meaning": "숙련된 (기술이 뛰어난)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "68072f97-933c-4cf5-b915-08cde4451c68",
        "word": "Expert",
        "meaning": "전문적인 (최고 수준의 지식/기술)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "92f5195d-a5c2-4acd-bf88-5debb313348d",
        "word": "Masterful",
        "meaning": "거장다운, 능수능란한 (통제력 있고 뛰어난)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "c10a6cd8-fa5c-44e0-bc29-6d7ae0089c21",
        "word": "Educated",
        "meaning": "교육받은, 교양 있는 (학교 교육을 잘 받은)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "370963e9-6754-4fa4-868a-d8b18b824fa1",
        "word": "Literate",
        "meaning": "글을 읽고 쓸 줄 아는 (기본적인 지식이 있는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "353609e4-ace8-4f99-ab71-bf00a2e0a34e",
        "word": "Well-read",
        "meaning": "다독한 (책을 많이 읽어 지식이 풍부한)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "ca4a352d-2a8b-49ea-8dc5-be49f1066076",
        "word": "Scholarly",
        "meaning": "학자적인 (학문에 정진하는)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    },
    {
        "card_id": "5e9b577b-9ffd-4652-b093-92b929ac542b",
        "word": "Bookish",
        "meaning": "책을 좋아하는 (실생활보다 책에 파묻힌)",
        "deck_id": "03e874a8-6a51-4a58-82b3-232eb4cf7b01",
        "deck_title": "INTELLIGENCE_BRILLIANCE"
    }
]

RELEVANT_TAGS = [
    "warm",
    "technology",
    "startup",
    "smartphone",
    "sad",
    "travel",
    "entrepreneur",
    "interview",
    "job",
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
- 위 태그들은 'INTELLIGENCE_BRILLIANCE' 덱과 관련이 깊은 주제들입니다
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

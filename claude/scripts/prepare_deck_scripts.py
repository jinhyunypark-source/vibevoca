#!/usr/bin/env python3
"""
덱별 예문 생성 스크립트 준비 프로그램

53개 덱에 대해 각각 단어 30개와 적합한 태그 10개를 추출하여
예문 생성 스크립트를 개별적으로 생성합니다.

Usage:
    python prepare_deck_scripts.py
"""

import sys
import os
import json
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


class DeckScriptPreparer:
    def __init__(self):
        self.client = get_supabase_client()

    def get_all_decks(self) -> List[Dict]:
        """모든 덱 목록 가져오기"""
        try:
            result = self.client.table('decks').select('id, title').order('title').execute()
            return result.data
        except Exception as e:
            print(f"Error fetching decks: {e}")
            return []

    def get_words_for_deck(self, deck_id: str, deck_title: str, limit: int = 30) -> List[Dict]:
        """특정 덱의 단어 목록 가져오기"""
        try:
            result = self.client.table('cards').select(
                'id, front_text, back_text'
            ).eq('deck_id', deck_id).limit(limit).execute()

            words = []
            for card in result.data:
                words.append({
                    "card_id": card['id'],
                    "word": card['front_text'],
                    "meaning": card['back_text'],
                    "deck_id": deck_id,
                    "deck_title": deck_title
                })
            return words
        except Exception as e:
            print(f"Error fetching words for deck {deck_title}: {e}")
            return []

    def get_all_tags(self) -> Dict:
        """모든 태그 정보 가져오기"""
        try:
            result = self.client.table('meta_interests').select(
                'id, code, label_en, label_ko, related_tags'
            ).execute()

            tags_by_interest = {}
            all_tags_list = []

            for interest in result.data:
                code = interest['code']
                label_en = interest['label_en']
                tags = interest.get('related_tags', [])

                if tags:
                    tags_by_interest[code] = {
                        "label_en": label_en,
                        "label_ko": interest.get('label_ko', ''),
                        "tags": tags
                    }
                    all_tags_list.extend(tags)

            return {
                "tags_by_interest": tags_by_interest,
                "all_tags": list(set(all_tags_list))
            }
        except Exception as e:
            print(f"Error fetching tags: {e}")
            return {}

    def select_relevant_tags(self, deck_title: str, all_tags_info: Dict, count: int = 10) -> List[str]:
        """
        각 덱에 대해 다양한 태그 선택

        덱 이름과 태그가 완전히 매치될 필요 없음.
        다양한 맥락에서 단어를 사용하는 예문을 만들기 위해 일반적인 태그들 사용.
        """
        # DB에서 가져온 태그
        db_tags = all_tags_info.get('all_tags', [])

        # 더 다양한 일반 태그 추가
        general_tags = [
            'daily_life', 'work', 'business', 'conversation', 'communication',
            'social', 'relationship', 'friendship', 'family',
            'learning', 'education', 'study', 'school', 'university',
            'activity', 'hobby', 'sport', 'exercise',
            'emotion', 'feeling', 'mood',
            'time', 'schedule', 'planning',
            'place', 'home', 'office', 'outdoor',
            'travel', 'journey', 'vacation',
            'food', 'restaurant', 'cooking', 'dining',
            'technology', 'internet', 'digital', 'smartphone',
            'health', 'wellness', 'medical',
            'entertainment', 'movie', 'music', 'art',
            'shopping', 'fashion', 'style',
            'nature', 'environment', 'weather',
            'career', 'job', 'interview', 'meeting'
        ]

        # DB 태그와 일반 태그 결합
        all_available_tags = list(set(db_tags + general_tags))

        # 다양성을 위해 여러 카테고리에서 고르게 선택
        import random
        random.seed(hash(deck_title))  # 덱마다 일관된 결과를 위해

        selected = random.sample(all_available_tags, min(count, len(all_available_tags)))

        return selected

    def generate_script_content(self, deck: Dict, words: List[Dict], tags: List[str]) -> str:
        """개별 덱 스크립트 내용 생성"""

        script_template = f'''#!/usr/bin/env python3
"""
예문 생성 스크립트: {deck['title']}

이 스크립트는 '{deck['title']}' 덱의 단어들에 대해
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


DECK_INFO = {{
    "deck_id": "{deck['id']}",
    "deck_title": "{deck['title']}",
    "total_words": {len(words)}
}}

WORDS = {json.dumps(words, ensure_ascii=False, indent=4)}

RELEVANT_TAGS = {json.dumps(tags, ensure_ascii=False, indent=4)}


class SentenceGenerator:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.client = get_supabase_client()

    def generate_prompt(self, word: str, meaning: str) -> str:
        """예문 생성을 위한 프롬프트"""

        prompt = f"""당신은 영어 학습 예문을 생성하는 전문가입니다.

주어진 영어 단어에 대해 학습자가 쉽게 이해하고 기억할 수 있는 자연스러운 예문을 만들어주세요.

**단어**: {{word}}
**의미**: {{meaning}}

**추천 태그**: {{', '.join(RELEVANT_TAGS)}}
- 위 태그들은 '{deck['title']}' 덱과 관련이 깊은 주제들입니다
- 각 예문에 자연스럽게 어울리는 태그 5개 내외를 선택해주세요
- 모든 태그를 억지로 사용하지 마세요

**요구사항**:
1. 총 5-8개의 예문을 생성해주세요
2. 각 예문은 10-20단어 정도의 자연스러운 문장이어야 합니다
3. 단어 '{{word}}'가 자연스럽게 사용되어야 합니다
4. 다양한 맥락과 상황을 다루어주세요
5. 실생활에서 사용 가능한 자연스러운 문장이어야 합니다
6. **한국어 번역은 자연스러운 한국어로 작성해주세요** (직역이 아닌 의역)

**출력 형식** (JSON):
{{{{
  "sentences": [
    {{{{
      "word": "{{word}}",
      "sentence_en": "영어 예문",
      "sentence_ko": "자연스러운 한국어 번역",
      "tags": ["선택된", "태그", "5개", "내외"]
    }}}}
  ]
}}}}

반드시 위의 JSON 형식으로만 응답해주세요."""

        return prompt

    def call_claude_api(self, prompt: str) -> Dict:
        """Claude API 호출"""
        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {{"role": "user", "content": prompt}}
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
            print(f"  ! Error calling API: {{e}}")
            return {{"sentences": []}}

    def generate_all_sentences(self) -> List[Dict]:
        """모든 단어에 대해 예문 생성"""

        print("=" * 70)
        print(f"예문 생성: {{DECK_INFO['deck_title']}}")
        print("=" * 70)
        print(f"총 단어 수: {{DECK_INFO['total_words']}}")
        print(f"추천 태그: {{', '.join(RELEVANT_TAGS)}}")
        print("=" * 70)

        all_sentences = []

        for i, word_data in enumerate(WORDS, 1):
            print(f"\\n[{{i}}/{{len(WORDS)}}] {{word_data['word']}} ({{word_data['meaning']}})")

            prompt = self.generate_prompt(word_data['word'], word_data['meaning'])
            result = self.call_claude_api(prompt)

            sentences = result.get('sentences', [])

            # card_id와 deck_title 추가
            for sentence in sentences:
                sentence['card_id'] = word_data['card_id']
                sentence['deck_title'] = DECK_INFO['deck_title']

            all_sentences.extend(sentences)
            print(f"  ✓ {{len(sentences)}}개 예문 생성됨")

        return all_sentences

    def save_results(self, sentences: List[Dict], output_file: str):
        """결과를 JSON 파일로 저장"""

        output_data = {{
            "deck_info": DECK_INFO,
            "total_sentences": len(sentences),
            "sentences": sentences
        }}

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\\n✓ 결과 저장: {{output_file}}")
        print(f"  총 {{len(sentences)}}개 예문 생성")

    def print_summary(self, sentences: List[Dict]):
        """생성된 예문 요약 출력"""

        print("\\n" + "=" * 70)
        print("생성 결과 미리보기")
        print("=" * 70)

        # 처음 3개 예문만 출력
        for i, sentence in enumerate(sentences[:3], 1):
            print(f"\\n[예문 {{i}}]")
            print(f"  단어: {{sentence['word']}}")
            print(f"  영문: {{sentence['sentence_en']}}")
            print(f"  한글: {{sentence['sentence_ko']}}")
            print(f"  태그: {{', '.join(sentence['tags'])}}")

        if len(sentences) > 3:
            print(f"\\n... 외 {{len(sentences) - 3}}개 예문")


def main():
    generator = SentenceGenerator()

    # 예문 생성
    sentences = generator.generate_all_sentences()

    # 결과 저장
    output_file = f"output/sentences/{{DECK_INFO['deck_title'].replace('/', '_')}}.json"
    generator.save_results(sentences, output_file)

    # 요약 출력
    generator.print_summary(sentences)

    print("\\n" + "=" * 70)
    print("✓ 완료!")
    print("  검토 후 upload_sentences_to_db.py를 사용해서 DB에 업로드하세요.")
    print("=" * 70)


if __name__ == "__main__":
    main()
'''

        return script_template

    def prepare_all_deck_scripts(self):
        """모든 덱에 대한 스크립트 생성"""

        print("=" * 70)
        print("덱별 예문 생성 스크립트 준비")
        print("=" * 70)

        # 1. 모든 덱 가져오기
        print("\n1. 덱 목록 조회 중...")
        decks = self.get_all_decks()
        print(f"   ✓ {len(decks)}개 덱 발견")

        # 2. 태그 정보 가져오기
        print("\n2. 태그 정보 조회 중...")
        all_tags_info = self.get_all_tags()
        print(f"   ✓ {len(all_tags_info.get('all_tags', []))}개 태그 발견")

        # 3. 각 덱별로 스크립트 생성
        print(f"\n3. {len(decks)}개 덱에 대한 스크립트 생성 중...")

        scripts_dir = "deck_scripts"
        os.makedirs(scripts_dir, exist_ok=True)

        summary = []

        for i, deck in enumerate(decks, 1):
            deck_title = deck['title']
            deck_id = deck['id']

            print(f"\n   [{i}/{len(decks)}] {deck_title}")

            # 단어 가져오기
            words = self.get_words_for_deck(deck_id, deck_title, limit=30)
            if not words:
                print(f"      ! 단어 없음, 스킵")
                continue

            print(f"      • 단어: {len(words)}개")

            # 관련 태그 선택
            tags = self.select_relevant_tags(deck_title, all_tags_info, count=10)
            print(f"      • 태그: {len(tags)}개")

            # 스크립트 내용 생성
            script_content = self.generate_script_content(deck, words, tags)

            # 파일명 생성 (특수문자 제거)
            safe_filename = deck_title.replace('/', '_').replace(' ', '_').replace(':', '_')
            script_path = os.path.join(scripts_dir, f"generate_{safe_filename}.py")

            # 스크립트 파일 저장
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 실행 권한 부여
            os.chmod(script_path, 0o755)

            print(f"      ✓ 저장: {script_path}")

            summary.append({
                "deck_title": deck_title,
                "deck_id": deck_id,
                "word_count": len(words),
                "tag_count": len(tags),
                "script_path": script_path
            })

        # 요약 정보 저장
        summary_path = os.path.join(scripts_dir, "_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 70)
        print(f"✓ 완료! {len(summary)}개 스크립트 생성됨")
        print(f"  디렉토리: {scripts_dir}/")
        print(f"  요약 파일: {summary_path}")
        print("=" * 70)

        return summary


def main():
    preparer = DeckScriptPreparer()
    summary = preparer.prepare_all_deck_scripts()

    print("\n생성된 스크립트 목록:")
    for item in summary[:5]:
        print(f"  • {item['deck_title']}: {item['word_count']}개 단어")

    if len(summary) > 5:
        print(f"  ... 외 {len(summary) - 5}개")


if __name__ == "__main__":
    main()

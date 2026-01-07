#!/usr/bin/env python3
"""
LLM 기반 예문 생성 프로그램

단어 목록과 태그 정보를 받아 Claude API를 사용하여
각 단어별로 자연스러운 예문을 생성합니다.

Usage:
    python generate_sentences_with_llm.py --words words.json --tags tags.json --output sentences.json
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Optional
from anthropic import Anthropic

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


class LLMSentenceGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.anthropic = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.client = get_supabase_client()

    def generate_prompt(self, word: str, meaning: str, tags_info: Dict) -> str:
        """예문 생성을 위한 프롬프트 생성"""

        # 사용 가능한 관심사 태그 목록 생성
        interests_info = []
        for interest, tags in tags_info.get('tags_by_interest', {}).items():
            interests_info.append(f"  - {interest}: {', '.join(tags)}")

        prompt = f"""당신은 영어 학습을 위한 예문을 생성하는 전문가입니다.

주어진 영어 단어에 대해 학습자가 쉽게 이해하고 기억할 수 있는 예문을 만들어주세요.

**단어**: {word}
**의미**: {meaning}

**사용 가능한 관심사 태그**:
{chr(10).join(interests_info)}

**요구사항**:
1. 총 5-10개의 예문을 생성해주세요
2. 각 예문은 위의 관심사 태그 중 하나 이상을 자연스럽게 활용해주세요
3. 예문은 10-20단어 정도로 작성해주세요
4. 단어 '{word}'가 자연스럽게 사용되어야 합니다
5. 다양한 맥락과 상황을 다루어주세요
6. 실생활에서 사용 가능한 자연스러운 문장이어야 합니다

**출력 형식** (JSON):
{{
  "sentences": [
    {{
      "word": "{word}",
      "sentence_en": "영어 예문",
      "sentence_ko": "한국어 번역/설명",
      "tags": ["사용된", "태그들"]
    }}
  ]
}}

반드시 위의 JSON 형식으로만 응답해주세요. 다른 설명은 포함하지 마세요."""

        return prompt

    def call_claude_api(self, prompt: str) -> Optional[Dict]:
        """Claude API 호출"""
        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # 응답에서 JSON 추출
            content = response.content[0].text

            # JSON 파싱 시도
            # Claude가 ```json ... ``` 형식으로 응답할 수 있으므로 처리
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            result = json.loads(json_str)
            return result

        except Exception as e:
            print(f"  ! Error calling Claude API: {e}")
            return None

    def generate_sentences_for_word(
        self,
        word_data: Dict,
        tags_info: Dict,
        count: int = 7
    ) -> List[Dict]:
        """단어에 대한 예문 생성"""

        word = word_data['word']
        meaning = word_data['meaning']

        print(f"\n  Generating sentences for: {word} ({meaning})")

        # 프롬프트 생성
        prompt = self.generate_prompt(word, meaning, tags_info)

        # API 호출
        result = self.call_claude_api(prompt)

        if not result or 'sentences' not in result:
            print(f"  ! Failed to generate sentences for {word}")
            return []

        sentences = result['sentences']

        # card_id 추가
        for sentence in sentences:
            sentence['card_id'] = word_data['card_id']
            sentence['deck_name'] = word_data['deck_name']

        print(f"  ✓ Generated {len(sentences)} sentences")

        return sentences

    def generate_for_all_words(
        self,
        words: List[Dict],
        tags_info: Dict,
        output_path: str
    ) -> List[Dict]:
        """모든 단어에 대해 예문 생성"""

        print("\n" + "=" * 60)
        print("LLM-based Sentence Generation")
        print("=" * 60)
        print(f"Total words: {len(words)}")

        all_sentences = []

        for i, word_data in enumerate(words, 1):
            print(f"\n[{i}/{len(words)}]", end="")

            sentences = self.generate_sentences_for_word(word_data, tags_info)
            all_sentences.extend(sentences)

            # 진행 상황 저장 (중간 저장)
            if i % 10 == 0:
                self.save_to_file(all_sentences, output_path)
                print(f"\n  → Progress saved: {len(all_sentences)} sentences so far")

        # 최종 저장
        self.save_to_file(all_sentences, output_path)

        print("\n" + "=" * 60)
        print(f"Total sentences generated: {len(all_sentences)}")
        print(f"Saved to: {output_path}")
        print("=" * 60)

        return all_sentences

    def save_to_file(self, sentences: List[Dict], output_path: str):
        """예문 목록을 JSON 파일로 저장"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(sentences, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  ! Error saving file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate sentences using LLM")
    parser.add_argument("--words", required=True, help="Input words JSON file")
    parser.add_argument("--tags", required=True, help="Input tags JSON file")
    parser.add_argument("--output", required=True, help="Output sentences JSON file")
    parser.add_argument("--api-key", help="Anthropic API key (or use ANTHROPIC_API_KEY env var)")

    args = parser.parse_args()

    # 단어 목록 로드
    try:
        with open(args.words, 'r', encoding='utf-8') as f:
            words = json.load(f)
    except Exception as e:
        print(f"Error loading words file: {e}")
        return

    # 태그 정보 로드
    try:
        with open(args.tags, 'r', encoding='utf-8') as f:
            tags_info = json.load(f)
    except Exception as e:
        print(f"Error loading tags file: {e}")
        return

    # 예문 생성
    generator = LLMSentenceGenerator(api_key=args.api_key)
    sentences = generator.generate_for_all_words(words, tags_info, args.output)

    print(f"\nGenerated {len(sentences)} sentences for {len(words)} words")


if __name__ == "__main__":
    main()

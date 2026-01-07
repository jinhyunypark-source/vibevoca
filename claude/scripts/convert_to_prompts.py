#!/usr/bin/env python3
"""
Python 스크립트를 웹 LLM용 자연어 프롬프트로 변환

deck_scripts/ 디렉토리의 Python 스크립트를 읽어서
웹 LLM에 바로 복사-붙여넣기 할 수 있는 자연어 프롬프트로 변환합니다.

Usage:
    python convert_to_prompts.py
"""

import os
import json
import re
from typing import Dict, List


class PromptConverter:
    def __init__(self, scripts_dir: str = "deck_scripts", output_dir: str = "claude/deck_prompts"):
        self.scripts_dir = scripts_dir
        self.output_dir = output_dir

    def extract_data_from_script(self, script_path: str) -> Dict:
        """Python 스크립트에서 데이터 추출"""
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Python 코드를 실행해서 변수 추출 (더 안전한 방법)
        import ast

        deck_info = {}
        words = []
        tags = []

        try:
            # DECK_INFO 추출
            deck_info_match = re.search(r'DECK_INFO = ({[^}]+})', content, re.DOTALL)
            if deck_info_match:
                deck_info_str = deck_info_match.group(1)
                deck_info = ast.literal_eval(deck_info_str)
        except:
            pass

        try:
            # WORDS 추출 - 더 넓은 패턴으로 매칭
            words_match = re.search(r'WORDS = \[(.*?)\n\]', content, re.DOTALL)
            if words_match:
                words_str = '[' + words_match.group(1) + '\n]'
                words = ast.literal_eval(words_str)
        except:
            pass

        try:
            # RELEVANT_TAGS 추출
            tags_match = re.search(r'RELEVANT_TAGS = (\[.*?\])', content, re.DOTALL)
            if tags_match:
                tags_str = tags_match.group(1)
                tags = ast.literal_eval(tags_str)
        except:
            pass

        return {
            "deck_info": deck_info,
            "words": words,
            "tags": tags
        }

    def create_prompt(self, data: Dict) -> str:
        """자연어 프롬프트 생성"""

        deck_info = data['deck_info']
        words = data['words']
        tags = data['tags']

        deck_title = deck_info.get('deck_title', '')
        total_words = deck_info.get('total_words', len(words))

        # 단어 목록을 보기 좋게 포맷팅
        words_list = []
        for i, word_data in enumerate(words, 1):
            word = word_data['word']
            meaning = word_data['meaning']
            words_list.append(f"{i}. {word} - {meaning}")

        words_text = '\n'.join(words_list)

        # 태그 목록
        tags_text = ', '.join(tags)

        # 프롬프트 템플릿
        prompt = f"""# 영어 학습 예문 생성 요청

## 덱 정보
- **덱 이름**: {deck_title}
- **총 단어 수**: {total_words}개

## 단어 목록
{words_text}

## 추천 태그 (상황/맥락)
{tags_text}

## 작업 요구사항

당신은 영어 학습 예문을 생성하는 전문가입니다. 위의 단어들에 대해 학습자가 쉽게 이해하고 기억할 수 있는 자연스러운 예문을 만들어주세요.

### 예문 생성 가이드라인

1. **예문 개수**: 각 단어당 5-8개의 예문 생성
2. **예문 길이**: 10-20단어 정도의 자연스러운 문장
3. **태그 활용**:
   - 위의 추천 태그(상황/맥락)를 자연스럽게 활용
   - 각 예문마다 어울리는 태그 5개 내외만 선택
   - **중요**: 모든 태그를 억지로 사용하지 말 것
4. **다양성**: 다양한 맥락과 상황을 다룰 것
5. **실용성**: 실생활에서 사용 가능한 자연스러운 문장
6. **한국어 번역**:
   - 직역이 아닌 **자연스러운 한국어 의역**
   - 한국인이 실제로 사용하는 표현으로 번역

### 출력 형식

반드시 아래의 JSON 형식으로 출력해주세요:

```json
{{
  "deck_title": "{deck_title}",
  "total_sentences": 0,
  "sentences": [
    {{
      "word": "단어",
      "sentence_en": "영어 예문",
      "sentence_ko": "자연스러운 한국어 번역",
      "tags": ["선택된", "태그", "5개", "내외"]
    }}
  ]
}}
```

### 예시

```json
{{
  "deck_title": "{deck_title}",
  "total_sentences": 2,
  "sentences": [
    {{
      "word": "prudent",
      "sentence_en": "A prudent investor always diversifies their portfolio to minimize risk.",
      "sentence_ko": "신중한 투자자는 리스크를 최소화하기 위해 항상 포트폴리오를 분산시킵니다.",
      "tags": ["business", "work", "planning"]
    }},
    {{
      "word": "sage",
      "sentence_en": "The sage advice from my mentor helped me navigate the difficult decision.",
      "sentence_ko": "멘토의 현명한 조언 덕분에 어려운 결정을 내릴 수 있었습니다.",
      "tags": ["conversation", "relationship", "learning"]
    }}
  ]
}}
```

이제 위의 {total_words}개 단어에 대해 예문을 생성해주세요. JSON 형식으로만 응답해주시고, 다른 설명은 포함하지 마세요.
"""

        return prompt

    def convert_all_scripts(self):
        """모든 스크립트를 프롬프트로 변환"""

        print("=" * 70)
        print("Python 스크립트 → 자연어 프롬프트 변환")
        print("=" * 70)

        # 출력 디렉토리 생성
        os.makedirs(self.output_dir, exist_ok=True)

        # 모든 Python 스크립트 찾기
        script_files = [f for f in os.listdir(self.scripts_dir)
                       if f.startswith('generate_') and f.endswith('.py')]

        print(f"\n발견된 스크립트: {len(script_files)}개")
        print(f"출력 디렉토리: {self.output_dir}/")
        print()

        converted = []

        for i, script_file in enumerate(sorted(script_files), 1):
            script_path = os.path.join(self.scripts_dir, script_file)

            # 덱 이름 추출 (generate_DECK_NAME.py → DECK_NAME)
            deck_name = script_file.replace('generate_', '').replace('.py', '')

            print(f"[{i}/{len(script_files)}] {deck_name}")

            # 데이터 추출
            try:
                data = self.extract_data_from_script(script_path)

                # 프롬프트 생성
                prompt = self.create_prompt(data)

                # 프롬프트 파일 저장
                prompt_filename = f"{deck_name}_prompt.txt"
                prompt_path = os.path.join(self.output_dir, prompt_filename)

                with open(prompt_path, 'w', encoding='utf-8') as f:
                    f.write(prompt)

                print(f"    ✓ 저장: {prompt_path}")

                converted.append({
                    "deck_name": deck_name,
                    "deck_title": data['deck_info'].get('deck_title', ''),
                    "word_count": len(data['words']),
                    "tag_count": len(data['tags']),
                    "prompt_file": prompt_filename
                })

            except Exception as e:
                print(f"    ! 오류: {e}")

        # 요약 파일 저장
        summary_path = os.path.join(self.output_dir, "_prompts_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(converted, f, ensure_ascii=False, indent=2)

        print("\n" + "=" * 70)
        print(f"✓ 완료! {len(converted)}개 프롬프트 생성됨")
        print(f"  디렉토리: {self.output_dir}/")
        print(f"  요약 파일: {summary_path}")
        print("=" * 70)

        return converted


def main():
    converter = PromptConverter()
    converted = converter.convert_all_scripts()

    print("\n생성된 프롬프트 파일:")
    for item in converted[:5]:
        print(f"  • {item['deck_name']}: {item['word_count']}개 단어, {item['tag_count']}개 태그")

    if len(converted) > 5:
        print(f"  ... 외 {len(converted) - 5}개")

    print("\n사용 방법:")
    print("  1. deck_prompts/ 폴더에서 원하는 덱의 _prompt.txt 파일 열기")
    print("  2. 전체 내용을 복사")
    print("  3. 웹 LLM (ChatGPT, Claude 등)에 붙여넣기")
    print("  4. 생성된 JSON 결과를 저장")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AI를 활용한 단어/예문 생성 스크립트

사용법:
    python ai_generator.py generate-words <deck_id> --count 5
    python ai_generator.py generate-example <card_id> --place cafe --emotion happy --environment quiet
    python ai_generator.py improve-definition <card_id>
    python ai_generator.py suggest-similar <card_id> --count 3
"""

import argparse
import json
import os
import sys

# Anthropic API 사용
try:
    import anthropic
except ImportError:
    print("anthropic 패키지가 필요합니다: pip install anthropic")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client, Tables


def get_claude_client():
    """Anthropic Claude 클라이언트 반환"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
    return anthropic.Anthropic(api_key=api_key)


def load_prompt_template(template_name):
    """프롬프트 템플릿 로드"""
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
    prompt_file = os.path.join(prompts_dir, "word_prompts.md")

    with open(prompt_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 간단한 섹션 파싱 (실제 구현에서는 더 정교하게)
    return content


def generate_words(deck_id, count=5):
    """AI를 사용하여 새 단어 생성"""
    supabase = get_supabase_client()
    claude = get_claude_client()

    # 데크 정보 조회
    deck = supabase.table(Tables.DECKS).select("*").eq("id", deck_id).single().execute()
    if not deck.data:
        print(f"데크를 찾을 수 없습니다: {deck_id}")
        return

    deck_data = deck.data

    # 기존 단어들 조회
    existing = supabase.table(Tables.CARDS).select("front_text").eq("deck_id", deck_id).execute()
    existing_words = [c['front_text'] for c in existing.data]

    prompt = f"""당신은 영어 어휘 학습 전문가입니다. 다음 데크에 맞는 새로운 영어 단어를 생성해주세요.

데크: {deck_data['title']} ({deck_data.get('title_ko', '')})
기존 단어들: {', '.join(existing_words[:20])}...

요구사항:
1. 기존 단어와 중복되지 않는 새 단어 {count}개 생성
2. 데크 주제에 맞는 단어 선택
3. 각 단어에 대해 다음 정보 제공

JSON 배열 형식으로만 출력 (다른 텍스트 없이):
[
  {{
    "front_text": "영어 단어/표현",
    "back_text": "한글 뜻",
    "example_sentences": ["예문1", "예문2"]
  }}
]"""

    print(f"\n🤖 AI가 '{deck_data['title']}' 데크에 맞는 단어 {count}개를 생성 중...")

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text

    try:
        # JSON 파싱
        words = json.loads(result_text)

        print(f"\n✅ {len(words)}개의 단어 생성 완료:\n")
        for i, word in enumerate(words, 1):
            print(f"{i}. {word['front_text']} - {word['back_text']}")
            for ex in word.get('example_sentences', []):
                print(f"   예: {ex}")
            print()

        return words
    except json.JSONDecodeError:
        print("AI 응답 파싱 실패:")
        print(result_text)
        return None


def generate_example(card_id, place=None, emotion=None, environment=None):
    """AI를 사용하여 컨텍스트 기반 예문 생성"""
    supabase = get_supabase_client()
    claude = get_claude_client()

    # 카드 정보 조회
    card = supabase.table(Tables.CARDS).select("*").eq("id", card_id).single().execute()
    if not card.data:
        print(f"카드를 찾을 수 없습니다: {card_id}")
        return

    card_data = card.data

    prompt = f"""당신은 영어 문장 작성 전문가입니다. 주어진 단어와 컨텍스트에 맞는 자연스러운 예문을 생성해주세요.

단어: {card_data['front_text']}
의미: {card_data['back_text']}
컨텍스트:
  - 장소: {place or '일반'}
  - 감정: {emotion or '중립'}
  - 환경: {environment or '일상'}

요구사항:
1. 컨텍스트에 맞는 자연스러운 예문 1개 생성
2. 일상적인 상황에서 사용할 수 있는 문장
3. 단어의 의미가 명확히 드러나는 문장

JSON 형식으로만 출력:
{{
  "sentence": "영어 예문",
  "translation": "한글 번역"
}}"""

    print(f"\n🤖 '{card_data['front_text']}' 단어의 컨텍스트 예문 생성 중...")

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text

    try:
        example = json.loads(result_text)
        print(f"\n✅ 예문 생성 완료:")
        print(f"   영어: {example['sentence']}")
        print(f"   한글: {example['translation']}")
        return example
    except json.JSONDecodeError:
        print("AI 응답 파싱 실패:")
        print(result_text)
        return None


def improve_definition(card_id):
    """AI를 사용하여 단어 설명 개선"""
    supabase = get_supabase_client()
    claude = get_claude_client()

    card = supabase.table(Tables.CARDS).select("*").eq("id", card_id).single().execute()
    if not card.data:
        print(f"카드를 찾을 수 없습니다: {card_id}")
        return

    card_data = card.data

    prompt = f"""당신은 영어 교육 전문가입니다. 다음 단어의 설명을 더 이해하기 쉽게 개선해주세요.

단어: {card_data['front_text']}
현재 설명: {card_data['back_text']}

요구사항:
1. 간결하고 명확한 한글 설명
2. 핵심 의미를 잘 전달
3. 학습자가 쉽게 기억할 수 있는 표현

JSON 형식으로만 출력:
{{
  "improved_definition": "개선된 설명"
}}"""

    print(f"\n🤖 '{card_data['front_text']}' 단어 설명 개선 중...")

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text

    try:
        result = json.loads(result_text)
        print(f"\n✅ 설명 개선 완료:")
        print(f"   기존: {card_data['back_text']}")
        print(f"   개선: {result['improved_definition']}")
        return result
    except json.JSONDecodeError:
        print("AI 응답 파싱 실패:")
        print(result_text)
        return None


def suggest_similar(card_id, count=3):
    """AI를 사용하여 유사 단어 추천"""
    supabase = get_supabase_client()
    claude = get_claude_client()

    card = supabase.table(Tables.CARDS).select("*").eq("id", card_id).single().execute()
    if not card.data:
        print(f"카드를 찾을 수 없습니다: {card_id}")
        return

    card_data = card.data

    # 데크 정보도 조회
    deck = supabase.table(Tables.DECKS).select("title, title_ko").eq("id", card_data['deck_id']).single().execute()
    deck_data = deck.data if deck.data else {}

    prompt = f"""당신은 영어 어휘 전문가입니다. 주어진 단어와 관련된 유사 단어를 추천해주세요.

기준 단어: {card_data['front_text']}
의미: {card_data['back_text']}
데크: {deck_data.get('title', '')} ({deck_data.get('title_ko', '')})

요구사항:
1. 의미가 유사하거나 관련된 단어 {count}개 추천
2. 각 단어의 뜻과 차이점 설명
3. 학습에 도움이 되는 단어 선택

JSON 배열 형식으로만 출력:
[
  {{
    "word": "유사 단어",
    "meaning": "뜻",
    "difference": "기준 단어와의 차이점"
  }}
]"""

    print(f"\n🤖 '{card_data['front_text']}'와 유사한 단어 추천 중...")

    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    result_text = response.content[0].text

    try:
        suggestions = json.loads(result_text)
        print(f"\n✅ 유사 단어 {len(suggestions)}개 추천:")
        for i, s in enumerate(suggestions, 1):
            print(f"\n{i}. {s['word']} - {s['meaning']}")
            print(f"   차이점: {s['difference']}")
        return suggestions
    except json.JSONDecodeError:
        print("AI 응답 파싱 실패:")
        print(result_text)
        return None


def main():
    parser = argparse.ArgumentParser(description="AI 기반 단어/예문 생성")
    subparsers = parser.add_subparsers(dest="command", help="명령어")

    # generate-words
    gen_words = subparsers.add_parser("generate-words", help="새 단어 생성")
    gen_words.add_argument("deck_id", help="데크 ID")
    gen_words.add_argument("--count", type=int, default=5, help="생성할 단어 수")

    # generate-example
    gen_example = subparsers.add_parser("generate-example", help="컨텍스트 예문 생성")
    gen_example.add_argument("card_id", help="카드 ID")
    gen_example.add_argument("--place", help="장소 컨텍스트")
    gen_example.add_argument("--emotion", help="감정 컨텍스트")
    gen_example.add_argument("--environment", help="환경 컨텍스트")

    # improve-definition
    improve = subparsers.add_parser("improve-definition", help="단어 설명 개선")
    improve.add_argument("card_id", help="카드 ID")

    # suggest-similar
    suggest = subparsers.add_parser("suggest-similar", help="유사 단어 추천")
    suggest.add_argument("card_id", help="카드 ID")
    suggest.add_argument("--count", type=int, default=3, help="추천할 단어 수")

    args = parser.parse_args()

    if args.command == "generate-words":
        generate_words(args.deck_id, args.count)
    elif args.command == "generate-example":
        generate_example(args.card_id, args.place, args.emotion, args.environment)
    elif args.command == "improve-definition":
        improve_definition(args.card_id)
    elif args.command == "suggest-similar":
        suggest_similar(args.card_id, args.count)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

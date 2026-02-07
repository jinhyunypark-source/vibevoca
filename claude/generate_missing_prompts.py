"""
누락된 이미지용 프롬프트 생성 스크립트

작업 내용:
1. missing_images.json에서 누락된 단어 목록 로드
2. 64개씩 그룹으로 나누어 프롬프트 파일 생성
3. missing_prompts_output/ 폴더에 저장

실행 방법:
    python claude/generate_missing_prompts.py

작성일: 2026-01-13
"""
import os
import json

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 입력
MISSING_JSON = os.path.join(SCRIPT_DIR, 'missing_images.json')

# 출력
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'missing_prompts_output')

# 프롬프트 설정
WORDS_PER_FILE = 64

# 프롬프트 템플릿 (기존과 동일)
PROMPT_TEMPLATE = """단어 하나당 하나씩의 이미지를 만들고, 그 이미지를 총 64개 가로 8개 세로 8개 모은 더 큰 하나의 이미지를 만든다. 이미지는 제시된 단어의 순서대로 좌상단에서 우상단으로, 그리고 다음줄로 순서를 반드시 지켜야 한다. 단어는 다음과 같다. 최종 아웃풋은 정확하게 픽셀로 자를수 있게 2048*2048 크기로 만든다.

{words}

각 단어의 이미지는:
- 단어의 핵심 의미를 직관적으로 표현
- 간결하고 명확한 비주얼
- 8*8 그리드 정사각 형태로 배열
- 각 이미지는 동일한 크기
- 단어의 이미지 테두리 표시 하지 않고, 배경 흰색으로 통일
- 단어가 64개 미만인 경우, 나머지 칸은 흰색 공백으로 채움
"""
# ============================================


def load_missing_words():
    """누락된 단어 목록 로드"""
    with open(MISSING_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 중복 제거 (같은 단어가 여러 card에 있을 수 있음)
    seen = set()
    unique_words = []
    for card in data['cards']:
        word = card['word']
        if word not in seen:
            seen.add(word)
            unique_words.append(word)

    return unique_words


def generate_prompts():
    """프롬프트 파일 생성"""
    print("=" * 60)
    print("누락 이미지용 프롬프트 생성")
    print("=" * 60 + "\n")

    # 누락된 단어 로드
    print("누락된 단어 로드 중...")
    words = load_missing_words()
    print(f"총 단어 수: {len(words)}개 (중복 제거 후)\n")

    # 출력 폴더 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 64개씩 그룹으로 나누기
    groups = []
    for i in range(0, len(words), WORDS_PER_FILE):
        groups.append(words[i:i + WORDS_PER_FILE])

    print(f"생성할 프롬프트 파일: {len(groups)}개")
    print(f"  - 파일당 단어 수: {WORDS_PER_FILE}개")
    print(f"  - 마지막 파일 단어 수: {len(groups[-1])}개\n")

    # 프롬프트 파일 생성
    for i, group in enumerate(groups, 1):
        # 단어 목록 포맷
        words_text = ",\n".join(group)

        # 프롬프트 생성
        prompt = PROMPT_TEMPLATE.format(words=words_text)

        # 파일 저장
        filename = f"missing_{i}_prompt.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(prompt)

        print(f"  생성됨: {filename} ({len(group)}개 단어)")

    # 단어 목록 파일도 생성 (이미지 분할 시 매핑용)
    print("\n단어 목록 파일 생성 중...")
    for i, group in enumerate(groups, 1):
        filename = f"missing_{i}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            for word in group:
                f.write(word + "\n")

        print(f"  생성됨: {filename}")

    # 결과 요약
    print("\n" + "=" * 60)
    print("완료!")
    print("=" * 60)
    print(f"\n출력 폴더: {OUTPUT_DIR}")
    print(f"프롬프트 파일: missing_1_prompt.txt ~ missing_{len(groups)}_prompt.txt")
    print(f"단어 파일: missing_1.txt ~ missing_{len(groups)}.txt")

    # 사용 안내
    print("\n" + "-" * 60)
    print("사용 방법:")
    print("-" * 60)
    print("1. missing_X_prompt.txt 내용을 AI 이미지 생성 도구에 입력")
    print("2. 생성된 2048x2048 이미지를 input_image/missing_X.png로 저장")
    print("3. split_images.py 수정하여 missing 이미지 처리")
    print("-" * 60)

    return groups


if __name__ == "__main__":
    generate_prompts()

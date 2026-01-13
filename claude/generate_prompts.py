"""
단어 파일에서 이미지 생성용 프롬프트 생성 스크립트

작업 내용:
- word_files/ 디렉토리의 각 txt 파일을 읽어서
- 파일 내 단어들을 사용해 이미지 생성 프롬프트 생성
- 생성된 프롬프트를 word_prompts_output/ 디렉토리에 저장

설정:
- 64개 단어 기준 8x8 그리드
- 최종 이미지 크기: 2048x2048 픽셀
- 배경: 흰색, 테두리: 없음

실행 방법:
    python claude/generate_prompts.py

작성일: 2026-01-12
수정일: 2026-01-12 (6x6 36개 → 8x8 64개로 변경)
자세한 내용: WORK_LOG.md 참고
"""
import os
import glob

# ==================== 프롬프트 템플릿 설정 ====================
# 이 부분을 수정하여 프롬프트 내용을 변경할 수 있습니다

PROMPT_TEMPLATE = """단어 하나당 하나씩의 이미지를 만들고, 그 이미지를 총 64개 가로 8개 세로 8개 모은 더 큰 하나의 이미지를 만든다. 이미지는 제시된 단어의 순서대로 좌상단에서 우상단으로, 그리고 다음줄로 순서를 반드시 지켜야 한다. 단어는 다음과 같다. 최종 아웃풋은 정확하게 픽셀로 자를수 있게 2048*2048 크기로 만든다.

{words}

각 단어의 이미지는:
- 단어의 핵심 의미를 직관적으로 표현
- 최대한 디테일한 표현, 명확한 비주얼, 다채로운 색상도 좋다.
- 8*8 그리드 정사각 형태로 배열
- 각 이미지는 동일한 크기
- 단어의 작은 이미지를 코딩으로 정확하게 자를수 있도록 , 테두리 경계를 넘어서면 안된다. 
- 배경 흰색으로 통일
"""

# 프롬프트 접두사/접미사 (필요시 추가)
PROMPT_PREFIX = ""  # 프롬프트 앞에 추가할 내용
PROMPT_SUFFIX = ""  # 프롬프트 뒤에 추가할 내용

# ============================================================


def read_words_from_file(file_path):
    """텍스트 파일에서 단어 목록 읽기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words


def format_words_list(words):
    """단어 목록을 프롬프트에 삽입할 형식으로 변환"""
    # 콤마로 구분하여 한 줄로 작성
    return ",\n".join(words)


def generate_prompt(words):
    """단어 목록으로 프롬프트 생성"""
    words_text = format_words_list(words)
    prompt = PROMPT_TEMPLATE.format(words=words_text)

    # 접두사/접미사 추가
    if PROMPT_PREFIX:
        prompt = PROMPT_PREFIX + "\n\n" + prompt
    if PROMPT_SUFFIX:
        prompt = prompt + "\n\n" + PROMPT_SUFFIX

    return prompt


def main():
    """메인 실행 함수"""
    # 디렉토리 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    word_files_dir = os.path.join(script_dir, 'word_files')
    output_dir = os.path.join(script_dir, 'word_prompts_output')

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # word_files 디렉토리의 모든 txt 파일 찾기
    txt_files = sorted(glob.glob(os.path.join(word_files_dir, '*.txt')),
                      key=lambda x: int(os.path.basename(x).split('.')[0]))

    if not txt_files:
        print(f"'{word_files_dir}' 디렉토리에 txt 파일이 없습니다.")
        return

    print(f"총 {len(txt_files)}개의 파일을 처리합니다.\n")

    # 각 파일 처리
    for txt_file in txt_files:
        # 파일명에서 번호 추출
        filename = os.path.basename(txt_file)
        file_number = filename.split('.')[0]

        # 단어 읽기
        words = read_words_from_file(txt_file)

        if not words:
            print(f"{filename}: 단어가 없습니다. 건너뜁니다.")
            continue

        # 프롬프트 생성
        prompt = generate_prompt(words)

        # 프롬프트 저장
        output_filename = f"{file_number}_prompt.txt"
        output_path = os.path.join(output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)

        print(f"{output_filename} 생성 완료 ({len(words)}개 단어)")

    print(f"\n모든 프롬프트가 '{output_dir}' 디렉토리에 생성되었습니다.")
    print(f"\n프롬프트 템플릿을 수정하려면 스크립트 상단의 PROMPT_TEMPLATE 변수를 편집하세요.")


if __name__ == "__main__":
    main()

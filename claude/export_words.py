"""
Supabase cards 테이블 영어 단어 추출 스크립트

작업 내용:
- Supabase의 cards 테이블에서 front_text (영어 단어) 추출
- 64개씩 그룹으로 나누어 텍스트 파일로 저장
- 결과물: word_files/ 디렉토리에 1.txt ~ N.txt 파일 생성

실행 방법:
    source backend/venv/bin/activate
    python claude/export_words.py

작성일: 2026-01-12
수정일: 2026-01-12 (36개 → 64개로 변경)
자세한 내용: WORK_LOG.md 참고
"""
import os
from supabase import create_client
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = os.environ.get("SUPABASE_URL")
    # SUPABASE_KEY가 없으면 SUPABASE_ANON_KEY 사용
    key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_KEY/SUPABASE_ANON_KEY가 설정되지 않았습니다.")

    return create_client(url, key)

def export_words_to_files():
    """cards 테이블에서 영어 단어를 가져와 36개씩 파일로 저장"""
    # Supabase 클라이언트 생성
    supabase = get_supabase_client()

    # cards 테이블에서 영어 단어 가져오기 (front_text 필드 사용)
    # Supabase는 기본적으로 1000개까지만 반환하므로 전체 데이터를 가져오기 위해 반복
    all_words = []
    batch_size = 1000
    offset = 0

    while True:
        response = supabase.table("cards").select("front_text").range(offset, offset + batch_size - 1).execute()

        if not response.data:
            break

        # 단어 추출
        batch_words = [card['front_text'] for card in response.data if card.get('front_text')]
        all_words.extend(batch_words)

        print(f"{offset + 1}~{offset + len(response.data)}번째 카드 가져오기 완료")

        # 더 이상 데이터가 없으면 중단
        if len(response.data) < batch_size:
            break

        offset += batch_size

    print(f"\n총 {len(all_words)}개의 영어 단어를 찾았습니다.")
    words = all_words

    # 출력 디렉토리 생성
    output_dir = os.path.join(os.path.dirname(__file__), 'word_files')
    os.makedirs(output_dir, exist_ok=True)

    # 64개씩 나누어 파일로 저장
    words_per_file = 64
    total_files = (len(words) + words_per_file - 1) // words_per_file

    for i in range(total_files):
        start_idx = i * words_per_file
        end_idx = min((i + 1) * words_per_file, len(words))
        file_words = words[start_idx:end_idx]

        # 파일 저장
        filename = os.path.join(output_dir, f"{i + 1}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            for word in file_words:
                f.write(f"{word}\n")

        print(f"{i + 1}.txt 파일 생성 완료 ({len(file_words)}개 단어)")

    print(f"\n총 {total_files}개의 파일이 '{output_dir}' 디렉토리에 생성되었습니다.")

if __name__ == "__main__":
    export_words_to_files()

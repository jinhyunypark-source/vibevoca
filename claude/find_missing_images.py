"""
이미지가 없는 카드 찾기 스크립트

작업 내용:
1. Supabase cards 테이블에서 전체 카드 조회
2. assets/word_images/ 폴더의 이미지와 비교
3. 이미지가 없는 카드의 ID와 단어를 파일로 출력

실행 방법:
    source backend/venv/bin/activate
    python claude/find_missing_images.py

작성일: 2026-01-13
"""
import os
import json
from dotenv import load_dotenv
from supabase import create_client

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 환경 변수 로드
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# 이미지 폴더
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets', 'word_images')

# 출력 파일
OUTPUT_DIR = SCRIPT_DIR
OUTPUT_TXT = os.path.join(OUTPUT_DIR, 'missing_images.txt')
OUTPUT_JSON = os.path.join(OUTPUT_DIR, 'missing_images.json')
OUTPUT_CSV = os.path.join(OUTPUT_DIR, 'missing_images.csv')
# ============================================


def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def get_all_cards(supabase):
    """cards 테이블에서 전체 카드 가져오기 (페이지네이션)"""
    all_cards = []
    batch_size = 1000
    offset = 0

    while True:
        response = supabase.table("cards").select("id, front_text").range(offset, offset + batch_size - 1).execute()

        if not response.data:
            break

        all_cards.extend(response.data)

        if len(response.data) < batch_size:
            break

        offset += batch_size

    return all_cards


def get_existing_images():
    """assets/word_images/ 폴더의 이미지 파일 목록 (card_id 추출)"""
    existing_ids = set()

    if not os.path.exists(ASSETS_DIR):
        print(f"경고: 이미지 폴더가 없습니다: {ASSETS_DIR}")
        return existing_ids

    for filename in os.listdir(ASSETS_DIR):
        if filename.endswith('.jpg'):
            # 파일명에서 .jpg 제거하면 card_id
            card_id = filename[:-4]
            existing_ids.add(card_id)

    return existing_ids


def find_missing_images():
    """이미지가 없는 카드 찾기"""
    print("=" * 60)
    print("이미지 누락 카드 찾기")
    print("=" * 60 + "\n")

    # Supabase 연결
    print("Supabase 연결 중...")
    supabase = get_supabase_client()

    # 전체 카드 조회
    print("전체 카드 조회 중...")
    all_cards = get_all_cards(supabase)
    print(f"총 카드 수: {len(all_cards)}개\n")

    # 이미지 파일 목록
    print("이미지 파일 확인 중...")
    existing_images = get_existing_images()
    print(f"이미지 파일 수: {len(existing_images)}개\n")

    # 이미지가 없는 카드 찾기
    missing_cards = []
    for card in all_cards:
        card_id = card['id']
        word = card['front_text']

        if card_id not in existing_images:
            missing_cards.append({
                'id': card_id,
                'word': word
            })

    # 단어 기준으로 정렬
    missing_cards.sort(key=lambda x: x['word'].lower())

    # 결과 출력
    print("=" * 60)
    print(f"이미지 누락 카드: {len(missing_cards)}개")
    print(f"비율: {len(missing_cards) / len(all_cards) * 100:.1f}%")
    print("=" * 60 + "\n")

    # TXT 파일 저장
    print("TXT 파일 저장 중...")
    with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
        f.write(f"# 이미지 누락 카드 목록\n")
        f.write(f"# 총 {len(missing_cards)}개 / 전체 {len(all_cards)}개\n")
        f.write(f"# 생성일: 2026-01-13\n\n")

        for card in missing_cards:
            f.write(f"{card['id']}\t{card['word']}\n")

    # JSON 파일 저장
    print("JSON 파일 저장 중...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'total_cards': len(all_cards),
            'missing_count': len(missing_cards),
            'missing_ratio': f"{len(missing_cards) / len(all_cards) * 100:.1f}%",
            'cards': missing_cards
        }, f, ensure_ascii=False, indent=2)

    # CSV 파일 저장
    print("CSV 파일 저장 중...")
    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        f.write("id,word\n")
        for card in missing_cards:
            # CSV 이스케이프 처리
            word = card['word'].replace('"', '""')
            if ',' in word or '"' in word:
                word = f'"{word}"'
            f.write(f"{card['id']},{word}\n")

    # 결과 요약
    print("\n" + "-" * 60)
    print("출력 파일:")
    print(f"  - {OUTPUT_TXT}")
    print(f"  - {OUTPUT_JSON}")
    print(f"  - {OUTPUT_CSV}")
    print("-" * 60)

    # 샘플 출력
    print("\n샘플 (처음 10개):")
    for card in missing_cards[:10]:
        print(f"  {card['word']}")

    if len(missing_cards) > 10:
        print(f"  ... 외 {len(missing_cards) - 10}개")

    return missing_cards


if __name__ == "__main__":
    find_missing_images()

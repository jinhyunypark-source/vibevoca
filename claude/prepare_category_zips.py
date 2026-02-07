"""
카테고리별 이미지 ZIP 파일 생성 스크립트

작업 내용:
1. Supabase에서 categories → decks → cards 조회
2. 카테고리별 card_id 목록 추출
3. assets/word_images/에서 해당 이미지 수집
4. 카테고리별 ZIP 파일 생성
5. manifest.json 생성 (버전, 파일크기, 이미지 수)

실행 방법:
    source backend/venv/bin/activate
    python claude/prepare_category_zips.py --list          # 카테고리 목록 확인
    python claude/prepare_category_zips.py --create-all    # 전체 ZIP 생성
    python claude/prepare_category_zips.py --create <id>   # 특정 카테고리만

작성일: 2026-01-13
"""
import os
import sys
import json
import zipfile
import argparse
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 환경 변수 로드
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# 입력
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'assets', 'word_images')

# 출력
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'category_zips')
MANIFEST_FILE = os.path.join(OUTPUT_DIR, 'manifest.json')

# 버전
MANIFEST_VERSION = 1
# ============================================


def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def get_categories(supabase):
    """카테고리 목록 조회"""
    response = supabase.table("categories").select("*").order("created_at").execute()
    return response.data


def get_decks_by_category(supabase, category_id):
    """카테고리의 덱 목록 조회"""
    response = supabase.table("decks").select("id, title").eq("category_id", category_id).execute()
    return response.data


def get_cards_by_deck(supabase, deck_id):
    """덱의 카드 목록 조회"""
    response = supabase.table("cards").select("id, front_text").eq("deck_id", deck_id).execute()
    return response.data


def get_category_cards(supabase, category_id):
    """카테고리의 모든 카드 ID 조회"""
    decks = get_decks_by_category(supabase, category_id)
    all_cards = []

    for deck in decks:
        cards = get_cards_by_deck(supabase, deck['id'])
        for card in cards:
            all_cards.append({
                'id': card['id'],
                'word': card['front_text'],
                'deck_id': deck['id'],
                'deck_title': deck['title']
            })

    return all_cards


def create_category_zip(category, cards, images_dir, output_dir):
    """카테고리 ZIP 파일 생성"""
    category_id = category['id']
    category_title = category.get('title_ko') or category['title']

    # ZIP 파일명 (안전한 파일명 생성)
    safe_title = "".join(c if c.isalnum() else "_" for c in category_title)
    zip_filename = f"{category_id}.zip"
    zip_path = os.path.join(output_dir, zip_filename)

    # ZIP 생성
    found_count = 0
    missing_count = 0
    total_size = 0

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for card in cards:
            image_filename = f"{card['id']}.jpg"
            image_path = os.path.join(images_dir, image_filename)

            if os.path.exists(image_path):
                zf.write(image_path, image_filename)
                total_size += os.path.getsize(image_path)
                found_count += 1
            else:
                missing_count += 1

    zip_size = os.path.getsize(zip_path)

    return {
        'category_id': category_id,
        'category_title': category_title,
        'file_name': zip_filename,
        'zip_size_bytes': zip_size,
        'image_count': found_count,
        'missing_count': missing_count,
        'total_cards': len(cards),
        'updated_at': datetime.now().isoformat()
    }


def list_categories():
    """카테고리 목록 출력"""
    print("=" * 70)
    print("카테고리 목록")
    print("=" * 70 + "\n")

    supabase = get_supabase_client()
    categories = get_categories(supabase)

    print(f"{'No':<4} {'ID':<38} {'Title':<20} {'Cards':<8}")
    print("-" * 70)

    for i, cat in enumerate(categories, 1):
        cards = get_category_cards(supabase, cat['id'])
        title = cat.get('title_ko') or cat['title']
        print(f"{i:<4} {cat['id']:<38} {title:<20} {len(cards):<8}")

    print(f"\n총 {len(categories)}개 카테고리")


def create_all_zips():
    """전체 카테고리 ZIP 생성"""
    print("=" * 70)
    print("카테고리별 ZIP 파일 생성")
    print("=" * 70 + "\n")

    # 출력 폴더 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    supabase = get_supabase_client()
    categories = get_categories(supabase)

    print(f"총 {len(categories)}개 카테고리 처리 예정\n")

    manifest_packs = []

    for i, cat in enumerate(categories, 1):
        title = cat.get('title_ko') or cat['title']
        print(f"[{i}/{len(categories)}] {title} 처리 중...")

        # 카드 조회
        cards = get_category_cards(supabase, cat['id'])
        print(f"  - 카드 수: {len(cards)}개")

        # ZIP 생성
        result = create_category_zip(cat, cards, IMAGES_DIR, OUTPUT_DIR)
        manifest_packs.append(result)

        print(f"  - 이미지: {result['image_count']}개 (누락: {result['missing_count']}개)")
        print(f"  - ZIP 크기: {result['zip_size_bytes'] / 1024 / 1024:.2f} MB")
        print()

    # Manifest 생성
    manifest = {
        'version': MANIFEST_VERSION,
        'created_at': datetime.now().isoformat(),
        'total_packs': len(manifest_packs),
        'packs': manifest_packs
    }

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 결과 요약
    total_images = sum(p['image_count'] for p in manifest_packs)
    total_size = sum(p['zip_size_bytes'] for p in manifest_packs)

    print("=" * 70)
    print("완료!")
    print("=" * 70)
    print(f"\n결과:")
    print(f"  - 생성된 ZIP: {len(manifest_packs)}개")
    print(f"  - 총 이미지: {total_images}개")
    print(f"  - 총 크기: {total_size / 1024 / 1024:.2f} MB")
    print(f"\n출력 폴더: {OUTPUT_DIR}")
    print(f"Manifest: {MANIFEST_FILE}")


def create_single_zip(category_id):
    """특정 카테고리 ZIP 생성"""
    print(f"카테고리 {category_id} ZIP 생성 중...\n")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    supabase = get_supabase_client()

    # 카테고리 조회
    response = supabase.table("categories").select("*").eq("id", category_id).execute()
    if not response.data:
        print(f"오류: 카테고리 {category_id}를 찾을 수 없습니다.")
        return

    cat = response.data[0]
    title = cat.get('title_ko') or cat['title']
    print(f"카테고리: {title}")

    # 카드 조회
    cards = get_category_cards(supabase, category_id)
    print(f"카드 수: {len(cards)}개")

    # ZIP 생성
    result = create_category_zip(cat, cards, IMAGES_DIR, OUTPUT_DIR)

    print(f"\n결과:")
    print(f"  - 이미지: {result['image_count']}개")
    print(f"  - 누락: {result['missing_count']}개")
    print(f"  - ZIP 크기: {result['zip_size_bytes'] / 1024 / 1024:.2f} MB")
    print(f"  - 파일: {OUTPUT_DIR}/{result['file_name']}")


def main():
    parser = argparse.ArgumentParser(description='카테고리별 이미지 ZIP 생성')
    parser.add_argument('--list', action='store_true', help='카테고리 목록 출력')
    parser.add_argument('--create-all', action='store_true', help='전체 카테고리 ZIP 생성')
    parser.add_argument('--create', type=str, help='특정 카테고리 ZIP 생성 (category_id)')

    args = parser.parse_args()

    if args.list:
        list_categories()
    elif args.create_all:
        create_all_zips()
    elif args.create:
        create_single_zip(args.create)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

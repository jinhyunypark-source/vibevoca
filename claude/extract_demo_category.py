"""
데모 카테고리 이미지 추출 스크립트

작업 내용:
1. 첫 번째 카테고리의 이미지를 assets/word_images_demo/로 복사
2. 앱 번들에 포함될 기본 이미지 세트

실행 방법:
    source backend/venv/bin/activate
    python claude/extract_demo_category.py

작성일: 2026-01-13
"""
import os
import shutil
import json
from dotenv import load_dotenv
from supabase import create_client

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 환경 변수 로드
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# 입력
SOURCE_DIR = os.path.join(PROJECT_ROOT, 'assets', 'word_images')

# 출력
DEMO_DIR = os.path.join(PROJECT_ROOT, 'assets', 'word_images_demo')

# manifest.json도 복사
MANIFEST_SOURCE = os.path.join(SOURCE_DIR, 'manifest.json')
# ============================================


def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY") or os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def get_first_category(supabase):
    """첫 번째 카테고리 조회"""
    response = supabase.table("categories").select("*").order("created_at").limit(1).execute()
    return response.data[0] if response.data else None


def get_category_card_ids(supabase, category_id):
    """카테고리의 모든 카드 ID 조회"""
    # 덱 조회
    decks_response = supabase.table("decks").select("id").eq("category_id", category_id).execute()
    deck_ids = [d['id'] for d in decks_response.data]

    # 카드 조회
    card_ids = []
    for deck_id in deck_ids:
        cards_response = supabase.table("cards").select("id").eq("deck_id", deck_id).execute()
        card_ids.extend([c['id'] for c in cards_response.data])

    return card_ids


def extract_demo_images():
    """데모 카테고리 이미지 추출"""
    print("=" * 60)
    print("데모 카테고리 이미지 추출")
    print("=" * 60 + "\n")

    supabase = get_supabase_client()

    # 첫 번째 카테고리 조회
    category = get_first_category(supabase)
    if not category:
        print("오류: 카테고리를 찾을 수 없습니다.")
        return

    cat_title = category.get('title_ko') or category['title']
    print(f"데모 카테고리: {cat_title}")
    print(f"카테고리 ID: {category['id']}\n")

    # 카드 ID 목록
    card_ids = get_category_card_ids(supabase, category['id'])
    print(f"카드 수: {len(card_ids)}개\n")

    # 출력 폴더 생성 (기존 폴더 삭제)
    if os.path.exists(DEMO_DIR):
        shutil.rmtree(DEMO_DIR)
    os.makedirs(DEMO_DIR)

    # 이미지 복사
    copied = 0
    missing = 0

    for card_id in card_ids:
        src = os.path.join(SOURCE_DIR, f"{card_id}.jpg")
        dst = os.path.join(DEMO_DIR, f"{card_id}.jpg")

        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
        else:
            missing += 1

    # 데모용 manifest 생성
    demo_manifest = {
        'version': '1.0.0',
        'category_id': category['id'],
        'category_title': cat_title,
        'image_count': copied,
        'images': {card_id: {'filename': f'{card_id}.jpg'} for card_id in card_ids if os.path.exists(os.path.join(DEMO_DIR, f'{card_id}.jpg'))}
    }

    manifest_path = os.path.join(DEMO_DIR, 'manifest.json')
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(demo_manifest, f, ensure_ascii=False, indent=2)

    # 결과 출력
    total_size = sum(
        os.path.getsize(os.path.join(DEMO_DIR, f))
        for f in os.listdir(DEMO_DIR) if f.endswith('.jpg')
    )

    print("=" * 60)
    print("완료!")
    print("=" * 60)
    print(f"\n결과:")
    print(f"  - 복사된 이미지: {copied}개")
    print(f"  - 누락된 이미지: {missing}개")
    print(f"  - 총 용량: {total_size / 1024 / 1024:.2f} MB")
    print(f"\n출력 폴더: {DEMO_DIR}")

    # pubspec.yaml 안내
    print("\n" + "-" * 60)
    print("pubspec.yaml 수정 필요:")
    print("-" * 60)
    print("""
flutter:
  assets:
    - assets/word_images_demo/  # 데모 카테고리만 번들
    # - assets/word_images/     # 전체 이미지 제거
""")


if __name__ == "__main__":
    extract_demo_images()

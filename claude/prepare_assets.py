"""
Flutter assets용 이미지 준비 스크립트

작업 내용:
1. output_images_jpg의 이미지를 card_id 기반 파일명으로 복사
2. assets/word_images/ 폴더에 저장
3. 버전 관리용 manifest 파일 생성

파일 구조:
  assets/word_images/
    {card_id}.jpg           # 개별 이미지
    manifest.json           # 버전 및 매핑 정보

실행 방법:
    python claude/prepare_assets.py

작성일: 2026-01-13
"""
import os
import json
import shutil
import hashlib
from datetime import datetime

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 입력
SOURCE_IMAGES_DIR = os.path.join(SCRIPT_DIR, 'output_images_jpg')
MAPPING_FILE = os.path.join(SCRIPT_DIR, 'word_image_mapping.json')

# 출력
ASSETS_DIR = os.path.join(PROJECT_ROOT, 'assets', 'word_images')
MANIFEST_FILE = os.path.join(ASSETS_DIR, 'manifest.json')

# 버전 정보
IMAGE_VERSION = "1.0.0"
# ============================================


def get_file_hash(filepath):
    """파일의 MD5 해시 계산"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_mapping():
    """매핑 파일 로드"""
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['mappings']


def prepare_assets():
    """assets 폴더에 이미지 복사 및 manifest 생성"""
    print("=" * 60)
    print("Flutter Assets 준비 스크립트")
    print("=" * 60 + "\n")

    # 매핑 파일 로드
    print("매핑 파일 로드 중...")
    mappings = load_mapping()
    print(f"총 {len(mappings)}개의 매핑 정보 로드\n")

    # 출력 폴더 생성
    os.makedirs(ASSETS_DIR, exist_ok=True)

    # 이미지 복사 및 manifest 데이터 수집
    manifest_images = {}
    copied_count = 0
    skipped_count = 0
    error_count = 0

    print("이미지 복사 중...")
    for i, mapping in enumerate(mappings, 1):
        card_id = mapping.get('card_id')
        image_file = mapping.get('image_file')  # e.g., "1_1.png"
        word = mapping.get('word')

        # card_id가 없는 경우 건너뛰기
        if not card_id:
            skipped_count += 1
            continue

        # 소스 파일 경로 (JPG)
        source_filename = image_file.replace('.png', '.jpg')
        source_path = os.path.join(SOURCE_IMAGES_DIR, source_filename)

        if not os.path.exists(source_path):
            error_count += 1
            continue

        # 대상 파일 경로 (card_id.jpg)
        dest_filename = f"{card_id}.jpg"
        dest_path = os.path.join(ASSETS_DIR, dest_filename)

        # 파일 복사
        shutil.copy2(source_path, dest_path)
        copied_count += 1

        # manifest 데이터 수집
        file_hash = get_file_hash(dest_path)
        file_size = os.path.getsize(dest_path)

        manifest_images[card_id] = {
            "filename": dest_filename,
            "word": word,
            "hash": file_hash,
            "size": file_size,
            "original_file": image_file
        }

        # 진행 상황 출력
        if i % 200 == 0 or i == len(mappings):
            print(f"  {i}/{len(mappings)} 처리 완료...")

    # Manifest 파일 생성
    print("\nManifest 파일 생성 중...")
    manifest = {
        "version": IMAGE_VERSION,
        "created_at": datetime.now().isoformat(),
        "total_images": len(manifest_images),
        "image_format": "jpg",
        "image_size": "256x256",
        "images": manifest_images
    }

    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # 결과 출력
    total_size = sum(img['size'] for img in manifest_images.values())
    total_size_mb = total_size / (1024 * 1024)

    print("\n" + "=" * 60)
    print("완료!")
    print("=" * 60)
    print(f"\n결과:")
    print(f"  - 복사된 이미지: {copied_count}개")
    print(f"  - 건너뛴 이미지 (card_id 없음): {skipped_count}개")
    print(f"  - 오류: {error_count}개")
    print(f"  - 총 용량: {total_size_mb:.2f} MB")
    print(f"\n출력 폴더: {ASSETS_DIR}")
    print(f"Manifest: {MANIFEST_FILE}")
    print(f"\n버전: {IMAGE_VERSION}")

    # pubspec.yaml 업데이트 안내
    print("\n" + "-" * 60)
    print("pubspec.yaml에 다음을 추가하세요:")
    print("-" * 60)
    print("""
flutter:
  assets:
    - assets/word_images/
""")

    return manifest


if __name__ == "__main__":
    prepare_assets()

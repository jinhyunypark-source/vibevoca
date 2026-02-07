"""
Supabase Storage에 카테고리 ZIP 파일 업로드 스크립트

작업 내용:
1. Supabase Storage bucket 'category-images' 확인/생성
2. category_zips/ 폴더의 ZIP 파일 업로드
3. manifest.json 업로드

실행 방법:
    source backend/venv/bin/activate
    python claude/upload_to_supabase.py --check       # bucket 상태 확인
    python claude/upload_to_supabase.py --upload-all  # 전체 업로드
    python claude/upload_to_supabase.py --upload <id> # 특정 파일만

주의: Private bucket으로 생성됨 (인증 필요)

작성일: 2026-01-13
"""
import os
import sys
import json
import argparse
from dotenv import load_dotenv
from supabase import create_client

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 환경 변수 로드
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))

# 입력 폴더
ZIPS_DIR = os.path.join(SCRIPT_DIR, 'category_zips')
MANIFEST_FILE = os.path.join(ZIPS_DIR, 'manifest.json')

# Supabase Storage 설정
BUCKET_NAME = 'category-images'  # Supabase bucket name (하이픈 사용)
# ============================================


def get_supabase_client():
    """Supabase 클라이언트 생성 (서비스 키 사용)"""
    url = os.environ.get("SUPABASE_URL")
    # Storage 업로드에는 서비스 키 필요 (anon key로는 bucket 생성 불가)
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")


    if not key:
        print("경고: SUPABASE_SERVICE_KEY가 없습니다. anon key로 시도합니다.")
        key = os.environ.get("SUPABASE_ANON_KEY")

    return create_client(url, key)


def check_bucket(supabase):
    """Bucket 상태 확인"""
    print("=" * 60)
    print("Supabase Storage Bucket 상태 확인")
    print("=" * 60 + "\n")

    try:
        # Bucket 목록 조회
        buckets = supabase.storage.list_buckets()
        bucket_names = [b.name for b in buckets]

        print(f"현재 bucket 목록: {bucket_names}")

        if BUCKET_NAME in bucket_names:
            print(f"\n✅ '{BUCKET_NAME}' bucket이 존재합니다.")

            # 파일 목록 조회
            files = supabase.storage.from_(BUCKET_NAME).list()
            print(f"   파일 수: {len(files)}개")

            for f in files[:10]:  # 처음 10개만 출력
                print(f"   - {f['name']}")
            if len(files) > 10:
                print(f"   ... 외 {len(files) - 10}개")
        else:
            print(f"\n❌ '{BUCKET_NAME}' bucket이 없습니다.")
            print("   --create-bucket 옵션으로 생성하세요.")

    except Exception as e:
        print(f"오류: {e}")


def create_bucket(supabase):
    """Bucket 생성 (Private)"""
    print(f"'{BUCKET_NAME}' bucket 생성 중...")

    try:
        # Private bucket 생성
        result = supabase.storage.create_bucket(
            BUCKET_NAME,
            options={
                'public': False,  # Private
                'file_size_limit': 10485760,  # 10MB
                'allowed_mime_types': ['application/zip', 'application/json']
            }
        )
        print(f"✅ Bucket 생성 완료: {result}")
    except Exception as e:
        if 'already exists' in str(e).lower():
            print(f"ℹ️ Bucket이 이미 존재합니다.")
        else:
            print(f"❌ 오류: {e}")


def upload_file(supabase, local_path, remote_path):
    """단일 파일 업로드"""
    with open(local_path, 'rb') as f:
        content = f.read()

    # Content-Type 설정
    content_type = 'application/json' if remote_path.endswith('.json') else 'application/zip'

    try:
        # 기존 파일 삭제 후 업로드 (upsert)
        supabase.storage.from_(BUCKET_NAME).remove([remote_path])
    except:
        pass  # 파일이 없으면 무시

    result = supabase.storage.from_(BUCKET_NAME).upload(
        remote_path,
        content,
        file_options={'content-type': content_type}
    )
    return result


def upload_all(supabase):
    """전체 ZIP 및 manifest 업로드"""
    print("=" * 60)
    print("Supabase Storage 업로드")
    print("=" * 60 + "\n")

    # Manifest 로드
    if not os.path.exists(MANIFEST_FILE):
        print(f"오류: manifest.json이 없습니다. prepare_category_zips.py를 먼저 실행하세요.")
        return

    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    packs = manifest['packs']
    print(f"업로드할 파일: {len(packs)}개 ZIP + manifest.json\n")

    # ZIP 파일 업로드
    for i, pack in enumerate(packs, 1):
        filename = pack['file_name']
        local_path = os.path.join(ZIPS_DIR, filename)

        if not os.path.exists(local_path):
            print(f"[{i}/{len(packs)}] ❌ {filename} - 파일 없음")
            continue

        print(f"[{i}/{len(packs)}] {filename} 업로드 중...", end=' ')
        try:
            upload_file(supabase, local_path, filename)
            size_mb = pack['zip_size_bytes'] / 1024 / 1024
            print(f"✅ ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"❌ {e}")

    # Manifest 업로드
    print(f"\nmanifest.json 업로드 중...", end=' ')
    try:
        upload_file(supabase, MANIFEST_FILE, 'manifest.json')
        print("✅")
    except Exception as e:
        print(f"❌ {e}")

    print("\n" + "=" * 60)
    print("업로드 완료!")
    print("=" * 60)


def upload_single(supabase, category_id):
    """특정 카테고리 ZIP만 업로드"""
    filename = f"{category_id}.zip"
    local_path = os.path.join(ZIPS_DIR, filename)

    if not os.path.exists(local_path):
        print(f"오류: {filename}이 없습니다.")
        return

    print(f"{filename} 업로드 중...", end=' ')
    try:
        upload_file(supabase, local_path, filename)
        size_mb = os.path.getsize(local_path) / 1024 / 1024
        print(f"✅ ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"❌ {e}")


def main():
    parser = argparse.ArgumentParser(description='Supabase Storage 업로드')
    parser.add_argument('--check', action='store_true', help='Bucket 상태 확인')
    parser.add_argument('--create-bucket', action='store_true', help='Bucket 생성')
    parser.add_argument('--upload-all', action='store_true', help='전체 업로드')
    parser.add_argument('--upload', type=str, help='특정 카테고리 ZIP 업로드 (category_id)')

    args = parser.parse_args()

    supabase = get_supabase_client()

    if args.check:
        check_bucket(supabase)
    elif args.create_bucket:
        create_bucket(supabase)
    elif args.upload_all:
        upload_all(supabase)
    elif args.upload:
        upload_single(supabase, args.upload)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

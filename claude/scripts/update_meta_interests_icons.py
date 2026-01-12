#!/usr/bin/env python3
"""
meta_interests 테이블 아이콘 업데이트 스크립트

Material Icons 이름으로 meta_interests 테이블의 icon 필드를 업데이트합니다.
관리자 작업이므로 SUPABASE_SERVICE_ROLE_KEY가 필요합니다.

사용 예시:
    python update_meta_interests_icons.py
    python update_meta_interests_icons.py --check-only
    python update_meta_interests_icons.py --list
"""

import sys
import os
import argparse
from dotenv import load_dotenv

# Load environment variables
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(project_root, '.env'))

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from supabase import create_client


def get_supabase_client():
    """Get Supabase client with admin credentials"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("❌ SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY not found in .env file")

    return create_client(url, key)


# Define correct Material Icons for each interest
ICON_UPDATES = {
    # Hobby interests
    'soccer': 'sports_soccer',
    'football': 'sports_soccer',
    'social': 'groups',
    'travel': 'flight',
    'activity': 'directions_run',
    'career': 'work',
    'learning': 'school',
    'conversation': 'chat',
    'marketing': 'campaign',
    'health': 'favorite',
    'friendship': 'diversity_1',
    'movie': 'movie',
    'technology': 'computer',
    'medical': 'medical_services',
    'food': 'restaurant',

    # Job/Occupation interests
    'student': 'school',
    'developer': 'code',
    'office_worker': 'work',
    'business': 'business_center',
}


def list_interests(client):
    """현재 meta_interests 목록 출력"""
    print("\n📋 현재 meta_interests 목록:")
    print("=" * 80)

    response = client.table('meta_interests').select('*').order('category,order_index').execute()

    current_category = None
    for item in response.data:
        category = item.get('category', 'unknown')
        if category != current_category:
            print(f"\n{category.upper()}:")
            print("-" * 80)
            current_category = category

        code = item.get('code', 'N/A')
        label_ko = item.get('label_ko', 'N/A')
        icon = item.get('icon', 'N/A')
        order = item.get('order_index', 'N/A')
        print(f"  [{order:2}] {code:20} | {label_ko:20} | icon: {icon}")

    print(f"\n총 {len(response.data)}개 항목")


def check_icons(client):
    """아이콘 상태 확인 (업데이트 없이)"""
    print("\n🔍 아이콘 상태 확인:")
    print("=" * 80)

    response = client.table('meta_interests').select('code, label_ko, icon, category').execute()
    existing_codes = {item['code']: item for item in response.data}

    print(f"\n발견된 항목: {len(response.data)}개\n")

    needs_update = []
    missing_codes = []
    ok_count = 0

    for code, expected_icon in ICON_UPDATES.items():
        if code in existing_codes:
            current_icon = existing_codes[code].get('icon')
            label_ko = existing_codes[code].get('label_ko')

            if current_icon != expected_icon:
                needs_update.append((code, label_ko, current_icon, expected_icon))
            else:
                ok_count += 1
        else:
            missing_codes.append(code)

    # 업데이트 필요한 항목
    if needs_update:
        print("⚠️  업데이트 필요:")
        print("-" * 80)
        for code, label_ko, current, expected in needs_update:
            print(f"  {code:20} ({label_ko:15}) | 현재: {current or 'null':20} -> {expected}")
        print()

    # 누락된 항목
    if missing_codes:
        print("❌ 테이블에 없는 항목:")
        print("-" * 80)
        for code in missing_codes:
            print(f"  {code}")
        print()

    # 정상 항목
    print(f"✅ 정상: {ok_count}개")
    print(f"⚠️  업데이트 필요: {len(needs_update)}개")
    print(f"❌ 누락: {len(missing_codes)}개")


def update_icons(client, dry_run=False):
    """아이콘 업데이트 실행"""
    print("\n" + "="*80)
    if dry_run:
        print("🔍 DRY RUN: 아이콘 업데이트 시뮬레이션")
    else:
        print("🚀 meta_interests 아이콘 업데이트 시작")
    print("="*80 + "\n")

    # 기존 interests 확인
    response = client.table('meta_interests').select('code, label_ko, icon, category').execute()
    existing_codes = {item['code']: item for item in response.data}

    print(f"발견된 항목: {len(response.data)}개\n")

    # 업데이트 실행
    updated_count = 0
    skipped_count = 0

    for code, icon in ICON_UPDATES.items():
        if code in existing_codes:
            current_icon = existing_codes[code].get('icon')

            if current_icon == icon:
                skipped_count += 1
                continue

            try:
                if not dry_run:
                    client.table('meta_interests').update({'icon': icon}).eq('code', code).execute()
                print(f"✓ Updated {code:20} -> icon: {icon}")
                updated_count += 1
            except Exception as e:
                print(f"✗ Failed to update {code}: {e}")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}✅ 업데이트: {updated_count}개")
    print(f"{'[DRY RUN] ' if dry_run else ''}⏭️  스킵: {skipped_count}개 (이미 올바른 아이콘)")

    if not dry_run and updated_count > 0:
        print("\n" + "="*80)
        print("업데이트 완료! 최종 결과:")
        print("="*80)
        list_interests(client)


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='meta_interests 테이블 아이콘 업데이트',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예시:
  python update_meta_interests_icons.py              # 아이콘 업데이트 실행
  python update_meta_interests_icons.py --check      # 상태 확인만
  python update_meta_interests_icons.py --list       # 전체 목록 출력
  python update_meta_interests_icons.py --dry-run    # 시뮬레이션
        '''
    )

    parser.add_argument('--check', action='store_true',
                        help='아이콘 상태만 확인 (업데이트 없음)')
    parser.add_argument('--list', action='store_true',
                        help='현재 meta_interests 목록 출력')
    parser.add_argument('--dry-run', action='store_true',
                        help='업데이트 시뮬레이션 (실제 변경 없음)')

    # 인자 없이 실행 시 사용법 출력
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n기본 동작: 아이콘을 업데이트합니다.")
        print("먼저 --check 옵션으로 확인하는 것을 권장합니다.\n")
        sys.exit(0)

    args = parser.parse_args()

    try:
        client = get_supabase_client()

        if args.list:
            list_interests(client)
        elif args.check:
            check_icons(client)
        else:
            update_icons(client, dry_run=args.dry_run)

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
RPC Function을 Supabase에 적용하는 스크립트

실행 방법:
    cd claude
    source venv/bin/activate
    python scripts/apply_rpc_function.py
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.supabase_config import get_supabase_client


def main():
    print("=" * 80)
    print("🔧 Supabase RPC Function 적용")
    print("=" * 80)

    client = get_supabase_client()

    # SQL 파일 읽기
    sql_path = os.path.join(os.path.dirname(__file__), '../../database/vibe_sentences_rpc.sql')

    with open(sql_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    print(f"\n📄 SQL 파일: {sql_path}")
    print(f"   크기: {len(sql)} bytes")

    # Supabase에 적용
    print("\n🚀 RPC Function 적용 중...")

    try:
        # Supabase Python 클라이언트로는 DDL을 직접 실행할 수 없으므로
        # postgrest-py의 제한으로 인해 rpc()나 직접 SQL 실행이 불가능합니다.
        print("\n⚠️  Python 클라이언트로는 CREATE FUNCTION을 실행할 수 없습니다.")
        print("\n✋ 수동 작업 필요:")
        print("   1. Supabase Dashboard → SQL Editor 열기")
        print("   2. 아래 SQL을 복사하여 실행:")
        print("\n" + "=" * 80)
        print(sql)
        print("=" * 80)
        print("\n또는:")
        print("   psql 명령어로 직접 연결하여 실행")

    except Exception as e:
        print(f"\n❌ 에러: {str(e)}")


if __name__ == '__main__':
    main()

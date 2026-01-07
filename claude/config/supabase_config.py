"""
Supabase 연결 설정
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

def get_supabase_client() -> Client:
    """Supabase 클라이언트 반환"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다.")

    return create_client(url, key)


# 테이블 이름 상수
class Tables:
    CATEGORIES = "categories"
    DECKS = "decks"
    CARDS = "cards"
    CONTEXTS = "contexts"
    CARD_EXAMPLES = "card_examples"

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env from parent directory if needed, or current
load_dotenv()

# Singleton pattern for Supabase Client
_client: Client = None

def get_supabase_client() -> Client:
    global _client
    if _client is not None:
        return _client
        
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in environment variables.")

    _client = create_client(url, key)
    return _client

import os
import json
import glob
from supabase import create_client, Client
from dotenv import load_dotenv

# 프로젝트 루트의 .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
    exit(1)

supabase: Client = create_client(url, key)

def fetch_card_map():
    """Fetches all cards and returns a dictionary mapping front_text to card_id."""
    print("Fetching cards from Supabase...")
    # Fetch all cards. Adjust limit if necessary (default is usually 1000).
    # Since we have ~1500 words, we might need pagination or high limit.
    response = supabase.table("cards").select("id, front_text").execute()
    
    # Check if there's more data (simple check, assuming < 10000 for now)
    # Ideally implement pagination if dataset grows.
    
    card_map = {}
    for card in response.data:
        # Normalize to lowercase for matching, assuming uniqueness
        card_map[card['front_text'].strip().lower()] = card['id']
    
    print(f"Loaded {len(card_map)} cards.")
    return card_map

def process_file(filepath, card_map):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        sentences = data.get('sentences', [])
        deck_title = data.get('deck_title', 'Unknown')
        
        records_to_insert = []
        
        for item in sentences:
            word = item.get('word', '').strip()
            if not word:
                continue
                
            # Lookup card_id
            card_id = card_map.get(word.lower())
            
            if not card_id:
                print(f"Warning: Card not found for word '{word}' in deck '{deck_title}'. Skipping.")
                continue
            
            record = {
                "card_id": card_id,
                "word": word,
                "sentence_en": item.get('sentence_en'),
                "sentence_ko": item.get('sentence_ko'),
                "tags": item.get('tags', [])
            }
            records_to_insert.append(record)
            
        if records_to_insert:
            print(f"Inserting {len(records_to_insert)} records for {deck_title}...")
            # Supabase supports batch insert
            data = supabase.table("card_sentences").insert(records_to_insert).execute()
            print("Done.")
        else:
            print("No valid records to insert.")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    card_map = fetch_card_map()
    
    files = glob.glob("claude/deck_output/*.json")
    if not files:
        print("No JSON files found in claude/deck_output/")
        return
        
    for filepath in files:
        process_file(filepath, card_map)

if __name__ == "__main__":
    main()

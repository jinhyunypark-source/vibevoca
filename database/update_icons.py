"""
Update meta_interests icons with correct Material Icons
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# Add parent directory to path to import supabase_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from supabase import create_client

def get_supabase_client():
    """Get Supabase client with proper credentials"""
    url = os.getenv("SUPABASE_URL")
    # Try SERVICE_ROLE_KEY first for admin operations, then ANON_KEY
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY not found in environment")

    return create_client(url, key)

# Define correct icons for each interest
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

    # Job/Occupation interests
    'student': 'school',
    'developer': 'code',
    'office_worker': 'work',
    'business': 'business_center',
}

# New interests to insert if they don't exist
NEW_INTERESTS = [
    {
        'code': 'soccer',
        'label_en': 'Soccer',
        'label_ko': '축구',
        'icon': 'sports_soccer',
        'category': 'hobby',
        'tags': ['soccer', 'sports'],
        'order_index': 21
    },
    {
        'code': 'travel',
        'label_en': 'Travel',
        'label_ko': '여행',
        'icon': 'flight',
        'category': 'hobby',
        'tags': ['travel', 'trip'],
        'order_index': 22
    },
]

def update_icons():
    """Update icons for all interests"""
    client = get_supabase_client()

    print("\n" + "="*80)
    print("Updating meta_interests icons...")
    print("="*80 + "\n")

    # First, check existing interests
    response = client.table('meta_interests').select('code, label_ko, icon, category').execute()
    existing_codes = {item['code'] for item in response.data}

    print(f"Found {len(response.data)} existing interests\n")

    # Update existing interests
    updated_count = 0
    for code, icon in ICON_UPDATES.items():
        if code in existing_codes:
            try:
                result = client.table('meta_interests').update({'icon': icon}).eq('code', code).execute()
                print(f"✓ Updated {code:20} -> icon: {icon}")
                updated_count += 1
            except Exception as e:
                print(f"✗ Failed to update {code}: {e}")
        else:
            print(f"- Skipped {code:20} (not found)")

    print(f"\nUpdated {updated_count} existing interests\n")

    # Insert new interests if they don't exist
    print("Checking for missing interests...\n")
    inserted_count = 0
    for interest in NEW_INTERESTS:
        if interest['code'] not in existing_codes:
            try:
                result = client.table('meta_interests').insert(interest).execute()
                print(f"+ Inserted {interest['code']:20} | {interest['label_ko']}")
                inserted_count += 1
            except Exception as e:
                print(f"✗ Failed to insert {interest['code']}: {e}")
        else:
            print(f"- {interest['code']:20} already exists")

    print(f"\nInserted {inserted_count} new interests\n")

    # Display final results
    print("="*80)
    print("Final Results - Hobby & Job Interests")
    print("="*80 + "\n")

    response = client.table('meta_interests').select('*').in_('category', ['hobby', 'job']).order('category,order_index').execute()

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

    print("\n" + "="*80)
    print("Update completed!")
    print("="*80 + "\n")

if __name__ == "__main__":
    update_icons()

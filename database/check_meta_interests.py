"""
Check current meta_interests table data in Supabase
"""
import sys
import os

# Add parent directory to path to import supabase_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from claude.config.supabase_config import get_supabase_client

def check_meta_interests():
    """Check current meta_interests table data"""
    client = get_supabase_client()

    # Query all meta_interests
    response = client.table('meta_interests').select('*').order('order_index').execute()

    print(f"\n{'='*80}")
    print(f"Total meta_interests: {len(response.data)}")
    print(f"{'='*80}\n")

    # Group by category
    categories = {}
    for item in response.data:
        category = item.get('category', 'unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(item)

    # Display by category
    for category, items in categories.items():
        print(f"\n{category.upper()} ({len(items)} items):")
        print("-" * 80)
        for item in items:
            code = item.get('code', 'N/A')
            label_ko = item.get('label_ko', 'N/A')
            icon = item.get('icon', 'N/A')
            order = item.get('order_index', 'N/A')
            print(f"  [{order:2}] {code:15} | {label_ko:20} | icon: {icon}")

if __name__ == "__main__":
    check_meta_interests()

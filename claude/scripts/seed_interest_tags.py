#!/usr/bin/env python3
"""
Seed Related Tags for meta_interests

기존 meta_interests 테이블의 관심사에 related_tags 데이터를 추가합니다.
generate_sentences_batch.py의 INTEREST_CATEGORIES와 동일한 태그 구조를 사용합니다.

Usage:
    python seed_interest_tags.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client

# ============================================
# Interest → Related Tags Mapping
# ============================================
# meta_interests.code → related_tags 매핑

INTEREST_TAG_MAPPING = {
    "baseball": ["baseball", "sports", "mlb", "kbo"],
    "soccer": ["soccer", "football", "sports", "premier_league"],
    "football": ["soccer", "football", "sports", "premier_league"],  # alias for soccer
    "music": ["music", "concert", "album", "kpop"],
    "kpop": ["music", "concert", "album", "kpop"],  # alias
    "gaming": ["gaming", "esports", "video_game"],
    "esports": ["gaming", "esports", "video_game"],  # alias
    "cooking": ["cooking", "food", "recipe", "chef"],
    "food": ["cooking", "food", "recipe", "chef"],  # alias
    "movies": ["movies", "film", "cinema", "oscar"],
    "film": ["movies", "film", "cinema", "oscar"],  # alias
    "cinema": ["movies", "film", "cinema", "oscar"],  # alias
    "technology": ["technology", "tech", "ai", "startup"],
    "tech": ["technology", "tech", "ai", "startup"],  # alias
    "fitness": ["fitness", "gym", "workout", "health"],
    "gym": ["fitness", "gym", "workout", "health"],  # alias
    "workout": ["fitness", "gym", "workout", "health"],  # alias
    "travel": ["travel", "adventure", "tourism"],
    "adventure": ["travel", "adventure", "tourism"],  # alias
    "reading": ["reading", "books", "literature", "novel"],
    "books": ["reading", "books", "literature", "novel"],  # alias
    "literature": ["reading", "books", "literature", "novel"],  # alias

    # 추가 관심사 (확장 가능)
    "art": ["art", "painting", "gallery", "museum"],
    "photography": ["photography", "camera", "photo", "image"],
    "fashion": ["fashion", "style", "clothing", "trend"],
    "business": ["business", "startup", "entrepreneur", "marketing"],
    "science": ["science", "research", "physics", "chemistry"],
    "nature": ["nature", "environment", "wildlife", "outdoor"],
    "pets": ["pets", "animals", "dog", "cat"],
    "anime": ["anime", "manga", "japanese", "otaku"],
    "kdrama": ["kdrama", "drama", "korean", "tv_show"],
}


class InterestTagSeeder:
    def __init__(self):
        self.client = get_supabase_client()

    def get_all_interests(self):
        """Get all existing meta_interests."""
        result = self.client.table('meta_interests').select('id, code, label_en, label_ko, related_tags').execute()
        return result.data

    def update_related_tags(self, interest_id: str, code: str, tags: list):
        """Update related_tags for a meta_interest."""
        try:
            self.client.table('meta_interests').update({
                'related_tags': tags
            }).eq('id', interest_id).execute()
            return True
        except Exception as e:
            print(f"  ! Error updating {code}: {e}")
            return False

    def seed(self):
        """Seed related_tags for all meta_interests."""
        print("=" * 60)
        print("Seeding Related Tags for meta_interests")
        print("=" * 60)

        interests = self.get_all_interests()
        print(f"\nFound {len(interests)} interests in database\n")

        updated = 0
        skipped = 0
        not_found = 0

        for interest in interests:
            code = interest['code'].lower()
            interest_id = interest['id']
            current_tags = interest.get('related_tags', [])

            if code in INTEREST_TAG_MAPPING:
                tags = INTEREST_TAG_MAPPING[code]

                if current_tags and len(current_tags) > 0:
                    print(f"⏭  {code:20s} - Already has tags: {current_tags}")
                    skipped += 1
                else:
                    if self.update_related_tags(interest_id, code, tags):
                        print(f"✓  {code:20s} → {tags}")
                        updated += 1
            else:
                print(f"⚠  {code:20s} - No mapping found (please add to INTEREST_TAG_MAPPING)")
                not_found += 1

        print("\n" + "=" * 60)
        print(f"Results:")
        print(f"  Updated: {updated}")
        print(f"  Skipped (already has tags): {skipped}")
        print(f"  Not found in mapping: {not_found}")
        print("=" * 60)


def main():
    seeder = InterestTagSeeder()
    seeder.seed()


if __name__ == "__main__":
    main()

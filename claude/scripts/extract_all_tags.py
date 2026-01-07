#!/usr/bin/env python3
"""
태그 목록 추출 프로그램

meta_interests 테이블의 related_tags 컬럼에서 모든 태그 목록을 추출합니다.

Usage:
    python extract_all_tags.py
    python extract_all_tags.py --output tags.json
"""

import sys
import os
import json
import argparse
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


class TagExtractor:
    def __init__(self):
        self.client = get_supabase_client()

    def get_all_tags(self) -> Dict[str, List[str]]:
        """
        meta_interests 테이블에서 모든 태그 목록 추출

        Returns:
            Dict: {
                "baseball": ["baseball", "sports", "mlb", "kbo"],
                "soccer": ["soccer", "football", "sports", "premier_league"],
                ...
            }
        """
        try:
            result = self.client.table('meta_interests').select(
                'id, code, label_en, label_ko, related_tags'
            ).execute()

            tags_by_interest = {}
            all_unique_tags = set()

            for interest in result.data:
                code = interest['code']
                tags = interest.get('related_tags', [])

                if tags:
                    tags_by_interest[code] = tags
                    all_unique_tags.update(tags)

            return {
                "tags_by_interest": tags_by_interest,
                "all_unique_tags": sorted(list(all_unique_tags)),
                "total_interests": len(tags_by_interest),
                "total_unique_tags": len(all_unique_tags)
            }

        except Exception as e:
            print(f"Error extracting tags: {e}")
            return {}

    def save_to_file(self, tags_data: Dict, output_path: str):
        """태그 데이터를 JSON 파일로 저장"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tags_data, f, ensure_ascii=False, indent=2)
            print(f"Saved tags data to {output_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def print_summary(self, tags_data: Dict):
        """태그 데이터 요약 출력"""
        if not tags_data:
            print("No tags found")
            return

        print("\n" + "=" * 60)
        print("Tag Extraction Summary")
        print("=" * 60)
        print(f"Total interests: {tags_data['total_interests']}")
        print(f"Total unique tags: {tags_data['total_unique_tags']}")
        print("\nTags by interest:")

        for interest, tags in tags_data['tags_by_interest'].items():
            print(f"  {interest:20s}: {tags}")

        print("\nAll unique tags:")
        print(f"  {', '.join(tags_data['all_unique_tags'])}")


def main():
    parser = argparse.ArgumentParser(description="Extract all tags from meta_interests table")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()

    extractor = TagExtractor()
    tags_data = extractor.get_all_tags()

    if tags_data:
        extractor.print_summary(tags_data)

        if args.output:
            extractor.save_to_file(tags_data, args.output)

        return tags_data
    else:
        print("Failed to extract tags")
        return {}


if __name__ == "__main__":
    main()

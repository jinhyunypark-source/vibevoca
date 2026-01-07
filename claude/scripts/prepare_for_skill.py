#!/usr/bin/env python3
"""
Skill 실행 준비 스크립트

Step 1, 2를 실행하고 skill이 사용할 파일을 준비한 후,
사용자에게 skill 실행 명령을 안내합니다.

Usage:
    python prepare_for_skill.py --deck-name "Daily Essentials"
"""

import sys
import os
import argparse
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract_words_from_deck import WordExtractor
from extract_all_tags import TagExtractor


class SkillPreparation:
    def __init__(self, deck_name: str):
        self.deck_name = deck_name

        # 출력 디렉토리 설정
        self.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.words_file = os.path.join(self.output_dir, f"words_{timestamp}.json")
        self.tags_file = os.path.join(self.output_dir, f"tags_{timestamp}.json")
        self.sentences_file = os.path.join(self.output_dir, f"sentences_{timestamp}.json")

        # 각 단계별 객체
        self.word_extractor = WordExtractor()
        self.tag_extractor = TagExtractor()

    def print_header(self, title: str):
        """헤더 출력"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def step1_extract_words(self):
        """Step 1: 영어 단어 추출"""
        self.print_header("Step 1: Extract Words from Deck")

        print(f"Deck name: {self.deck_name}")

        words = self.word_extractor.get_words_by_deck_name(self.deck_name)

        if not words:
            raise ValueError(f"No words found for deck: {self.deck_name}")

        print(f"\n✓ Extracted {len(words)} words")

        # 파일로 저장
        self.word_extractor.save_to_file(words, self.words_file)
        print(f"✓ Saved to: {self.words_file}")

        # 미리보기
        print("\nWord preview:")
        for i, word in enumerate(words[:5], 1):
            print(f"  {i}. {word['word']:20s} - {word['meaning']}")
        if len(words) > 5:
            print(f"  ... and {len(words) - 5} more")

        return words

    def step2_extract_tags(self):
        """Step 2: 태그 목록 추출"""
        self.print_header("Step 2: Extract Tags from meta_interests")

        tags_data = self.tag_extractor.get_all_tags()

        if not tags_data:
            raise ValueError("Failed to extract tags")

        print(f"\n✓ Extracted {tags_data['total_interests']} interests")
        print(f"✓ Total unique tags: {tags_data['total_unique_tags']}")

        # 파일로 저장
        self.tag_extractor.save_to_file(tags_data, self.tags_file)
        print(f"✓ Saved to: {self.tags_file}")

        return tags_data

    def print_skill_instructions(self):
        """Skill 실행 안내"""
        self.print_header("Step 3: Run Claude Code Skill")

        print("\n파일 준비가 완료되었습니다!")
        print("\n이제 Claude Code에서 다음 명령을 실행하세요:\n")

        print(f"  /generate-sentences {self.words_file} {self.tags_file} {self.sentences_file}")

        print("\n또는 skill을 대화형으로 실행하려면:\n")
        print("  /generate-sentences")
        print("\n  그리고 다음 파일 경로를 입력하세요:")
        print(f"    Words file: {self.words_file}")
        print(f"    Tags file: {self.tags_file}")
        print(f"    Output file: {self.sentences_file}")

        print("\n" + "=" * 70)
        print("\nSkill 실행 후 Step 4로 진행하려면:")
        print(f"  python upload_sentences_to_db.py --input {self.sentences_file} --skip-duplicates")
        print("=" * 70)

    def run(self):
        """준비 프로세스 실행"""
        self.print_header(f"Sentence Generation - Skill Preparation")
        print(f"Deck: {self.deck_name}")

        try:
            # Step 1: 단어 추출
            words = self.step1_extract_words()

            # Step 2: 태그 추출
            tags_data = self.step2_extract_tags()

            # Skill 실행 안내
            self.print_skill_instructions()

            return {
                "words_file": self.words_file,
                "tags_file": self.tags_file,
                "sentences_file": self.sentences_file,
                "word_count": len(words)
            }

        except Exception as e:
            self.print_header("ERROR")
            print(f"Failed: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Prepare files for generate-sentences skill"
    )
    parser.add_argument("--deck-name", required=True, help="Name of the deck to process")

    args = parser.parse_args()

    # 준비 실행
    prep = SkillPreparation(deck_name=args.deck_name)
    result = prep.run()

    print(f"\n✓ Ready for skill execution")
    print(f"  Words: {result['word_count']}")
    print(f"  Files prepared in: {os.path.dirname(result['words_file'])}")


if __name__ == "__main__":
    main()

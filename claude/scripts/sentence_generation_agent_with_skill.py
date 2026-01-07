#!/usr/bin/env python3
"""
예문 생성 통합 에이전트 (Claude Code Skill 버전)

사용자가 deck 이름을 입력하면 다음 과정을 수행합니다:
1. 영어 단어 추출 (Python)
2. 태그 목록 추출 (Python)
3. 예문 생성 (Claude Code Skill) ← API 키 불필요!
4. DB 반영 (Python)

Usage:
    # Step 1-2 실행 및 skill 준비
    python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials" --prepare

    # Step 3: Claude Code에서 skill 실행
    /generate-sentences <words_file> <tags_file> <sentences_file>

    # Step 4: DB 업로드
    python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials" --upload <sentences_file>

    # 또는 대화형으로 전체 프로세스 안내
    python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials"
"""

import sys
import os
import argparse
import time
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract_words_from_deck import WordExtractor
from extract_all_tags import TagExtractor
from upload_sentences_to_db import SentenceUploader


class SentenceGenerationAgentWithSkill:
    def __init__(self, deck_name: str):
        self.deck_name = deck_name

        # 출력 디렉토리
        self.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.words_file = os.path.join(self.output_dir, f"words_{timestamp}.json")
        self.tags_file = os.path.join(self.output_dir, f"tags_{timestamp}.json")
        self.sentences_file = os.path.join(self.output_dir, f"sentences_{timestamp}.json")

        # 객체 초기화
        self.word_extractor = WordExtractor()
        self.tag_extractor = TagExtractor()
        self.sentence_uploader = SentenceUploader()

    def print_header(self, title: str, width: int = 70):
        """헤더 출력"""
        print("\n" + "=" * width)
        print(f"  {title}")
        print("=" * width)

    def print_box(self, lines: list, width: int = 70):
        """박스 형태로 메시지 출력"""
        print("\n" + "┌" + "─" * (width - 2) + "┐")
        for line in lines:
            padding = width - len(line) - 4
            print(f"│ {line}{' ' * padding} │")
        print("└" + "─" * (width - 2) + "┘")

    def prepare_files(self):
        """Step 1-2: 파일 준비"""
        self.print_header("Step 1-2: Prepare Files")

        # Step 1: 단어 추출
        print(f"\n[Step 1] Extracting words from deck: {self.deck_name}")
        words = self.word_extractor.get_words_by_deck_name(self.deck_name)

        if not words:
            raise ValueError(f"No words found for deck: {self.deck_name}")

        self.word_extractor.save_to_file(words, self.words_file)
        print(f"  ✓ Extracted {len(words)} words → {self.words_file}")

        # Step 2: 태그 추출
        print(f"\n[Step 2] Extracting tags from meta_interests")
        tags_data = self.tag_extractor.get_all_tags()

        if not tags_data:
            raise ValueError("Failed to extract tags")

        self.tag_extractor.save_to_file(tags_data, self.tags_file)
        print(f"  ✓ Extracted {tags_data['total_interests']} interests → {self.tags_file}")

        return len(words)

    def show_skill_instructions(self):
        """Step 3: Skill 실행 안내"""
        self.print_header("Step 3: Generate Sentences with Claude Code Skill")

        instructions = [
            "",
            "🤖 이제 Claude Code Skill을 실행하세요!",
            "",
            "다음 명령을 Claude Code에서 실행:",
            "",
            f"/generate-sentences {self.words_file} {self.tags_file} {self.sentences_file}",
            "",
            "또는 대화형으로:",
            "",
            "/generate-sentences",
            "",
            "그리고 파일 경로를 입력하세요.",
            ""
        ]

        self.print_box(instructions, width=70)

        print("\n💡 Skill이 완료되면 다음 명령으로 Step 4를 실행하세요:")
        print(f"\n  python {os.path.basename(__file__)} --deck-name \"{self.deck_name}\" --upload {self.sentences_file}")

    def upload_sentences(self, sentences_file: str, skip_duplicates: bool = True):
        """Step 4: DB 업로드"""
        self.print_header("Step 4: Upload to Database")

        # 파일 존재 확인
        if not os.path.exists(sentences_file):
            raise FileNotFoundError(f"Sentences file not found: {sentences_file}")

        # 파일 로드
        sentences = self.sentence_uploader.load_sentences_from_file(sentences_file)

        if not sentences:
            raise ValueError("No sentences found in file")

        print(f"\n✓ Loaded {len(sentences)} sentences from {sentences_file}")

        # 사용자 확인
        print(f"\n⚠️  This will upload {len(sentences)} sentences to the database.")
        print(f"   Skip duplicates: {skip_duplicates}")
        print("\n   Continue? (y/n): ", end="")
        response = input().strip().lower()

        if response != 'y':
            print("\nCancelled by user")
            return False

        # 업로드
        self.sentence_uploader.upload_all(sentences, skip_duplicates=skip_duplicates)

        print("\n✓ Upload completed!")
        return True

    def run_interactive(self):
        """대화형 전체 프로세스"""
        self.print_header(f"Sentence Generation Agent (Claude Code Skill)")
        print(f"\nDeck: {self.deck_name}")
        print("\n이 에이전트는 3단계로 진행됩니다:")
        print("  1-2. 파일 준비 (Python)")
        print("  3.   예문 생성 (Claude Code Skill)")
        print("  4.   DB 업로드 (Python)")

        start_time = time.time()

        try:
            # Step 1-2: 파일 준비
            word_count = self.prepare_files()

            # Step 3: Skill 실행 안내
            self.show_skill_instructions()

            # 완료 대기
            print("\n" + "=" * 70)
            print("\n⏸️  Waiting for skill execution...")
            print("\nSkill을 실행한 후 'done'을 입력하세요 (또는 'skip'으로 나중에): ", end="")
            response = input().strip().lower()

            if response == 'skip':
                print("\n✓ Step 1-2 완료. Skill 실행 후 Step 4를 직접 실행하세요.")
                return

            if response != 'done':
                print("\nCancelled")
                return

            # Step 4: 업로드
            if os.path.exists(self.sentences_file):
                self.upload_sentences(self.sentences_file, skip_duplicates=True)

                # 최종 보고
                elapsed = time.time() - start_time
                self.print_header("SUCCESS")
                print(f"\nDeck: {self.deck_name}")
                print(f"Words: {word_count}")
                print(f"Total time: {elapsed / 60:.1f} minutes")
                print("\n" + "=" * 70)
            else:
                print(f"\n⚠️  Sentences file not found: {self.sentences_file}")
                print("Skill을 먼저 실행하세요.")

        except Exception as e:
            self.print_header("ERROR")
            print(f"\nFailed: {e}")
            raise


def main():
    parser = argparse.ArgumentParser(
        description="Sentence Generation Agent with Claude Code Skill"
    )
    parser.add_argument("--deck-name", required=True, help="Name of the deck")
    parser.add_argument("--prepare", action="store_true", help="Only run Step 1-2 (prepare files)")
    parser.add_argument("--upload", help="Only run Step 4 (upload sentences from file)")
    parser.add_argument("--skip-duplicates", action="store_true", default=True, help="Skip duplicate sentences")

    args = parser.parse_args()

    agent = SentenceGenerationAgentWithSkill(deck_name=args.deck_name)

    if args.prepare:
        # Step 1-2만 실행
        agent.prepare_files()
        agent.show_skill_instructions()

    elif args.upload:
        # Step 4만 실행
        agent.upload_sentences(args.upload, skip_duplicates=args.skip_duplicates)

    else:
        # 대화형 전체 프로세스
        agent.run_interactive()


if __name__ == "__main__":
    main()

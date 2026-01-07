#!/usr/bin/env python3
"""
예문 생성 통합 에이전트

사용자가 deck 이름을 입력하면 다음 과정을 자동으로 수행합니다:
1. 영어 단어 추출 (deck 이름 → front_text 리스트)
2. 태그 목록 추출 (meta_interests 테이블)
3. 예문 생성 및 저장 (LLM 활용)
4. DB 반영 (card_sentences 테이블 업로드)

Usage:
    python sentence_generation_agent.py --deck-name "Daily Essentials"
    python sentence_generation_agent.py --deck-name "Business English" --skip-duplicates
    python sentence_generation_agent.py --deck-name "Travel Phrases" --keep-files
"""

import sys
import os
import json
import argparse
import time
from datetime import datetime
from typing import List, Dict, Optional

# 다른 스크립트들을 임포트
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract_words_from_deck import WordExtractor
from extract_all_tags import TagExtractor
from generate_sentences_with_llm import LLMSentenceGenerator
from upload_sentences_to_db import SentenceUploader


class SentenceGenerationAgent:
    def __init__(self, deck_name: str, api_key: Optional[str] = None, keep_files: bool = False):
        self.deck_name = deck_name
        self.api_key = api_key
        self.keep_files = keep_files

        # 임시 파일 경로 설정
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "output"
        )
        os.makedirs(self.output_dir, exist_ok=True)

        self.words_file = os.path.join(self.output_dir, f"words_{timestamp}.json")
        self.tags_file = os.path.join(self.output_dir, f"tags_{timestamp}.json")
        self.sentences_file = os.path.join(self.output_dir, f"sentences_{timestamp}.json")

        # 각 단계별 객체 초기화
        self.word_extractor = WordExtractor()
        self.tag_extractor = TagExtractor()
        self.sentence_generator = LLMSentenceGenerator(api_key=api_key)
        self.sentence_uploader = SentenceUploader()

    def print_header(self, title: str):
        """헤더 출력"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70)

    def step1_extract_words(self) -> List[Dict]:
        """1단계: 영어 단어 추출"""
        self.print_header("Step 1: Extract Words from Deck")

        print(f"Deck name: {self.deck_name}")

        words = self.word_extractor.get_words_by_deck_name(self.deck_name)

        if not words:
            raise ValueError(f"No words found for deck: {self.deck_name}")

        print(f"\n✓ Extracted {len(words)} words")

        # 파일로 저장
        self.word_extractor.save_to_file(words, self.words_file)
        print(f"✓ Saved to: {self.words_file}")

        # 단어 목록 미리보기
        print("\nWord preview:")
        for i, word in enumerate(words[:5], 1):
            print(f"  {i}. {word['word']:20s} - {word['meaning']}")
        if len(words) > 5:
            print(f"  ... and {len(words) - 5} more")

        return words

    def step2_extract_tags(self) -> Dict:
        """2단계: 태그 목록 추출"""
        self.print_header("Step 2: Extract Tags from meta_interests")

        tags_data = self.tag_extractor.get_all_tags()

        if not tags_data:
            raise ValueError("Failed to extract tags")

        print(f"\n✓ Extracted {tags_data['total_interests']} interests")
        print(f"✓ Total unique tags: {tags_data['total_unique_tags']}")

        # 파일로 저장
        self.tag_extractor.save_to_file(tags_data, self.tags_file)
        print(f"✓ Saved to: {self.tags_file}")

        # 태그 미리보기
        print("\nInterest preview:")
        for i, (interest, tags) in enumerate(list(tags_data['tags_by_interest'].items())[:5], 1):
            print(f"  {i}. {interest:15s}: {', '.join(tags[:3])}...")
        if len(tags_data['tags_by_interest']) > 5:
            print(f"  ... and {len(tags_data['tags_by_interest']) - 5} more")

        return tags_data

    def step3_generate_sentences(self, words: List[Dict], tags_data: Dict) -> List[Dict]:
        """3단계: 예문 생성 및 저장"""
        self.print_header("Step 3: Generate Sentences with LLM")

        print(f"Words to process: {len(words)}")
        print(f"Using model: Claude 3.5 Sonnet")

        # 예상 시간 계산
        estimated_time = len(words) * 5  # 단어당 약 5초
        print(f"Estimated time: ~{estimated_time // 60} minutes")

        # 사용자 확인
        print("\n⚠️  This will consume API credits. Continue? (y/n): ", end="")
        response = input().strip().lower()

        if response != 'y':
            print("Cancelled by user")
            raise ValueError("User cancelled sentence generation")

        # 예문 생성
        start_time = time.time()

        sentences = self.sentence_generator.generate_for_all_words(
            words,
            tags_data,
            self.sentences_file
        )

        elapsed_time = time.time() - start_time

        print(f"\n✓ Generated {len(sentences)} sentences")
        print(f"✓ Time taken: {elapsed_time:.1f} seconds ({elapsed_time / 60:.1f} minutes)")
        print(f"✓ Saved to: {self.sentences_file}")

        # 예문 미리보기
        print("\nSentence preview:")
        for i, sentence in enumerate(sentences[:3], 1):
            print(f"  {i}. [{sentence['word']}] {sentence['sentence_en'][:50]}...")
            print(f"     Tags: {', '.join(sentence.get('tags', []))}")

        return sentences

    def step4_upload_to_db(self, sentences: List[Dict], skip_duplicates: bool = False):
        """4단계: DB 반영"""
        self.print_header("Step 4: Upload to card_sentences Table")

        print(f"Sentences to upload: {len(sentences)}")
        print(f"Skip duplicates: {skip_duplicates}")

        # 사용자 확인
        print("\n⚠️  This will modify the database. Continue? (y/n): ", end="")
        response = input().strip().lower()

        if response != 'y':
            print("Cancelled by user")
            raise ValueError("User cancelled DB upload")

        # DB 업로드
        self.sentence_uploader.upload_all(sentences, skip_duplicates=skip_duplicates)

        print("\n✓ Upload completed")

    def cleanup_files(self):
        """임시 파일 정리"""
        if not self.keep_files:
            self.print_header("Cleanup")
            files_to_remove = [self.words_file, self.tags_file, self.sentences_file]

            for file_path in files_to_remove:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"✓ Removed: {file_path}")
                except Exception as e:
                    print(f"! Failed to remove {file_path}: {e}")

    def run(self, skip_duplicates: bool = False):
        """전체 프로세스 실행"""
        print("\n" + "=" * 70)
        print("  Sentence Generation Agent")
        print("  Deck: " + self.deck_name)
        print("=" * 70)

        start_time = time.time()

        try:
            # Step 1: 영어 단어 추출
            words = self.step1_extract_words()

            # Step 2: 태그 목록 추출
            tags_data = self.step2_extract_tags()

            # Step 3: 예문 생성 및 저장
            sentences = self.step3_generate_sentences(words, tags_data)

            # Step 4: DB 반영
            self.step4_upload_to_db(sentences, skip_duplicates=skip_duplicates)

            # 성공 메시지
            elapsed_time = time.time() - start_time
            self.print_header("SUCCESS")
            print(f"Deck: {self.deck_name}")
            print(f"Words processed: {len(words)}")
            print(f"Sentences generated: {len(sentences)}")
            print(f"Total time: {elapsed_time / 60:.1f} minutes")
            print("=" * 70)

        except Exception as e:
            self.print_header("ERROR")
            print(f"Failed to complete: {e}")
            print("=" * 70)
            raise

        finally:
            # 파일 정리
            if not self.keep_files:
                self.cleanup_files()
            else:
                print(f"\nFiles kept in: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Sentence Generation Agent - Complete workflow for generating and uploading example sentences"
    )
    parser.add_argument("--deck-name", required=True, help="Name of the deck to process")
    parser.add_argument("--api-key", help="Anthropic API key (or use ANTHROPIC_API_KEY env var)")
    parser.add_argument("--skip-duplicates", action="store_true", help="Skip duplicate sentences when uploading")
    parser.add_argument("--keep-files", action="store_true", help="Keep intermediate JSON files after completion")

    args = parser.parse_args()

    # 에이전트 실행
    agent = SentenceGenerationAgent(
        deck_name=args.deck_name,
        api_key=args.api_key,
        keep_files=args.keep_files
    )

    agent.run(skip_duplicates=args.skip_duplicates)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
card_sentences 테이블 업로드 프로그램

생성된 예문 JSON 파일을 읽어서 card_sentences 테이블에 업로드합니다.

Usage:
    python upload_sentences_to_db.py --input sentences.json
    python upload_sentences_to_db.py --input sentences.json --skip-duplicates
"""

import sys
import os
import json
import argparse
from typing import List, Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.supabase_config import get_supabase_client


class SentenceUploader:
    def __init__(self):
        self.client = get_supabase_client()

    def check_duplicate(self, card_id: str, sentence_en: str) -> bool:
        """중복 예문 체크"""
        try:
            result = self.client.table('card_sentences').select('id').eq(
                'card_id', card_id
            ).eq(
                'sentence_en', sentence_en
            ).execute()

            return len(result.data) > 0

        except Exception as e:
            print(f"  ! Error checking duplicate: {e}")
            return False

    def upload_sentence(self, sentence: Dict, skip_duplicates: bool = False):
        """
        단일 예문 업로드

        Returns:
            True: Successfully uploaded
            None: Skipped (duplicate)
            False: Failed
        """
        try:
            # 중복 체크
            if skip_duplicates and self.check_duplicate(sentence['card_id'], sentence['sentence_en']):
                print(f"  ⏭  Skipped duplicate: {sentence['sentence_en'][:50]}...")
                return None  # None indicates skipped

            # 업로드할 데이터 구성
            data = {
                "card_id": sentence['card_id'],
                "word": sentence['word'],
                "sentence_en": sentence['sentence_en'],
                "sentence_ko": sentence['sentence_ko'],
                "tags": sentence.get('tags', []),
                "is_default": False,  # LLM 생성 예문은 기본값 아님
                "is_verified": False,  # 검수 필요
                "source": "llm_claude"
            }

            # DB 삽입
            self.client.table('card_sentences').insert(data).execute()
            return True

        except Exception as e:
            print(f"  ! Error uploading sentence: {e}")
            return False

    def upload_all(self, sentences: List[Dict], skip_duplicates: bool = False):
        """모든 예문 업로드"""
        print("\n" + "=" * 60)
        print("Uploading Sentences to card_sentences Table")
        print("=" * 60)
        print(f"Total sentences to upload: {len(sentences)}")

        uploaded = 0
        skipped = 0
        failed = 0

        for i, sentence in enumerate(sentences, 1):
            word = sentence.get('word', 'unknown')
            print(f"\n[{i}/{len(sentences)}] {word}: ", end="")

            result = self.upload_sentence(sentence, skip_duplicates)

            if result:
                print("✓ Uploaded")
                uploaded += 1
            elif skip_duplicates and self.check_duplicate(sentence['card_id'], sentence['sentence_en']):
                skipped += 1
            else:
                print("✗ Failed")
                failed += 1

            # 진행 상황 출력
            if i % 10 == 0:
                print(f"\n  → Progress: {uploaded} uploaded, {skipped} skipped, {failed} failed")

        print("\n" + "=" * 60)
        print("Upload Summary:")
        print(f"  Uploaded: {uploaded}")
        print(f"  Skipped (duplicates): {skipped}")
        print(f"  Failed: {failed}")
        print(f"  Total: {len(sentences)}")
        print("=" * 60)

    def load_sentences_from_file(self, file_path: str) -> List[Dict]:
        """JSON 파일에서 예문 로드"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sentences = json.load(f)
            print(f"Loaded {len(sentences)} sentences from {file_path}")
            return sentences
        except Exception as e:
            print(f"Error loading file: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Upload sentences to card_sentences table")
    parser.add_argument("--input", required=True, help="Input sentences JSON file")
    parser.add_argument("--skip-duplicates", action="store_true", help="Skip duplicate sentences")

    args = parser.parse_args()

    uploader = SentenceUploader()

    # 파일에서 예문 로드
    sentences = uploader.load_sentences_from_file(args.input)

    if not sentences:
        print("No sentences to upload")
        return

    # DB에 업로드
    uploader.upload_all(sentences, skip_duplicates=args.skip_duplicates)


if __name__ == "__main__":
    main()

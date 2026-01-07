#!/usr/bin/env python3
"""
Batch process all decks - generates sentences for all decks with progress tracking
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.append('/Users/jin/dev/vibevoca/claude/config')
from supabase_config import get_supabase_client

# Import existing modules
from extract_words_from_deck import WordExtractor
from extract_all_tags import TagExtractor
from upload_sentences_to_db import SentenceUploader

class ProgressTracker:
    """Tracks progress of deck processing"""

    def __init__(self, progress_file='output/batch_progress.json'):
        self.progress_file = progress_file
        self.progress = self.load_progress()

    def load_progress(self):
        """Load existing progress or create new"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'started_at': datetime.now().isoformat(),
            'completed_decks': [],
            'failed_decks': [],
            'current_deck': None,
            'total_decks': 0,
            'total_words_processed': 0,
            'total_sentences_generated': 0,
            'last_updated': None
        }

    def save_progress(self):
        """Save current progress"""
        self.progress['last_updated'] = datetime.now().isoformat()
        os.makedirs(os.path.dirname(self.progress_file), exist_ok=True)
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2, ensure_ascii=False)

    def start_deck(self, deck_name):
        """Mark deck as started"""
        self.progress['current_deck'] = deck_name
        self.save_progress()

    def complete_deck(self, deck_name, words_count, sentences_count):
        """Mark deck as completed"""
        self.progress['completed_decks'].append({
            'deck_name': deck_name,
            'completed_at': datetime.now().isoformat(),
            'words_count': words_count,
            'sentences_count': sentences_count
        })
        self.progress['current_deck'] = None
        self.progress['total_words_processed'] += words_count
        self.progress['total_sentences_generated'] += sentences_count
        self.save_progress()

    def fail_deck(self, deck_name, error):
        """Mark deck as failed"""
        self.progress['failed_decks'].append({
            'deck_name': deck_name,
            'failed_at': datetime.now().isoformat(),
            'error': str(error)
        })
        self.progress['current_deck'] = None
        self.save_progress()

    def is_completed(self, deck_name):
        """Check if deck is already completed"""
        return any(d['deck_name'] == deck_name for d in self.progress['completed_decks'])

    def get_summary(self):
        """Get progress summary"""
        completed = len(self.progress['completed_decks'])
        failed = len(self.progress['failed_decks'])
        total = self.progress['total_decks']
        remaining = total - completed - failed

        return f"""
Progress Summary:
==================
Total Decks: {total}
Completed: {completed}
Failed: {failed}
Remaining: {remaining}
Current: {self.progress['current_deck'] or 'None'}

Total Words Processed: {self.progress['total_words_processed']}
Total Sentences Generated: {self.progress['total_sentences_generated']}

Started: {self.progress['started_at']}
Last Updated: {self.progress['last_updated'] or 'Never'}
"""


class BatchDeckProcessor:
    """Process all decks automatically"""

    def __init__(self, sentences_per_word=10, skip_completed_decks=None):
        self.client = get_supabase_client()
        self.word_extractor = WordExtractor()
        self.tag_extractor = TagExtractor()
        self.uploader = SentenceUploader()
        self.tracker = ProgressTracker()
        self.sentences_per_word = sentences_per_word
        self.skip_decks = skip_completed_decks or ['TASTE', 'LOGIC_CLARITY']

        # Create output directory
        os.makedirs('output', exist_ok=True)

    def get_all_decks(self):
        """Get all deck names"""
        result = self.client.table('decks').select('title').order('title').execute()
        return [deck['title'] for deck in result.data]

    def process_single_deck(self, deck_name):
        """Process a single deck completely"""
        print(f"\n{'='*60}")
        print(f"Processing Deck: {deck_name}")
        print(f"{'='*60}\n")

        self.tracker.start_deck(deck_name)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        try:
            # Step 1: Extract words
            print(f"[1/4] Extracting words from {deck_name}...")
            words = self.word_extractor.get_words_by_deck_name(deck_name)
            if not words:
                print(f"  ⚠ No words found in {deck_name}, skipping.")
                return 0, 0

            words_file = f"output/words_{deck_name}_{timestamp}.json"
            with open(words_file, 'w', encoding='utf-8') as f:
                json.dump(words, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Extracted {len(words)} words → {words_file}")

            # Step 2: Extract tags (use cached if exists)
            print(f"[2/4] Extracting tags...")
            tags_file = f"output/tags_{deck_name}_{timestamp}.json"
            tags_data = self.tag_extractor.get_all_tags()
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(tags_data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Extracted {len(tags_data['all_unique_tags'])} tags → {tags_file}")

            # Step 3: Prepare for manual sentence generation
            print(f"\n[3/4] Ready for sentence generation")
            print(f"  Input files prepared:")
            print(f"    - Words: {words_file}")
            print(f"    - Tags: {tags_file}")
            print(f"  Expected output: output/sentences_{deck_name}_{timestamp}.json")
            print(f"  Total words: {len(words)}")
            print(f"  Sentences needed: {len(words) * self.sentences_per_word}")

            return None, None  # Indicates manual step needed

        except Exception as e:
            print(f"  ✗ Error processing {deck_name}: {e}")
            self.tracker.fail_deck(deck_name, e)
            return None, None

    def upload_sentences_for_deck(self, deck_name, timestamp):
        """Upload generated sentences for a deck"""
        sentences_file = f"output/sentences_{deck_name}_{timestamp}.json"

        if not os.path.exists(sentences_file):
            print(f"  ✗ Sentences file not found: {sentences_file}")
            return False

        print(f"[4/4] Uploading sentences to database...")
        with open(sentences_file, 'r', encoding='utf-8') as f:
            sentences = json.load(f)

        if not sentences:
            print(f"  ⚠ No sentences to upload")
            return False

        uploaded = 0
        skipped = 0
        failed = 0

        for sentence in sentences:
            success = self.uploader.upload_sentence(sentence, skip_duplicates=True)
            if success is None:
                skipped += 1
            elif success:
                uploaded += 1
            else:
                failed += 1

        print(f"\n  Upload Summary:")
        print(f"    Uploaded: {uploaded}")
        print(f"    Skipped (duplicates): {skipped}")
        print(f"    Failed: {failed}")

        if failed == 0:
            # Get words count from file
            words_file = f"output/words_{deck_name}_{timestamp}.json"
            with open(words_file, 'r', encoding='utf-8') as f:
                words = json.load(f)

            self.tracker.complete_deck(deck_name, len(words), len(sentences))
            print(f"  ✓ Deck {deck_name} completed successfully!")
            return True
        else:
            self.tracker.fail_deck(deck_name, f"{failed} sentences failed to upload")
            return False

    def run_batch_preparation(self):
        """Prepare files for all remaining decks"""
        all_decks = self.get_all_decks()
        self.tracker.progress['total_decks'] = len(all_decks)
        self.tracker.save_progress()

        print(f"\n{'='*60}")
        print(f"BATCH DECK PROCESSING")
        print(f"{'='*60}")
        print(f"Total decks to process: {len(all_decks)}")
        print(f"Skipping already completed: {', '.join(self.skip_decks)}")
        print(f"{'='*60}\n")

        prepared_decks = []

        for deck_name in all_decks:
            # Skip if already completed
            if deck_name in self.skip_decks or self.tracker.is_completed(deck_name):
                print(f"⊘ Skipping {deck_name} (already completed)")
                continue

            words_count, sentences_count = self.process_single_deck(deck_name)

            if words_count is None:
                # Manual step needed
                prepared_decks.append(deck_name)

        print(f"\n{'='*60}")
        print(f"PREPARATION COMPLETE")
        print(f"{'='*60}")
        print(f"Prepared {len(prepared_decks)} decks for sentence generation")
        print(f"\nNext: Generate sentences for prepared decks and run upload step")
        print(f"{'='*60}\n")

        print(self.tracker.get_summary())

        return prepared_decks


def main():
    """Main entry point"""
    processor = BatchDeckProcessor(sentences_per_word=10)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'prepare':
            # Prepare all decks
            processor.run_batch_preparation()

        elif command == 'upload':
            # Upload for a specific deck
            if len(sys.argv) < 4:
                print("Usage: python batch_process_all_decks.py upload <deck_name> <timestamp>")
                sys.exit(1)
            deck_name = sys.argv[2]
            timestamp = sys.argv[3]
            processor.upload_sentences_for_deck(deck_name, timestamp)

        elif command == 'status':
            # Show progress status
            print(processor.tracker.get_summary())

        else:
            print(f"Unknown command: {command}")
            print("Available commands: prepare, upload, status")

    else:
        print("Usage:")
        print("  python batch_process_all_decks.py prepare     # Prepare all decks")
        print("  python batch_process_all_decks.py upload <deck_name> <timestamp>")
        print("  python batch_process_all_decks.py status      # Show progress")


if __name__ == '__main__':
    main()

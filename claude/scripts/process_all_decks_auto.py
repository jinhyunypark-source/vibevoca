#!/usr/bin/env python3
"""
Fully automated deck processing - runs completely unattended
"""
import json
import sys
import os
from datetime import datetime

sys.path.append('/Users/jin/dev/vibevoca/claude/config')
from supabase_config import get_supabase_client

from extract_words_from_deck import WordExtractor
from extract_all_tags import TagExtractor
from generate_sentences_automated import AutomatedSentenceGenerator
from upload_sentences_to_db import SentenceUploader


class ProgressTracker:
    """Tracks progress of deck processing with resume capability"""

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

        summary = f"""
{'='*60}
PROGRESS SUMMARY
{'='*60}
Total Decks: {total}
Completed: {completed}
Failed: {failed}
Remaining: {remaining}
Current: {self.progress['current_deck'] or 'None'}

Total Words Processed: {self.progress['total_words_processed']}
Total Sentences Generated: {self.progress['total_sentences_generated']}

Started: {self.progress['started_at']}
Last Updated: {self.progress['last_updated'] or 'Never'}
{'='*60}
"""
        return summary


class FullyAutomatedProcessor:
    """Process all decks completely automatically"""

    def __init__(self, sentences_per_word=10, resume=True):
        self.client = get_supabase_client()
        self.word_extractor = WordExtractor()
        self.tag_extractor = TagExtractor()
        self.sentence_generator = AutomatedSentenceGenerator()
        self.uploader = SentenceUploader()
        self.tracker = ProgressTracker()
        self.sentences_per_word = sentences_per_word
        self.resume = resume

        # Create output directory
        os.makedirs('output', exist_ok=True)

    def get_all_decks(self):
        """Get all deck names"""
        result = self.client.table('decks').select('title').order('title').execute()
        return [deck['title'] for deck in result.data]

    def process_single_deck(self, deck_name):
        """Process a single deck completely - all steps automated"""
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
                self.tracker.complete_deck(deck_name, 0, 0)
                return True

            words_file = f"output/words_{deck_name}_{timestamp}.json"
            with open(words_file, 'w', encoding='utf-8') as f:
                json.dump(words, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Extracted {len(words)} words")

            # Step 2: Extract tags
            print(f"\n[2/4] Extracting tags...")
            tags_data = self.tag_extractor.get_all_tags()
            tags_file = f"output/tags_{deck_name}_{timestamp}.json"
            with open(tags_file, 'w', encoding='utf-8') as f:
                json.dump(tags_data, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Extracted {len(tags_data['all_unique_tags'])} tags")

            # Step 3: Generate sentences (AUTOMATED)
            print(f"\n[3/4] Generating sentences (automated)...")
            sentences = self.sentence_generator.generate_for_deck(
                words,
                tags_data,
                self.sentences_per_word
            )

            sentences_file = f"output/sentences_{deck_name}_{timestamp}.json"
            with open(sentences_file, 'w', encoding='utf-8') as f:
                json.dump(sentences, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Generated {len(sentences)} sentences → {sentences_file}")

            # Step 4: Upload to database
            print(f"\n[4/4] Uploading to database...")
            uploaded = 0
            skipped = 0
            failed = 0

            for idx, sentence in enumerate(sentences, 1):
                success = self.uploader.upload_sentence(sentence, skip_duplicates=True)
                if success is None:
                    skipped += 1
                elif success:
                    uploaded += 1
                else:
                    failed += 1

                if idx % 20 == 0:
                    print(f"  Progress: {idx}/{len(sentences)} ({uploaded} uploaded, {skipped} skipped)")

            print(f"\n  Upload Summary:")
            print(f"    Uploaded: {uploaded}")
            print(f"    Skipped (duplicates): {skipped}")
            print(f"    Failed: {failed}")

            if failed == 0:
                self.tracker.complete_deck(deck_name, len(words), len(sentences))
                print(f"\n  ✓ Deck '{deck_name}' completed successfully!")
                return True
            else:
                self.tracker.fail_deck(deck_name, f"{failed} sentences failed to upload")
                print(f"\n  ✗ Deck '{deck_name}' completed with errors")
                return False

        except Exception as e:
            print(f"\n  ✗ Error processing {deck_name}: {e}")
            import traceback
            traceback.print_exc()
            self.tracker.fail_deck(deck_name, str(e))
            return False

    def run_all(self):
        """Process all decks automatically"""
        all_decks = self.get_all_decks()
        self.tracker.progress['total_decks'] = len(all_decks)
        self.tracker.save_progress()

        print(f"\n{'='*60}")
        print(f"FULLY AUTOMATED DECK PROCESSING")
        print(f"{'='*60}")
        print(f"Total decks: {len(all_decks)}")
        print(f"Sentences per word: {self.sentences_per_word}")
        print(f"Resume mode: {'Enabled' if self.resume else 'Disabled'}")
        print(f"{'='*60}\n")

        # Show current progress
        if self.resume and self.tracker.progress['completed_decks']:
            print("Current progress:")
            print(f"  Completed: {len(self.tracker.progress['completed_decks'])} decks")
            print(f"  Failed: {len(self.tracker.progress['failed_decks'])} decks")
            print()

        success_count = 0
        failed_count = 0

        for idx, deck_name in enumerate(all_decks, 1):
            # Skip if already completed (resume mode)
            if self.resume and self.tracker.is_completed(deck_name):
                print(f"[{idx}/{len(all_decks)}] ⊘ Skipping '{deck_name}' (already completed)")
                success_count += 1
                continue

            print(f"\n[{idx}/{len(all_decks)}] Processing '{deck_name}'...")

            success = self.process_single_deck(deck_name)

            if success:
                success_count += 1
            else:
                failed_count += 1

            # Show running summary
            print(f"\nRunning total: {success_count} completed, {failed_count} failed, {len(all_decks) - idx} remaining")

        # Final summary
        print(f"\n\n{'='*60}")
        print(f"BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(self.tracker.get_summary())

        if self.tracker.progress['failed_decks']:
            print("\nFailed Decks:")
            for failure in self.tracker.progress['failed_decks']:
                print(f"  - {failure['deck_name']}: {failure['error']}")

        return success_count, failed_count


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Fully automated deck sentence generation')
    parser.add_argument('--sentences', type=int, default=10,
                       help='Number of sentences per word (default: 10)')
    parser.add_argument('--no-resume', action='store_true',
                       help='Start fresh, ignore previous progress')
    parser.add_argument('--status', action='store_true',
                       help='Show current progress status only')

    args = parser.parse_args()

    processor = FullyAutomatedProcessor(
        sentences_per_word=args.sentences,
        resume=not args.no_resume
    )

    if args.status:
        # Just show status
        print(processor.tracker.get_summary())
    else:
        # Run full processing
        success, failed = processor.run_all()
        sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()

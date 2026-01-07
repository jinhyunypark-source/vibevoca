/**
 * Deck Sentence Generator Skill
 *
 * VibeVoca 덱 예문 자동 생성 스킬
 */

export const metadata = {
  name: 'deck-sentence-generator',
  description: 'VibeVoca 덱의 영어 예문을 자동으로 생성하고 데이터베이스에 업로드',
  version: '1.0.0',
  author: 'Claude Code',
  tags: ['vibevoca', 'database', 'automation', 'sentences'],
};

export async function run(args: string[]): Promise<void> {
  const baseDir = '/Users/jin/dev/vibevoca/claude/scripts';
  const venvActivate = 'source /Users/jin/dev/vibevoca/claude/venv/bin/activate';

  // Parse arguments
  const command = args[0];

  if (!command) {
    console.log(`
사용법:
  /deck-sentence-generator <deck_name>     # 특정 덱 처리
  /deck-sentence-generator --all           # 전체 덱 처리
  /deck-sentence-generator --status        # 진행상황 확인
  /deck-sentence-generator --retry         # 실패한 덱만 재시도
  /deck-sentence-generator --help          # 도움말

예시:
  /deck-sentence-generator TASTE
  /deck-sentence-generator LOGIC_CLARITY
  /deck-sentence-generator --all
`);
    return;
  }

  if (command === '--help') {
    console.log('Deck Sentence Generator 스킬 도움말은 SKILL.md를 참조하세요.');
    return;
  }

  if (command === '--status') {
    // Show progress status
    await executeCommand(
      `${venvActivate} && cd ${baseDir} && python3 process_all_decks_auto.py --status`
    );
    return;
  }

  if (command === '--all' || command === '--retry') {
    // Process all decks (resume mode will skip completed ones)
    console.log('전체 덱 자동 처리를 시작합니다...\n');
    await executeCommand(
      `${venvActivate} && cd ${baseDir} && python3 process_all_decks_auto.py`
    );
    return;
  }

  // Single deck processing
  const deckName = command;
  console.log(`덱 '${deckName}' 처리를 시작합니다...\n`);

  // Run the processing steps
  await processSingleDeck(baseDir, venvActivate, deckName);
}

async function processSingleDeck(
  baseDir: string,
  venvActivate: string,
  deckName: string
): Promise<void> {
  const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0].replace('T', '_');

  console.log('[1/4] 단어 추출 중...');
  await executeCommand(
    `${venvActivate} && cd ${baseDir} && python3 -c "
from extract_words_from_deck import WordExtractor
import json
extractor = WordExtractor()
words = extractor.get_words_by_deck_name('${deckName}')
with open('output/words_${deckName}_${timestamp}.json', 'w', encoding='utf-8') as f:
    json.dump(words, f, indent=2, ensure_ascii=False)
print(f'✓ {len(words)}개 단어 추출 완료')
"`
  );

  console.log('\n[2/4] 태그 추출 중...');
  await executeCommand(
    `${venvActivate} && cd ${baseDir} && python3 -c "
from extract_all_tags import TagExtractor
import json
extractor = TagExtractor()
tags = extractor.get_all_tags()
with open('output/tags_${deckName}_${timestamp}.json', 'w', encoding='utf-8') as f:
    json.dump(tags, f, indent=2, ensure_ascii=False)
print(f'✓ {len(tags[\\"all_unique_tags\\"])}개 태그 추출 완료')
"`
  );

  console.log('\n[3/4] 예문 생성 중...');
  await executeCommand(
    `${venvActivate} && cd ${baseDir} && python3 generate_sentences_automated.py \
      output/words_${deckName}_${timestamp}.json \
      output/tags_${deckName}_${timestamp}.json \
      output/sentences_${deckName}_${timestamp}.json \
      10`
  );

  console.log('\n[4/4] 데이터베이스 업로드 중...');
  await executeCommand(
    `${venvActivate} && cd ${baseDir} && python3 upload_sentences_to_db.py \
      --input output/sentences_${deckName}_${timestamp}.json \
      --skip-duplicates`
  );

  console.log(`\n✓ 덱 '${deckName}' 처리 완료!`);
}

async function executeCommand(command: string): Promise<void> {
  // This would execute the command - implementation depends on the runtime
  // For now, this is a placeholder
  console.log(`Executing: ${command}`);
}

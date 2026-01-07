# Deck Sentence Generator Skill

VibeVoca 프로젝트의 덱(Deck)별 영어 예문 자동 생성 및 데이터베이스 업로드 스킬

## 설명

이 스킬은 Supabase 데이터베이스의 덱(decks)과 카드(cards) 정보를 읽어, 각 단어에 대한 예문을 자동 생성하고 card_sentences 테이블에 업로드합니다.

## 주요 기능

1. **단일 덱 처리**: 특정 덱 이름을 지정하여 해당 덱의 예문만 생성
2. **전체 덱 일괄 처리**: 모든 덱을 자동으로 순차 처리
3. **진행상황 추적**: 중단 시에도 이어서 작업할 수 있도록 진행상황 저장
4. **중복 방지**: 이미 생성된 예문은 자동으로 스킵

## 사용 방법

### 1. 단일 덱 처리

```bash
/deck-sentence-generator <deck_name>
```

예시:
```bash
/deck-sentence-generator TASTE
/deck-sentence-generator LOGIC_CLARITY
```

### 2. 전체 덱 일괄 처리

```bash
/deck-sentence-generator --all
```

### 3. 진행상황 확인

```bash
/deck-sentence-generator --status
```

### 4. 실패한 덱만 재시도

```bash
/deck-sentence-generator --retry
```

## 처리 과정

1. **단어 추출** (Extract Words)
   - Supabase decks + cards 테이블에서 단어 목록 추출
   - 덱 ID, 카드 ID, 영어 단어, 한글 뜻 포함

2. **태그 추출** (Extract Tags)
   - meta_interests 테이블에서 관련 태그 추출
   - 예문에 맥락을 추가하기 위한 태그 사용

3. **예문 생성** (Generate Sentences)
   - 각 단어당 10개의 예문 자동 생성
   - 영어 문장 + 한글 번역 포함
   - 관련 태그 2-4개 랜덤 선택하여 포함

4. **데이터베이스 업로드** (Upload to DB)
   - card_sentences 테이블에 업로드
   - 중복 체크하여 이미 있는 예문은 스킵
   - 업로드 결과 요약 출력

## 출력 파일

모든 중간 파일은 `claude/scripts/output/` 디렉토리에 저장됩니다:

- `words_<DECK_NAME>_<TIMESTAMP>.json` - 추출된 단어 목록
- `tags_<DECK_NAME>_<TIMESTAMP>.json` - 추출된 태그 목록
- `sentences_<DECK_NAME>_<TIMESTAMP>.json` - 생성된 예문 목록
- `batch_progress.json` - 일괄 처리 진행상황 추적 파일

## 데이터베이스 스키마

### card_sentences 테이블
```sql
{
  "card_id": "uuid",           -- 카드 ID (cards 테이블 참조)
  "word": "string",            -- 영어 단어
  "sentence_en": "string",     -- 영어 예문
  "sentence_ko": "string",     -- 한글 번역
  "tags": ["string"],          -- 관련 태그 배열
  "is_default": false,         -- LLM 생성은 기본값 아님
  "is_verified": false,        -- 검수 필요
  "source": "llm_claude"       -- 생성 소스
}
```

## 설정

### 예문 개수 조정
기본값: 단어당 10개 예문

변경하려면 `process_all_decks_auto.py` 실행 시:
```bash
python3 process_all_decks_auto.py --sentences 15
```

### Resume 모드
기본적으로 활성화되어 있어, 중단 후 재실행 시 완료된 덱은 자동 스킵합니다.

처음부터 다시 시작하려면:
```bash
python3 process_all_decks_auto.py --no-resume
```

## 관련 스크립트

### 핵심 스크립트
- `process_all_decks_auto.py` - 전체 자동화 메인 스크립트
- `extract_words_from_deck.py` - 덱에서 단어 추출
- `extract_all_tags.py` - 태그 추출
- `generate_sentences_automated.py` - 예문 자동 생성
- `upload_sentences_to_db.py` - 데이터베이스 업로드

### 진행상황 추적
- `batch_progress.json` - 완료/실패 덱 목록 및 통계

## 예시 실행 결과

```
============================================================
FULLY AUTOMATED DECK PROCESSING
============================================================
Total decks: 53
Sentences per word: 10
Resume mode: Enabled
============================================================

[1/53] Processing 'TASTE'...

[1/4] Extracting words from TASTE...
  ✓ Extracted 22 words

[2/4] Extracting tags...
  ✓ Extracted 15 tags

[3/4] Generating sentences (automated)...
  ✓ Generated 220 sentences

[4/4] Uploading to database...
  Upload Summary:
    Uploaded: 220
    Skipped (duplicates): 0
    Failed: 0

  ✓ Deck 'TASTE' completed successfully!
```

## 문제 해결

### 중복 예문 스킵
이미 데이터베이스에 있는 예문은 자동으로 스킵됩니다. 이는 정상 동작입니다.

### 업로드 실패
일부 문장이 업로드 실패하는 경우:
1. 네트워크 연결 확인
2. Supabase 연결 확인
3. `--retry` 옵션으로 재시도

### 진행상황 초기화
```bash
rm output/batch_progress.json
```

## 주의사항

1. **데이터베이스 연결**: Supabase 환경변수가 올바르게 설정되어 있어야 합니다
2. **중복 방지**: 같은 덱을 여러 번 실행해도 중복 예문은 생성되지 않습니다
3. **생성 품질**: 자동 생성된 예문은 `is_verified: false`로 저장되므로, 추후 검수가 필요할 수 있습니다

## 통계 (마지막 실행 기준)

- 총 처리 덱: 53개
- 총 단어 수: 1,568개
- 총 생성 예문: 15,680개
- 성공률: 100%

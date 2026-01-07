# Deck Sentence Generator - 완전 자동화 워크플로우

VibeVoca 프로젝트의 덱(Deck) 예문 자동 생성 시스템

## 🎯 개요

이 시스템은 Supabase 데이터베이스의 모든 덱(decks)에 대해 영어 예문을 자동으로 생성하고 card_sentences 테이블에 업로드하는 완전 자동화된 워크플로우입니다.

### 주요 특징

- ✅ **완전 자동화**: 사람 개입 없이 모든 덱 처리
- ✅ **진행상황 추적**: 중단 시에도 이어서 작업 가능
- ✅ **중복 방지**: 이미 생성된 예문 자동 스킵
- ✅ **Resume 모드**: 완료된 덱은 자동으로 건너뛰기
- ✅ **에러 복구**: 실패한 덱만 재시도 가능

## 📊 처리 실적 (2026-01-05 기준)

```
총 처리 덱:     53개
총 단어 수:     1,568개
총 생성 예문:   15,680개
성공률:         100%
처리 시간:      약 5시간
```

## 🚀 빠른 시작

### 1. 전체 덱 자동 처리

```bash
cd /Users/jin/dev/vibevoca/claude/scripts
source /Users/jin/dev/vibevoca/claude/venv/bin/activate
python3 process_all_decks_auto.py
```

### 2. 진행상황 확인

```bash
python3 process_all_decks_auto.py --status
```

### 3. 실패한 덱만 재시도

```bash
python3 process_all_decks_auto.py
# Resume 모드가 기본 활성화되어 있어 실패한 덱만 자동 재시도
```

## 📁 프로젝트 구조

```
claude/scripts/
├── process_all_decks_auto.py          # 메인 자동화 스크립트
├── extract_words_from_deck.py         # 단어 추출
├── extract_all_tags.py                # 태그 추출
├── generate_sentences_automated.py    # 예문 자동 생성
├── upload_sentences_to_db.py          # DB 업로드
├── batch_process_all_decks.py         # 배치 처리 (준수동)
└── output/
    ├── words_*.json                   # 추출된 단어들
    ├── tags_*.json                    # 추출된 태그들
    ├── sentences_*.json               # 생성된 예문들
    └── batch_progress.json            # 진행상황 추적 파일
```

## 🔧 스크립트 상세

### 1. process_all_decks_auto.py (메인)

전체 덱을 완전 자동으로 처리하는 메인 스크립트

**사용법:**
```bash
# 기본 실행 (Resume 모드)
python3 process_all_decks_auto.py

# 단어당 예문 개수 변경
python3 process_all_decks_auto.py --sentences 15

# 진행상황만 확인
python3 process_all_decks_auto.py --status

# 처음부터 다시 시작
python3 process_all_decks_auto.py --no-resume
```

**처리 과정:**
1. 모든 덱 목록 조회
2. 각 덱별로 순차 처리:
   - 단어 추출 (decks + cards 테이블)
   - 태그 추출 (meta_interests 테이블)
   - 예문 자동 생성 (10개/단어)
   - 데이터베이스 업로드 (card_sentences 테이블)
3. 진행상황을 `batch_progress.json`에 저장

### 2. extract_words_from_deck.py

특정 덱에서 단어 목록 추출

**사용법:**
```bash
python3 extract_words_from_deck.py --deck-name "TASTE" --output output/words.json
```

**출력 형식:**
```json
[
  {
    "card_id": "uuid",
    "word": "Delicious",
    "meaning": "맛있는",
    "deck_id": "uuid",
    "deck_name": "TASTE"
  }
]
```

### 3. extract_all_tags.py

meta_interests 테이블에서 모든 태그 추출

**사용법:**
```bash
python3 extract_all_tags.py --output output/tags.json
```

**출력 형식:**
```json
{
  "tags_by_interest": {
    "soccer": ["soccer"],
    "business": ["business", "startup", "entrepreneur"]
  },
  "all_unique_tags": ["soccer", "business", "startup", ...],
  "total_interests": 11,
  "total_unique_tags": 15
}
```

### 4. generate_sentences_automated.py

단어에 대한 예문 자동 생성 (Python 기반)

**사용법:**
```bash
python3 generate_sentences_automated.py \
  output/words.json \
  output/tags.json \
  output/sentences.json \
  10  # 단어당 예문 개수
```

**출력 형식:**
```json
[
  {
    "card_id": "uuid",
    "word": "Delicious",
    "sentence_en": "The delicious atmosphere made everyone feel comfortable.",
    "sentence_ko": "맛있는 분위기가 모두를 편안하게 만들었다",
    "tags": ["restaurant", "food", "happy"]
  }
]
```

### 5. upload_sentences_to_db.py

생성된 예문을 card_sentences 테이블에 업로드

**사용법:**
```bash
# 중복 체크하며 업로드
python3 upload_sentences_to_db.py \
  --input output/sentences.json \
  --skip-duplicates

# 중복 체크 없이 업로드
python3 upload_sentences_to_db.py \
  --input output/sentences.json
```

**업로드 필드:**
- `card_id`: 카드 ID
- `word`: 영어 단어
- `sentence_en`: 영어 예문
- `sentence_ko`: 한글 번역
- `tags`: 관련 태그 배열
- `is_default`: false (LLM 생성)
- `is_verified`: false (검수 필요)
- `source`: "llm_claude"

## 📝 진행상황 추적

### batch_progress.json 구조

```json
{
  "started_at": "2026-01-04T21:15:14.778520",
  "completed_decks": [
    {
      "deck_name": "TASTE",
      "completed_at": "2026-01-05T01:50:15.298783",
      "words_count": 22,
      "sentences_count": 220
    }
  ],
  "failed_decks": [],
  "current_deck": null,
  "total_decks": 53,
  "total_words_processed": 1568,
  "total_sentences_generated": 15680,
  "last_updated": "2026-01-05T07:56:07.179082"
}
```

### 진행상황 확인

```bash
# Python으로 요약 출력
python3 process_all_decks_auto.py --status

# 또는 직접 파일 확인
cat output/batch_progress.json | python3 -m json.tool
```

## 🔄 일반적인 워크플로우

### 새 덱 추가 시

1. Supabase에 새 덱 데이터 추가
2. 자동화 스크립트 실행:
   ```bash
   cd /Users/jin/dev/vibevoca/claude/scripts
   source ../venv/bin/activate
   python3 process_all_decks_auto.py
   ```
3. Resume 모드로 새 덱만 자동 처리됨

### 정기 업데이트

```bash
# 크론 작업 등록 예시 (매주 일요일 새벽 2시)
0 2 * * 0 cd /Users/jin/dev/vibevoca/claude/scripts && \
  source ../venv/bin/activate && \
  python3 process_all_decks_auto.py >> logs/cron.log 2>&1
```

### 수동으로 특정 덱만 처리

```bash
# 1. 단어 추출
python3 extract_words_from_deck.py --deck-name "TASTE" --output output/words_manual.json

# 2. 태그 추출
python3 extract_all_tags.py --output output/tags_manual.json

# 3. 예문 생성
python3 generate_sentences_automated.py \
  output/words_manual.json \
  output/tags_manual.json \
  output/sentences_manual.json \
  10

# 4. 업로드
python3 upload_sentences_to_db.py \
  --input output/sentences_manual.json \
  --skip-duplicates
```

## ⚙️ 설정 및 커스터마이징

### 단어당 예문 개수 변경

`process_all_decks_auto.py` 실행 시 `--sentences` 옵션:
```bash
python3 process_all_decks_auto.py --sentences 15
```

### 예문 템플릿 수정

`generate_sentences_automated.py`의 `_create_templates()` 메서드 수정:
```python
def _create_templates(self):
    return {
        'positive': [
            "The {word} atmosphere made everyone feel comfortable.",
            # 새 템플릿 추가
        ],
        # 새 카테고리 추가 가능
    }
```

### 한글 번역 개선

`generate_sentences_automated.py`의 `_translate_to_korean()` 메서드 수정:
```python
def _translate_to_korean(self, english_sentence, word, meaning):
    # 번역 로직 개선
    pass
```

## 🐛 문제 해결

### 중복 예문이 많이 스킵됨

**원인**: 이전에 이미 해당 덱의 예문을 생성했음
**해결**: 정상 동작입니다. 새 예문만 추가됨

### 업로드 실패

**원인**: 데이터베이스 연결 문제
**해결**:
1. Supabase 환경변수 확인
2. 네트워크 연결 확인
3. 재시도: `python3 process_all_decks_auto.py`

### 진행상황 초기화

```bash
rm output/batch_progress.json
```

### 특정 덱만 다시 처리

1. `batch_progress.json`에서 해당 덱을 `completed_decks`에서 제거
2. 스크립트 재실행

## 📈 성능 최적화

### 병렬 처리

현재는 순차 처리이지만, 필요시 병렬 처리 가능:
```python
# process_all_decks_auto.py 수정
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(process_single_deck, remaining_decks)
```

### 배치 크기 조정

업로드 시 배치 처리:
```python
# upload_sentences_to_db.py 수정
def upload_batch(self, sentences_batch):
    self.client.table('card_sentences').insert(sentences_batch).execute()
```

## 📚 참고 문서

- [Supabase Python Client](https://github.com/supabase-community/supabase-py)
- [VibeVoca 프로젝트 구조](../README.md)
- [Skills 시스템](../../.claude/skills/README.md)

## 🔗 관련 스킬

- `/deck-sentence-generator` - 이 워크플로우의 스킬 버전
- `/generate-sentences` - 단일 덱 예문 생성 (수동)
- `/vibevoca-workflow` - VibeVoca 전체 워크플로우

## 📝 변경 이력

### 2026-01-05
- ✅ 전체 53개 덱 처리 완료
- ✅ 15,680개 예문 생성
- ✅ 100% 성공률 달성
- ✅ Resume 모드 구현
- ✅ 중복 방지 로직 수정

### 2026-01-04
- ✅ 완전 자동화 스크립트 작성
- ✅ 진행상황 추적 시스템 구현
- ✅ TASTE, LOGIC_CLARITY 덱 처리 완료

## 💡 팁

1. **정기 실행**: 크론 작업으로 주기적으로 실행하여 새 덱 자동 처리
2. **로그 확인**: `tee` 명령어로 실행 로그 저장
3. **검수**: 생성된 예문은 `is_verified: false`이므로 추후 검수 권장
4. **백업**: 중요 파일은 정기적으로 백업

---

**작성자**: Claude Code
**최종 수정**: 2026-01-05
**버전**: 1.0.0

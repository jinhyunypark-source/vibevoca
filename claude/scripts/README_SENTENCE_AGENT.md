# Sentence Generation Agent

예문 생성 에이전트는 deck 이름을 입력받아 자동으로 영어 단어 예문을 생성하고 데이터베이스에 저장하는 통합 시스템입니다.

## 개요

사용자가 deck 이름을 제공하면 다음 과정을 자동으로 수행합니다:

1. **영어 단어 추출**: deck 이름으로 Supabase의 `decks`, `cards` 테이블을 조인하여 `front_text` 리스트 추출
2. **태그 목록 추출**: `meta_interests` 테이블의 `related_tags` 컬럼에서 모든 태그 정보 추출
3. **예문 생성**: Claude API를 사용하여 각 단어별로 5-10개의 자연스러운 예문 생성 (태그 참조)
4. **DB 반영**: 생성된 예문을 `card_sentences` 테이블에 업로드

## 사전 준비

### 1. 환경 변수 설정

`.env` 파일에 다음 설정이 필요합니다:

```bash
# Supabase 설정
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Anthropic API 설정
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 2. Python 패키지 설치

```bash
cd /Users/jin/dev/vibevoca/claude
source venv/bin/activate
pip install -r requirements.txt
```

필요한 패키지:
- `supabase>=2.0.0`
- `python-dotenv>=1.0.0`
- `anthropic>=0.40.0`

## 사용 방법

### 통합 에이전트 (권장)

deck 이름만 입력하면 전체 프로세스를 자동으로 실행합니다:

```bash
cd /Users/jin/dev/vibevoca/claude/scripts

# 기본 사용
python sentence_generation_agent.py --deck-name "Daily Essentials"

# 중복 예문 건너뛰기
python sentence_generation_agent.py --deck-name "Business English" --skip-duplicates

# 중간 파일 보존 (디버깅용)
python sentence_generation_agent.py --deck-name "Travel Phrases" --keep-files
```

**옵션:**
- `--deck-name`: (필수) 처리할 deck의 이름
- `--api-key`: Anthropic API key (환경변수 대신 직접 지정)
- `--skip-duplicates`: 중복 예문 건너뛰기
- `--keep-files`: 중간 생성 파일 보존

### 개별 스크립트 사용

각 단계를 개별적으로 실행할 수도 있습니다:

#### Step 1: 영어 단어 추출

```bash
python extract_words_from_deck.py --deck-name "Daily Essentials" --output words.json
```

**출력 형식:**
```json
[
  {
    "card_id": "uuid",
    "word": "exhausted",
    "meaning": "매우 피곤한",
    "deck_id": "uuid",
    "deck_name": "Daily Essentials"
  }
]
```

#### Step 2: 태그 목록 추출

```bash
python extract_all_tags.py --output tags.json
```

**출력 형식:**
```json
{
  "tags_by_interest": {
    "baseball": ["baseball", "sports", "mlb", "kbo"],
    "soccer": ["soccer", "football", "sports", "premier_league"]
  },
  "all_unique_tags": ["ai", "album", "baseball", ...],
  "total_interests": 15,
  "total_unique_tags": 45
}
```

#### Step 3: 예문 생성

```bash
python generate_sentences_with_llm.py \
  --words words.json \
  --tags tags.json \
  --output sentences.json
```

**출력 형식:**
```json
[
  {
    "card_id": "uuid",
    "word": "exhausted",
    "sentence_en": "After the marathon, I felt completely exhausted.",
    "sentence_ko": "마라톤 후에 완전히 지쳤다.",
    "tags": ["fitness", "sports"],
    "deck_name": "Daily Essentials"
  }
]
```

#### Step 4: DB 업로드

```bash
python upload_sentences_to_db.py --input sentences.json --skip-duplicates
```

## 출력 결과

### card_sentences 테이블 스키마

생성된 예문은 다음 형식으로 저장됩니다:

| 컬럼 | 타입 | 설명 |
|------|------|------|
| `card_id` | UUID | 단어 카드 ID |
| `word` | TEXT | 영어 단어 |
| `sentence_en` | TEXT | 영어 예문 |
| `sentence_ko` | TEXT | 한국어 번역/설명 |
| `tags` | TEXT[] | 참조한 관심사 태그 |
| `is_default` | BOOLEAN | 기본 예문 여부 (LLM 생성은 false) |
| `is_verified` | BOOLEAN | 검수 완료 여부 |
| `source` | TEXT | 출처 (llm_claude) |

## 주의사항

### API 비용

- Claude API 호출 비용이 발생합니다
- 50개 단어 기준 약 $0.50-$1.00 예상
- 프롬프트 실행 전 확인 메시지가 표시됩니다

### 실행 시간

- 단어당 약 5초 소요
- 50개 단어 기준 약 4-5분
- 진행 상황은 10개 단어마다 자동 저장됩니다

### 중복 처리

- `--skip-duplicates` 옵션 사용 권장
- 동일한 card_id와 sentence_en 조합은 건너뜁니다

## 예제 실행

```bash
# 1. 가상환경 활성화
cd /Users/jin/dev/vibevoca/claude
source venv/bin/activate

# 2. 환경 변수 확인
echo $SUPABASE_URL
echo $ANTHROPIC_API_KEY

# 3. 에이전트 실행
cd scripts
python sentence_generation_agent.py --deck-name "Daily Essentials" --skip-duplicates

# 출력 예시:
# ======================================================================
#   Sentence Generation Agent
#   Deck: Daily Essentials
# ======================================================================
#
# ======================================================================
#   Step 1: Extract Words from Deck
# ======================================================================
# Deck name: Daily Essentials
# ✓ Extracted 48 words
# ...
```

## 트러블슈팅

### "Deck not found" 오류

- deck 이름이 정확한지 확인
- Supabase `decks` 테이블에 해당 이름이 존재하는지 확인

### API 키 오류

```bash
# 환경 변수 확인
echo $ANTHROPIC_API_KEY

# 또는 직접 지정
python sentence_generation_agent.py --deck-name "..." --api-key "sk-ant-..."
```

### 중복 예문 오류

- `--skip-duplicates` 옵션 사용
- 또는 기존 예문을 먼저 삭제

### 네트워크 타임아웃

- API 호출이 실패하면 자동으로 스킵됩니다
- 중간 저장된 파일 (`--keep-files`)을 사용하여 재시도 가능

## 파일 구조

```
claude/scripts/
├── extract_words_from_deck.py      # Step 1: 단어 추출
├── extract_all_tags.py             # Step 2: 태그 추출
├── generate_sentences_with_llm.py  # Step 3: 예문 생성
├── upload_sentences_to_db.py       # Step 4: DB 업로드
├── sentence_generation_agent.py    # 통합 에이전트
└── output/                         # 생성된 파일 저장 (임시)
    ├── words_20260104_120000.json
    ├── tags_20260104_120000.json
    └── sentences_20260104_120000.json
```

## 라이선스

VibeVoca 프로젝트의 일부입니다.

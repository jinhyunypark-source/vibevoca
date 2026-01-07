# AI 기반 단어 컨텐츠 관리 시스템

VibeVoca 앱의 단어 컨텐츠를 AI를 활용해 관리하는 도구 모음입니다.

## 구조

```
claude/
├── config/
│   └── supabase_config.py    # Supabase 연결 설정
├── prompts/
│   └── word_prompts.md       # AI 프롬프트 템플릿
├── scripts/
│   ├── word_manager.py       # 단어 CRUD 관리
│   └── ai_generator.py       # AI 기반 생성 도구
├── requirements.txt
└── README.md
```

## 설치

```bash
cd claude
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 환경 설정

프로젝트 루트의 `.env` 파일에 다음 변수가 필요합니다:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 사용법

### 1. 단어 관리 (word_manager.py)

```bash
# 카테고리 목록 조회
python scripts/word_manager.py list-categories

# 데크 목록 조회
python scripts/word_manager.py list-decks

# 특정 데크의 카드 목록 조회
python scripts/word_manager.py list-cards <deck_id>

# 새 단어 추가
python scripts/word_manager.py add-word <deck_id> \
    --word "eloquent" \
    --meaning "유창한, 설득력 있는" \
    --examples "She gave an eloquent speech." "His writing is eloquent."

# 단어 수정
python scripts/word_manager.py update-word <card_id> \
    --meaning "새로운 뜻"

# 단어 삭제
python scripts/word_manager.py delete-word <card_id>
```

### 2. AI 생성 도구 (ai_generator.py)

```bash
# 데크에 맞는 새 단어 생성
python scripts/ai_generator.py generate-words <deck_id> --count 5

# 컨텍스트 기반 예문 생성
python scripts/ai_generator.py generate-example <card_id> \
    --place cafe \
    --emotion happy \
    --environment quiet

# 단어 설명 개선
python scripts/ai_generator.py improve-definition <card_id>

# 유사 단어 추천
python scripts/ai_generator.py suggest-similar <card_id> --count 3
```

## 주요 기능

### 단어 관리
- 카테고리/데크/카드 조회
- 단어 추가/수정/삭제 (CRUD)
- Supabase 데이터베이스 직접 연동

### AI 생성
- **새 단어 생성**: 데크 주제에 맞는 단어를 AI가 자동 생성
- **컨텍스트 예문**: 장소/감정/환경에 맞는 예문 생성
- **설명 개선**: 기존 단어 설명을 더 이해하기 쉽게 개선
- **유사 단어**: 학습에 도움되는 관련 단어 추천

## 데이터 모델

### Cards 테이블
| 컬럼 | 타입 | 설명 |
|-----|-----|-----|
| id | uuid | 기본 키 |
| deck_id | uuid | 데크 FK |
| front_text | text | 영어 단어 |
| back_text | text | 한글 뜻 |
| example_sentences | text[] | 예문 배열 |
| audio_url | text | 오디오 URL (선택) |

### Contexts 테이블
| 컬럼 | 타입 | 설명 |
|-----|-----|-----|
| id | uuid | 기본 키 |
| type | text | place/emotion/environment |
| slug | text | 고유 식별자 |
| label | text | 표시 이름 |
| prompt_description | text | AI 프롬프트용 설명 |

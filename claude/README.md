# AI 기반 단어 컨텐츠 관리 시스템

VibeVoca 앱의 단어 컨텐츠를 AI를 활용해 관리하는 도구 모음입니다.

## 구조

```
claude/
├── config/
│   └── supabase_config.py       # Supabase 연결 설정
├── prompts/
│   └── word_prompts.md          # AI 프롬프트 템플릿
├── scripts/
│   ├── word_manager.py          # 단어 CRUD 관리
│   └── ai_generator.py          # AI 기반 생성 도구
├── word_files/                  # 추출된 단어 파일들 (1.txt ~ 25.txt, 64개씩)
├── word_prompts_output/         # 생성된 프롬프트 파일들 (1_prompt.txt ~ 25_prompt.txt, 8x8 그리드)
├── input_image/                 # AI 생성 이미지 입력 (2048x2048)
├── output_images/               # 분할된 이미지 출력 (256x256)
├── export_words.py              # Supabase 단어 추출 스크립트
├── generate_prompts.py          # 프롬프트 생성 스크립트
├── split_images.py              # 이미지 분할 및 매핑 스크립트
├── word_image_mapping.csv       # 이미지-단어-card_id 매핑 (CSV)
├── word_image_mapping.json      # 이미지-단어-card_id 매핑 (JSON)
├── word_image_summary.txt       # 매핑 요약
├── requirements.txt
├── README.md
└── WORK_LOG.md                  # 작업 이력 기록
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

### 3. 단어 추출 도구 (export_words.py)

```bash
# Supabase cards 테이블에서 영어 단어 추출하여 파일로 저장
python export_words.py
```

- cards 테이블의 front_text 필드에서 모든 영어 단어를 가져옴
- 64개씩 그룹으로 나누어 `word_files/1.txt`, `word_files/2.txt` 등으로 저장
- 총 1568개 단어 → 25개 파일 생성 (마지막 파일은 32개)
- 자세한 내용은 `WORK_LOG.md` 참고

### 4. 프롬프트 생성 도구 (generate_prompts.py)

```bash
# 단어 파일에서 이미지 생성용 프롬프트 자동 생성
python3 generate_prompts.py
```

- `word_files/` 디렉토리의 각 txt 파일을 읽어 프롬프트 생성
- AI 이미지 생성 도구(DALL-E, Midjourney 등)에 사용할 프롬프트 출력
- **설정**: 64개 단어, 8x8 그리드, 2048x2048 픽셀, 흰색 배경, 테두리 없음
- 스크립트 상단의 `PROMPT_TEMPLATE` 변수를 수정하여 프롬프트 내용 변경 가능
- 생성된 프롬프트는 `word_prompts_output/` 디렉토리에 저장
- 자세한 내용은 `WORK_LOG.md` 참고

### 5. 이미지 분할 도구 (split_images.py)

```bash
# AI 생성 이미지를 64개 개별 이미지로 분할
python split_images.py
```

- `input_image/` 디렉토리의 2048x2048 이미지를 8x8 그리드로 분할
- 각 분할 이미지: 256x256 픽셀
- Supabase cards 테이블의 card_id와 자동 매핑
- 매핑 파일 생성: CSV, JSON, TXT 형식
- 출력: `output_images/` 디렉토리에 `{원본번호}_{위치}.png` 형식으로 저장
- 자세한 내용은 `WORK_LOG.md` 참고

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

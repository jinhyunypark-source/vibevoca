# Sentence Generation Agent (Claude Code Skill Version)

**별도의 API 키 없이** Claude Code의 skill 기능을 활용하여 예문을 생성하는 시스템입니다.

## 주요 변경사항

기존 버전과의 차이점:

| 구분 | 기존 (API 버전) | 신규 (Skill 버전) |
|------|----------------|------------------|
| **Step 3 예문 생성** | Python + Anthropic API | Claude Code Skill |
| **API 키 필요** | ✅ 필수 | ❌ 불필요 |
| **비용** | API 호출 비용 발생 | 무료 (현재 세션) |
| **실행 방식** | 자동 실행 | 대화형 실행 |

## 시스템 구조

```
┌─────────────────────────────────────────────────────────────┐
│                  Sentence Generation Agent                   │
└─────────────────────────────────────────────────────────────┘

Step 1: Extract Words (Python)
  ↓
  extract_words_from_deck.py
  → words.json

Step 2: Extract Tags (Python)
  ↓
  extract_all_tags.py
  → tags.json

Step 3: Generate Sentences (Claude Code Skill) ← API 키 불필요!
  ↓
  /generate-sentences
  → sentences.json

Step 4: Upload to DB (Python)
  ↓
  upload_sentences_to_db.py
  → card_sentences 테이블
```

## 설치 및 준비

### 1. Skill 설치 확인

Skill이 이미 설치되어 있는지 확인:

```bash
ls -la /Users/jin/dev/vibevoca/.claude/skills/generate-sentences/
```

다음 파일이 있어야 합니다:
- `SKILL.md` - skill 정의 및 사용법

### 2. Python 패키지

```bash
cd /Users/jin/dev/vibevoca/claude
source venv/bin/activate
pip install -r requirements.txt
```

필요한 패키지:
- `supabase>=2.0.0`
- `python-dotenv>=1.0.0`

### 3. 환경 변수

`.env` 파일에 Supabase 설정만 필요:

```bash
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

❌ `ANTHROPIC_API_KEY`는 필요 없습니다!

## 사용 방법

### 방법 1: 통합 대화형 실행 (권장)

한 번의 명령으로 전체 프로세스를 진행:

```bash
cd /Users/jin/dev/vibevoca/claude/scripts
python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials"
```

**실행 과정:**

1. **Step 1-2 자동 실행**
   - 단어 추출
   - 태그 추출
   - 파일 생성

2. **Step 3 안내 표시**
   ```
   ┌──────────────────────────────────────────────────────────────┐
   │                                                              │
   │ 🤖 이제 Claude Code Skill을 실행하세요!                      │
   │                                                              │
   │ 다음 명령을 Claude Code에서 실행:                            │
   │                                                              │
   │ /generate-sentences <words_file> <tags_file> <output_file>   │
   │                                                              │
   └──────────────────────────────────────────────────────────────┘
   ```

3. **Skill 실행 대기**
   - Claude Code에서 `/generate-sentences` 실행
   - 완료 후 `done` 입력

4. **Step 4 자동 실행**
   - DB 업로드
   - 완료 보고

### 방법 2: 단계별 실행

각 단계를 개별적으로 실행:

#### Step 1-2: 파일 준비

```bash
python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials" --prepare
```

출력:
```
======================================================================
  Step 1-2: Prepare Files
======================================================================

[Step 1] Extracting words from deck: Daily Essentials
  ✓ Extracted 48 words → /path/to/words_20260104_120000.json

[Step 2] Extracting tags from meta_interests
  ✓ Extracted 15 interests → /path/to/tags_20260104_120000.json

======================================================================
  Step 3: Generate Sentences with Claude Code Skill
======================================================================

💡 Skill이 완료되면 다음 명령으로 Step 4를 실행하세요:

  python sentence_generation_agent_with_skill.py --deck-name "Daily Essentials" --upload /path/to/sentences_20260104_120000.json
```

#### Step 3: Skill 실행

Claude Code에서:

```bash
/generate-sentences
```

또는 파일 경로를 직접 지정:

```bash
/generate-sentences /path/to/words.json /path/to/tags.json /path/to/sentences.json
```

**Skill이 하는 일:**

1. words.json 읽기
2. tags.json 읽기
3. 각 단어별로 5-10개 예문 생성:
   - 단어의 의미 파악
   - 관련 태그 선택 (자연스러운 것만)
   - 예문 작성 (10-20 단어)
   - 한국어 번역 추가
4. sentences.json에 저장
5. 진행 상황 보고

#### Step 4: DB 업로드

```bash
python sentence_generation_agent_with_skill.py \
  --deck-name "Daily Essentials" \
  --upload /path/to/sentences_20260104_120000.json
```

### 방법 3: 개별 스크립트 사용

완전히 수동으로 각 단계 실행:

```bash
# Step 1
python extract_words_from_deck.py --deck-name "Daily Essentials" --output words.json

# Step 2
python extract_all_tags.py --output tags.json

# Step 3 (Claude Code에서)
/generate-sentences words.json tags.json sentences.json

# Step 4
python upload_sentences_to_db.py --input sentences.json --skip-duplicates
```

## Skill 사용법 상세

### /generate-sentences 명령

#### 파라미터 있는 실행

```bash
/generate-sentences <words_file> <tags_file> <output_file>
```

예시:
```bash
/generate-sentences \
  claude/scripts/output/words_20260104_120000.json \
  claude/scripts/output/tags_20260104_120000.json \
  claude/scripts/output/sentences_20260104_120000.json
```

#### 대화형 실행

```bash
/generate-sentences
```

Claude가 물어봅니다:
```
Words file path: claude/scripts/output/words_20260104_120000.json
Tags file path: claude/scripts/output/tags_20260104_120000.json
Output file path: claude/scripts/output/sentences_20260104_120000.json
```

### Skill 실행 예시

```
/generate-sentences words.json tags.json sentences.json

Loading files...
✓ Loaded 48 words
✓ Loaded 15 interests with 45 unique tags

Generating sentences...

[1/48] exhausted (매우 피곤한)
  Generating 7 sentences...
  ✓ Generated 7 sentences
  Tags used: [fitness, sports], [baseball, sports], [gaming]

[2/48] brilliant (훌륭한, 빛나는)
  Generating 7 sentences...
  ✓ Generated 7 sentences
  Tags used: [music, concert], [technology, ai], [movies]

...

[48/48] persistent (끈질긴)
  Generating 7 sentences...
  ✓ Generated 7 sentences
  Tags used: [fitness, workout], [business, startup]

✓ Completed!
  Total sentences: 336
  Saved to: sentences.json
```

## 예문 생성 예시

### 입력 단어: "exhausted" (매우 피곤한)

**생성되는 예문:**

```json
[
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "sentence_en": "After running the marathon, I felt completely exhausted.",
    "sentence_ko": "마라톤을 뛴 후 완전히 지쳤다.",
    "tags": ["fitness", "sports"],
    "deck_name": "Daily Essentials"
  },
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "sentence_en": "The pitcher looked exhausted after throwing 120 pitches.",
    "sentence_ko": "120개의 공을 던진 후 투수는 지쳐 보였다.",
    "tags": ["baseball", "sports"],
    "deck_name": "Daily Essentials"
  },
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "sentence_en": "Faker seemed exhausted after the five-game series.",
    "sentence_ko": "5경기 시리즈 후 페이커는 지쳐 보였다.",
    "tags": ["gaming", "esports"],
    "deck_name": "Daily Essentials"
  }
]
```

## 장점 및 특징

### ✅ 장점

1. **무료**: API 비용 없음 (Claude Code 세션 사용)
2. **안전**: API 키 관리 불필요
3. **대화형**: 실시간으로 진행 상황 확인
4. **유연성**: 중간에 중단하고 나중에 재개 가능
5. **투명성**: 생성 과정을 직접 볼 수 있음

### ⚠️ 주의사항

1. **실행 시간**: 단어당 5-10초 (50개 기준 4-5분)
2. **대화형**: 완전 자동화는 아님 (Step 3에서 수동 실행 필요)
3. **세션 의존**: Claude Code 세션이 활성화되어 있어야 함

## 파일 구조

```
vibevoca/
├── .claude/
│   └── skills/
│       └── generate-sentences/
│           └── SKILL.md                    # Skill 정의
│
└── claude/
    └── scripts/
        ├── extract_words_from_deck.py      # Step 1
        ├── extract_all_tags.py             # Step 2
        ├── upload_sentences_to_db.py       # Step 4
        ├── prepare_for_skill.py            # Step 1-2 통합
        ├── sentence_generation_agent_with_skill.py  # 전체 통합 (권장)
        │
        ├── output/                         # 생성된 파일
        │   ├── words_*.json
        │   ├── tags_*.json
        │   └── sentences_*.json
        │
        └── README_SKILL_VERSION.md         # 이 문서
```

## 비교: API 버전 vs Skill 버전

| 기능 | API 버전 | Skill 버전 |
|------|---------|-----------|
| API 키 필요 | ✅ | ❌ |
| 비용 | $0.50-1.00/50단어 | 무료 |
| 실행 방식 | 완전 자동 | 대화형 |
| 속도 | 빠름 | 비슷함 |
| 진행 상황 확인 | 제한적 | 실시간 |
| 에러 복구 | 중간 저장 | 대화형 조정 |
| 유연성 | 낮음 | 높음 |

## 트러블슈팅

### Skill을 찾을 수 없음

```bash
# Skill 확인
ls -la /Users/jin/dev/vibevoca/.claude/skills/generate-sentences/

# Skill 재설치 (필요시)
# SKILL.md 파일이 있는지 확인
```

### 파일 경로 오류

```bash
# 절대 경로 사용 권장
/generate-sentences \
  /Users/jin/dev/vibevoca/claude/scripts/output/words.json \
  /Users/jin/dev/vibevoca/claude/scripts/output/tags.json \
  /Users/jin/dev/vibevoca/claude/scripts/output/sentences.json
```

### Skill 실행이 중단됨

- 중간 저장 파일이 있다면 재시작 가능
- `--keep-files` 옵션으로 임시 파일 보존

## 빠른 참조

### 전체 프로세스 (한 줄)

```bash
# Step 1-2
python sentence_generation_agent_with_skill.py --deck-name "Your Deck" --prepare

# Step 3 (Claude Code에서)
/generate-sentences

# Step 4
python sentence_generation_agent_with_skill.py --deck-name "Your Deck" --upload <sentences_file>
```

### 대화형 실행 (권장)

```bash
python sentence_generation_agent_with_skill.py --deck-name "Your Deck"
```

## 라이선스

VibeVoca 프로젝트의 일부입니다.

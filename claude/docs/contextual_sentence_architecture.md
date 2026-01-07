# Contextual Sentence System Architecture

## 1. Overview

### Problem
- 1,500 words × 20 contexts = 30,000 sentences (inefficient)
- Static sentences don't adapt to user's real situation

### Solution: Template + Context Composition
- Part-of-speech based templates (~50)
- Context variable sets (~100)
- Dynamic composition = thousands of natural sentences
- Adding new context = just add variable set

---

## 2. Context Layers

```
Layer 1: Word Properties (Static)
├── Part of Speech: adjective, verb, noun, adverb
├── Semantic Category: emotion, action, description, state
└── Usage Patterns: formal, casual, both

Layer 2: User Profile (Semi-static)
├── Profession: developer, designer, teacher, student...
├── Interests: gaming, music, sports, cooking...
└── Learning Level: beginner, intermediate, advanced

Layer 3: Real-time Situation (Dynamic)
├── Place: home, work, commute, cafe...
├── Emotion: happy, tired, stressed, relaxed...
└── Environment: sunny, rainy, hot, cold...
```

---

## 3. Database Schema

### 3.1 Extend `cards` table

```sql
-- Add columns to existing cards table
ALTER TABLE cards ADD COLUMN IF NOT EXISTS part_of_speech TEXT;
ALTER TABLE cards ADD COLUMN IF NOT EXISTS semantic_category TEXT;
ALTER TABLE cards ADD COLUMN IF NOT EXISTS formality TEXT DEFAULT 'both';

-- Part of speech enum values: noun, verb, adjective, adverb, phrase
-- Semantic category: emotion, action, description, state, quality, relation
-- Formality: formal, casual, both
```

### 3.2 Sentence Templates

```sql
CREATE TABLE IF NOT EXISTS sentence_templates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Template targeting
    part_of_speech TEXT NOT NULL,           -- Which word types this template fits
    semantic_category TEXT,                  -- Optional: specific semantic match

    -- Template content (with placeholders)
    template_en TEXT NOT NULL,               -- "The {subject} felt {word} after {action}."
    template_ko TEXT NOT NULL,               -- "{subject}은/는 {action} 후에 {word} 느꼈다."

    -- Context matching
    context_type TEXT NOT NULL,              -- 'general', 'profession', 'place', 'emotion', 'environment'
    context_value TEXT,                      -- Specific value: 'developer', 'home', 'happy'

    -- Quality control
    priority INT DEFAULT 0,                  -- Higher = preferred
    is_active BOOLEAN DEFAULT true,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookup
CREATE INDEX idx_templates_pos ON sentence_templates(part_of_speech);
CREATE INDEX idx_templates_context ON sentence_templates(context_type, context_value);
```

### 3.3 Context Variables (Placeholder Replacements)

```sql
CREATE TABLE IF NOT EXISTS context_variables (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Variable identification
    placeholder TEXT NOT NULL,               -- '{subject}', '{action}', '{place}'

    -- Context matching
    context_type TEXT NOT NULL,              -- 'profession', 'place', 'emotion', 'environment'
    context_value TEXT NOT NULL,             -- 'developer', 'home', 'happy', 'sunny'

    -- Replacement values
    value_en TEXT NOT NULL,                  -- "the developer", "debugging code"
    value_ko TEXT NOT NULL,                  -- "개발자", "코드 디버깅"

    -- Metadata
    tags TEXT[],                             -- Additional matching tags
    priority INT DEFAULT 0,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for fast lookup
CREATE INDEX idx_variables_context ON context_variables(context_type, context_value);
CREATE INDEX idx_variables_placeholder ON context_variables(placeholder);
```

### 3.4 Profession Vocabulary Pool

```sql
CREATE TABLE IF NOT EXISTS profession_vocabulary (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    profession TEXT NOT NULL UNIQUE,         -- 'developer', 'designer', 'teacher'
    profession_ko TEXT NOT NULL,             -- '개발자', '디자이너', '선생님'

    -- Word pools for sentence generation
    subjects JSONB DEFAULT '[]',             -- ["the developer", "my colleague", "the team lead"]
    objects JSONB DEFAULT '[]',              -- ["the code", "the bug", "the server"]
    actions JSONB DEFAULT '[]',              -- ["debugging", "deploying", "reviewing code"]
    places JSONB DEFAULT '[]',               -- ["at the office", "in a meeting", "at my desk"]
    scenarios JSONB DEFAULT '[]',            -- ["after a long meeting", "during code review"]

    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 3.5 Generated Sentence Cache (Optional, for performance)

```sql
CREATE TABLE IF NOT EXISTS sentence_cache (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Reference
    card_id UUID REFERENCES cards(id) ON DELETE CASCADE,

    -- Context fingerprint (for cache lookup)
    context_hash TEXT NOT NULL,              -- MD5 of context combination

    -- Generated content
    sentence_en TEXT NOT NULL,
    sentence_ko TEXT NOT NULL,

    -- Metadata
    template_id UUID REFERENCES sentence_templates(id),
    generation_method TEXT DEFAULT 'template', -- 'template', 'llm', 'manual'
    quality_score FLOAT,                     -- User feedback / AI evaluation

    -- Usage tracking
    usage_count INT DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(card_id, context_hash)
);

CREATE INDEX idx_cache_lookup ON sentence_cache(card_id, context_hash);
```

### 3.6 User Profile (기존 profiles 테이블 확장)

```sql
-- 기존 profiles 테이블에 컬럼 추가 (schema.sql + update_profile_metadata.sql 참조)
-- 기존 컬럼: id, role, interests, job_id, interest_ids

ALTER TABLE profiles ADD COLUMN learning_level TEXT DEFAULT 'intermediate';
ALTER TABLE profiles ADD COLUMN primary_language TEXT DEFAULT 'ko';
ALTER TABLE profiles ADD COLUMN show_romanization BOOLEAN DEFAULT false;

-- job_id를 통해 profession 정보 조회 (meta_jobs 테이블 참조)
```

---

## 3.7 Verb Conjugation (동사 변형 처리)

영어에서 주어에 따른 동사 변형을 처리하는 방법:

### 템플릿 마커 시스템

```
{verb:3s}   → 3인칭 단수 (works, has, does)
{verb:past} → 과거형 (worked, had, did)
{verb:ing}  → 진행형 (working, having, doing)
{verb:base} → 원형 (work, have, do)
```

### 예시

```
템플릿: "The {subject} {verb:3s} {word} after {action}."
입력:   subject="developer", verb="feel", word="exhausted"
결과:   "The developer feels exhausted after debugging."
```

### 변형 규칙

| 규칙 | 원형 | 3인칭 단수 |
|------|------|------------|
| 일반 | work | works |
| -s, -sh, -ch, -x, -z | watch | watches |
| -o | go | goes |
| 자음+y | study | studies |
| 모음+y | play | plays |
| 불규칙 | have, be, do | has, is, does |

### 주어-동사 쌍 (Subject-Verb Pairs)

더 자연스러운 문장을 위해 주어와 동사를 함께 저장:

```sql
-- context_variables 테이블에 subject_verb 타입 추가
{placeholder}: "{subject_verb}"
{context_type}: "profession"
{context_value}: "developer"
{value_en}: "The developer feels"  -- 이미 변형된 형태
{value_ko}: "개발자는 느낀다"
```

### 구현 코드

`claude/scripts/verb_conjugator.py` 참조

---

## 3.8 Mixed Sentence Strategy (50% Default + 50% Personalized)

### 문제점
사용자의 관심사가 몇 개 안 되면 맞춤 예문이 반복되어 지루해짐.

### 해결책
- **50% 기본 예문**: 항상 제공되는 일반적인 예문 (`is_default = true`)
- **50% 맞춤 예문**: 관심사/직업 기반 예문 (`is_default = false`, `tags`로 매칭)

### Hidden Tags 시스템

관심사를 직접 예문에 넣지 않고, **숨겨진 태그**로 연결:

```
사용자 관심사: baseball

예문 1: "Babe Ruth's legendary swing was simply {word}."
        → tags: ['baseball', 'mlb', 'babe_ruth']
        → 예문에 "baseball" 단어 없음!

예문 2: "Lee Dae-ho's home run against Japan was {word}."
        → tags: ['baseball', 'kbo', 'home_run']
        → 예문에 "baseball" 단어 없음!
```

### Interest Tags Mapping 테이블

```sql
interest_tags
├── interest_slug: "baseball"
├── related_tags: ['baseball', 'sports', 'mlb', 'kbo', 'pitcher', 'batter']
├── sample_keywords_en: ['Babe Ruth', 'home run', 'pitcher']
└── sample_keywords_ko: ['베이브 루스', '홈런', '투수']
```

### 예문 조회 SQL

```sql
SELECT * FROM get_mixed_sentences(
    p_card_id := 'uuid',
    p_interest_tags := ARRAY['baseball', 'sports', 'mlb'],
    p_profession := 'developer',
    p_limit := 4
);

-- 결과:
-- 1. 기본 예문 (is_default=true): 2개
-- 2. 관심사 예문 (tags && interest_tags): 2개
```

---

## 4. Sentence Generation Algorithm

### 4.1 Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    SENTENCE GENERATION FLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ User Context │    │  Word Card   │    │   Cache?     │       │
│  │              │    │              │    │              │       │
│  │ • Profession │    │ • front_text │    │ context_hash │       │
│  │ • Place      │───▶│ • POS        │───▶│ exists?      │       │
│  │ • Emotion    │    │ • Category   │    │              │       │
│  │ • Weather    │    │              │    │  YES → Return│       │
│  └──────────────┘    └──────────────┘    └──────┬───────┘       │
│                                                  │ NO            │
│                                                  ▼               │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                   TEMPLATE SELECTION                       │  │
│  │                                                            │  │
│  │  SELECT * FROM sentence_templates                          │  │
│  │  WHERE part_of_speech = :word_pos                         │  │
│  │    AND (context_type = 'general'                          │  │
│  │         OR (context_type = 'profession'                   │  │
│  │             AND context_value = :user_profession))        │  │
│  │  ORDER BY priority DESC, RANDOM()                         │  │
│  │  LIMIT 1                                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                  VARIABLE SUBSTITUTION                     │  │
│  │                                                            │  │
│  │  Template: "The {subject} felt {word} after {action}."    │  │
│  │                                                            │  │
│  │  Variables from context_variables:                         │  │
│  │  • {subject} → "developer" (profession=developer)         │  │
│  │  • {word}    → "exhausted" (from card)                    │  │
│  │  • {action}  → "debugging all night" (profession=dev)     │  │
│  │                                                            │  │
│  │  Result: "The developer felt exhausted after debugging    │  │
│  │           all night."                                      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                      CACHE & RETURN                        │  │
│  │                                                            │  │
│  │  INSERT INTO sentence_cache (card_id, context_hash, ...)  │  │
│  │  RETURN generated_sentence                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Pseudocode

```python
def generate_contextual_sentence(card_id: str, user_context: dict) -> dict:
    """
    Generate a contextual sentence for a word card.

    Args:
        card_id: UUID of the card
        user_context: {
            'profession': 'developer',
            'place': 'home',
            'emotion': 'tired',
            'environment': 'rainy'
        }

    Returns:
        {
            'sentence_en': '...',
            'sentence_ko': '...',
            'source': 'cache' | 'template' | 'llm'
        }
    """

    # 1. Generate context hash for cache lookup
    context_hash = md5(json.dumps(sorted(user_context.items())))

    # 2. Check cache
    cached = db.query("""
        SELECT sentence_en, sentence_ko
        FROM sentence_cache
        WHERE card_id = :card_id AND context_hash = :hash
    """, card_id=card_id, hash=context_hash)

    if cached:
        return {**cached, 'source': 'cache'}

    # 3. Get card info
    card = db.query("SELECT * FROM cards WHERE id = :id", id=card_id)

    # 4. Select best matching template
    template = db.query("""
        SELECT * FROM sentence_templates
        WHERE part_of_speech = :pos
          AND (
            context_type = 'general'
            OR (context_type = 'profession' AND context_value = :profession)
            OR (context_type = 'place' AND context_value = :place)
            OR (context_type = 'emotion' AND context_value = :emotion)
          )
        ORDER BY
          CASE WHEN context_value = :profession THEN 3
               WHEN context_value = :place THEN 2
               WHEN context_value = :emotion THEN 1
               ELSE 0 END DESC,
          priority DESC,
          RANDOM()
        LIMIT 1
    """, pos=card.part_of_speech, **user_context)

    # 5. Get context variables
    variables = db.query("""
        SELECT placeholder, value_en, value_ko
        FROM context_variables
        WHERE (context_type = 'profession' AND context_value = :profession)
           OR (context_type = 'place' AND context_value = :place)
           OR (context_type = 'emotion' AND context_value = :emotion)
    """, **user_context)

    # 6. Build replacement map
    replacements = {v.placeholder: v for v in variables}
    replacements['{word}'] = {'value_en': card.front_text, 'value_ko': card.back_text}

    # 7. Generate sentence
    sentence_en = template.template_en
    sentence_ko = template.template_ko

    for placeholder, values in replacements.items():
        sentence_en = sentence_en.replace(placeholder, values['value_en'])
        sentence_ko = sentence_ko.replace(placeholder, values['value_ko'])

    # 8. Cache result
    db.execute("""
        INSERT INTO sentence_cache (card_id, context_hash, sentence_en, sentence_ko, template_id)
        VALUES (:card_id, :hash, :en, :ko, :template_id)
    """, card_id=card_id, hash=context_hash, en=sentence_en, ko=sentence_ko,
        template_id=template.id)

    return {
        'sentence_en': sentence_en,
        'sentence_ko': sentence_ko,
        'source': 'template'
    }
```

---

## 5. Data Examples

### 5.1 Sentence Templates

| POS | Context Type | Context Value | Template EN | Template KO |
|-----|--------------|---------------|-------------|-------------|
| adjective | general | - | The situation was {word}. | 상황이 {word}였다. |
| adjective | profession | developer | After {action}, the code review was {word}. | {action} 후, 코드 리뷰가 {word}였다. |
| adjective | emotion | tired | Feeling {word}, I wanted to rest. | {word} 기분이 들어 쉬고 싶었다. |
| verb | general | - | I tried to {word} the problem. | 문제를 {word}하려고 노력했다. |
| verb | profession | developer | The team needed to {word} the bug. | 팀은 버그를 {word}해야 했다. |
| noun | general | - | The {word} was unexpected. | {word}은(는) 예상치 못했다. |

### 5.2 Context Variables

| Placeholder | Context Type | Context Value | Value EN | Value KO |
|-------------|--------------|---------------|----------|----------|
| {subject} | profession | developer | the developer | 개발자 |
| {action} | profession | developer | debugging the server | 서버 디버깅 |
| {action} | profession | developer | reviewing pull requests | PR 리뷰 |
| {place} | place | home | at home | 집에서 |
| {place} | place | commute | on the subway | 지하철에서 |
| {time} | emotion | tired | after a long day | 긴 하루 끝에 |
| {weather} | environment | rainy | on a rainy day | 비 오는 날 |

### 5.3 Profession Vocabulary

```json
{
  "profession": "developer",
  "profession_ko": "개발자",
  "subjects": ["the developer", "my colleague", "the tech lead", "our team"],
  "objects": ["the code", "the bug", "the API", "the database", "the feature"],
  "actions": ["debugging", "deploying", "code reviewing", "refactoring", "testing"],
  "places": ["at the office", "in a standup", "during code review", "at my desk"],
  "scenarios": [
    "after a long debugging session",
    "during the sprint review",
    "before the release deadline",
    "while pair programming"
  ]
}
```

---

## 6. Hybrid Approach: Template + LLM

### When to use Template:
- Simple, common combinations
- Fast response needed
- Predictable quality

### When to use LLM:
- Complex context combinations
- No matching template
- Higher quality needed
- First-time generation (then cache)

```python
def generate_with_fallback(card_id, user_context):
    # Try template first
    result = generate_from_template(card_id, user_context)

    if result and result['quality_score'] > 0.7:
        return result

    # Fallback to LLM
    return generate_with_llm(card_id, user_context)

def generate_with_llm(card_id, user_context):
    prompt = f"""
    Generate a natural example sentence for the word "{card.front_text}" ({card.back_text}).

    Context:
    - User's profession: {user_context['profession']}
    - Current place: {user_context['place']}
    - Current mood: {user_context['emotion']}
    - Weather: {user_context['environment']}

    Requirements:
    - Make the sentence relatable to a {user_context['profession']}
    - Reference the {user_context['place']} setting naturally
    - Keep it concise (10-15 words)
    - Provide both English and Korean
    """

    response = llm.generate(prompt)

    # Cache the result
    cache_sentence(card_id, user_context, response)

    return response
```

---

## 7. Performance Optimization

### 7.1 Pre-generation Strategy

```python
# Pre-generate common combinations during off-peak hours
COMMON_PROFESSIONS = ['developer', 'designer', 'student', 'teacher', 'marketer']
COMMON_PLACES = ['home', 'work', 'commute']
COMMON_EMOTIONS = ['happy', 'tired', 'stressed']

async def pre_generate_common_sentences():
    cards = get_all_cards()

    for card in cards:
        for profession in COMMON_PROFESSIONS:
            for place in COMMON_PLACES:
                context = {'profession': profession, 'place': place, 'emotion': 'neutral'}
                await generate_contextual_sentence(card.id, context)
```

### 7.2 Cache Hit Rate Target

```
Target: 80%+ cache hit rate

Strategy:
1. Pre-generate top 5 profession × top 3 place combinations
2. Lazy generate emotion/environment combinations
3. LRU eviction for rarely used combinations
```

---

## 8. API Design

### Endpoint: Get Contextual Sentence

```
GET /api/v1/cards/{card_id}/sentence

Query Parameters:
- profession: string (optional)
- place: string (optional)
- emotion: string (optional)
- environment: string (optional)

Response:
{
  "card_id": "uuid",
  "word": "exhausted",
  "meaning": "녹초가 된",
  "sentence": {
    "en": "After debugging the server issue all night, the developer felt exhausted.",
    "ko": "밤새 서버 문제를 디버깅한 후, 개발자는 녹초가 되었다."
  },
  "context": {
    "profession": "developer",
    "place": "work",
    "matched_template": "profession_specific"
  },
  "source": "cache" | "template" | "llm"
}
```

---

## 9. Migration Plan

### Phase 1: Schema Setup
1. Add columns to cards table (part_of_speech, semantic_category)
2. Create new tables (sentence_templates, context_variables, etc.)
3. Populate initial template data

### Phase 2: Data Enrichment
1. Classify existing cards by part of speech (can use LLM)
2. Create profession vocabulary pools
3. Generate initial context variables

### Phase 3: Algorithm Implementation
1. Implement template-based generation
2. Add caching layer
3. Integrate LLM fallback

### Phase 4: Pre-generation
1. Pre-generate common combinations
2. Monitor cache hit rate
3. Optimize based on usage patterns

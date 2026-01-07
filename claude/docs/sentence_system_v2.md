# Card Sentence System v2 (Simplified)

## 1. Overview

### 기존 접근 (v1) - 폐기
- 동적 템플릿 조합
- 런타임 문장 생성
- 문제: 문장이 어색해질 가능성 높음

### 새로운 접근 (v2)
- **배치 프로세스**로 예문 사전 생성 (LLM 활용)
- **검수 완료된 예문**만 제공
- 런타임에는 **단순 조회**만

---

## 2. Database Schema

### 2.1 card_sentences (핵심 테이블)

```sql
card_sentences
├── id: uuid (PK)
├── card_id: uuid (FK → cards)
├── word: text (빠른 조회용)
│
├── sentence_en: text  -- "Babe Ruth's swing was simply {word}."
├── sentence_ko: text  -- "베이브 루스의 스윙은 정말 {word}."
│
├── tags: text[]       -- ['baseball', 'sports', 'mlb']
├── is_default: bool   -- true = 기본 예문
├── difficulty: text   -- beginner, intermediate, advanced
│
├── is_verified: bool  -- 검수 완료 여부
├── source: text       -- llm, manual, imported
└── created_at, updated_at
```

### 2.2 meta_interests (기존 테이블 확장)

```sql
meta_interests (기존 테이블)
├── id: uuid (PK)
├── code: text           -- "baseball"
├── label_en: text       -- "Baseball"
├── label_ko: text       -- "야구"
├── related_tags: text[] -- ['baseball', 'sports', 'mlb', 'kbo'] (새로 추가)
└── ...

profiles (기존 테이블)
├── id: uuid (PK)
├── user_id: uuid
├── interest_ids: uuid[] -- meta_interests.id 배열
├── learning_level: text -- 'beginner', 'intermediate', 'advanced' (새로 추가)
├── sentence_count: int  -- 카드당 예문 수 (새로 추가)
└── ...
```

---

## 3. Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    BATCH PROCESS (오프라인)                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. cards 테이블에서 단어 목록 조회                            │
│         ↓                                                   │
│  2. LLM으로 예문 생성                                        │
│     • 기본 예문 2-3개 (is_default = true)                    │
│     • 관심사별 예문 각 2개 (tags = ['baseball', ...])         │
│         ↓                                                   │
│  3. card_sentences 테이블에 저장                             │
│         ↓                                                   │
│  4. 검수 후 is_verified = true                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    RUNTIME (앱에서 조회)                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 사용자 관심사 조회 (profiles.interest_ids)                │
│     → meta_interests JOIN → related_tags 수집               │
│     baseball → ['baseball', 'sports', 'mlb', 'kbo']         │
│     soccer → ['soccer', 'football', 'sports', ...]          │
│         ↓                                                   │
│  2. get_card_sentences() 호출                               │
│     • 50% 기본 예문 (is_default = true)                     │
│     • 50% 매칭 예문 (tags && user_tags)                     │
│         ↓                                                   │
│  3. 앱에 예문 표시                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Example Data

### 단어: "exhausted" (녹초가 된)

#### 기본 예문 (is_default = true)

| sentence_en | sentence_ko | tags |
|-------------|-------------|------|
| The situation left everyone exhausted. | 그 상황은 모든 사람을 녹초로 만들었다. | [] |
| I felt exhausted after the long meeting. | 긴 회의 후 녹초가 되었다. | [] |

#### 관심사별 예문 (is_default = false)

| sentence_en | sentence_ko | tags |
|-------------|-------------|------|
| The pitcher looked exhausted in the 9th inning. | 9회에 투수가 녹초가 된 것 같았다. | ['baseball', 'sports'] |
| Son Heung-min seemed exhausted after the match. | 경기 후 손흥민이 녹초가 된 것 같았다. | ['soccer', 'sports'] |
| Faker looked exhausted after the 5-game series. | 5세트 시리즈 후 페이커가 녹초가 된 것 같았다. | ['gaming', 'esports'] |
| Gordon Ramsay was exhausted after the dinner service. | 디너 서비스 후 고든 램지가 녹초가 되었다. | ['cooking', 'food'] |

---

## 5. Query Examples

### 기본 조회 (SQL)

```sql
-- 1. 사용자 관심사 태그 수집
WITH user_interests AS (
    SELECT unnest(related_tags) as tag
    FROM profiles p
    JOIN meta_interests mi ON mi.id = ANY(p.interest_ids)
    WHERE p.user_id = 'current-user-id'
)
SELECT array_agg(DISTINCT tag) as user_tags FROM user_interests;

-- 결과: ['baseball', 'sports', 'mlb', 'kbo', 'soccer', 'football', ...]

-- 2. 예문 조회
SELECT * FROM get_card_sentences(
    p_card_id := 'uuid-here',
    p_user_tags := ARRAY['baseball', 'sports', 'mlb', 'kbo'],
    p_limit := 2
);

-- 결과:
-- 1. "I felt exhausted after the long meeting." (default)
-- 2. "The pitcher looked exhausted in the 9th inning." (matched: baseball)
```

### Flutter에서 호출

```dart
Future<List<String>> getUserInterestTags(String userId) async {
  // profiles → meta_interests JOIN → related_tags 수집
  final result = await supabase.rpc('get_user_interest_tags', params: {
    'p_user_id': userId,
  });

  return List<String>.from(result ?? []);
}

Future<List<CardSentence>> getSentences(String cardId, String userId) async {
  // 사용자 관심사 태그 가져오기
  final userTags = await getUserInterestTags(userId);

  final response = await supabase.rpc('get_card_sentences', params: {
    'p_card_id': cardId,
    'p_user_tags': userTags,
    'p_limit': 2,
  });

  return response.map((e) => CardSentence.fromJson(e)).toList();
}
```

---

## 6. Batch Generation Script

### 사용법

```bash
# 특정 단어
python generate_sentences_batch.py --word "exhausted"

# 특정 덱
python generate_sentences_batch.py --deck-id "uuid" --limit 50

# 전체 (제한 100개)
python generate_sentences_batch.py --all --limit 100

# 특정 관심사만
python generate_sentences_batch.py --all --interests baseball soccer gaming
```

### 출력 예시

```
[1/100] Processing: exhausted (녹초가 된)
  + Default sentences: 2
  + baseball sentences: 2
  + soccer sentences: 2
  + gaming sentences: 2
  + cooking sentences: 2

Total sentences generated: 10
```

---

## 7. Seed Related Tags

### 사용법

```bash
# meta_interests 테이블에 related_tags 데이터 추가
python scripts/seed_interest_tags.py
```

### 출력 예시

```
============================================================
Seeding Related Tags for meta_interests
============================================================

Found 15 interests in database

✓  baseball              → ['baseball', 'sports', 'mlb', 'kbo']
✓  soccer                → ['soccer', 'football', 'sports', 'premier_league']
✓  music                 → ['music', 'concert', 'album', 'kpop']
⏭  gaming                - Already has tags: ['gaming', 'esports']
⚠  hiking                - No mapping found (please add to INTEREST_TAG_MAPPING)

============================================================
Results:
  Updated: 10
  Skipped (already has tags): 3
  Not found in mapping: 2
============================================================
```

---

## 8. Files

| 파일 | 설명 |
|------|------|
| `migrations/003_card_sentences_simple.sql` | DB 스키마 및 헬퍼 함수 |
| `scripts/generate_sentences_batch.py` | 배치 예문 생성 스크립트 |
| `scripts/seed_interest_tags.py` | meta_interests.related_tags 시드 스크립트 |

---

## 9. 장점

1. **품질 보장**: 사전 생성 + 검수
2. **단순한 구조**: 복잡한 템플릿 로직 없음
3. **빠른 조회**: 런타임에 단순 SELECT
4. **확장 용이**: 새로운 관심사 = 새로운 태그 + 예문 추가
5. **LLM 활용**: 자연스러운 예문 대량 생성

# VibeVoca 테스트 가이드

Supabase RPC Function 및 Python 스크립트 단위 테스트 가이드입니다.

## 환경 설정

### 1. 의존성 설치

```bash
cd claude
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경 변수 확인

프로젝트 루트의 `.env` 파일에 다음 변수가 설정되어 있는지 확인:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 단위 테스트 실행

### get_vibe_sentences_for_deck RPC Function 테스트

**테스트 파일**: `claude/scripts/test_get_vibe_sentences_for_deck.py`

**실행 방법**:

```bash
cd claude
source venv/bin/activate
pytest scripts/test_get_vibe_sentences_for_deck.py -v
```

**테스트 케이스**:

1. ✅ **태그 매칭 테스트** - 사용자 태그와 일치하는 문장만 반환
2. ✅ **여러 태그 테스트** - 여러 태그 OR 조건으로 작동
3. ✅ **태그 불일치 테스트** - 일치하는 태그 없을 때 빈 배열 반환
4. ✅ **존재하지 않는 데크** - 유효하지 않은 deck_id로 호출 시 빈 배열
5. ✅ **반환 구조 검증** - card_id, sentence, tags 필드 존재 및 타입 확인
6. ✅ **LIMIT 500 검증** - 최대 500개 제한 확인

**테스트 출력 예시**:

```
🧪 get_vibe_sentences_for_deck RPC Function 단위 테스트
================================================================================
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_returns_matching_tags PASSED
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_with_multiple_tags PASSED
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_with_no_matching_tags PASSED
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_with_nonexistent_deck PASSED
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_returns_correct_structure PASSED
test_get_vibe_sentences_for_deck.py::TestGetVibeSentencesForDeck::test_function_limit_500 PASSED

🧹 테스트 데이터 정리 중...
✅ 테스트 데이터 정리 완료
```

## 테스트 데이터 관리

### 자동 정리 (Fixture)

테스트는 pytest fixture를 사용하여 자동으로 테스트 데이터를 생성하고 정리합니다:

1. **Setup** (테스트 시작 전):
   - 테스트용 category, deck, cards, card_sentences 생성
   - UUID 기반 고유 식별자 사용

2. **Test** (테스트 실행):
   - RPC function 호출 및 결과 검증

3. **Teardown** (테스트 완료 후):
   - 생성된 모든 테스트 데이터 자동 삭제 (역순)

### 수동 정리 (필요 시)

만약 테스트가 중단되어 데이터가 남아있다면:

```sql
-- Supabase SQL Editor에서 실행
DELETE FROM card_sentences WHERE sentence LIKE '%Test%';
DELETE FROM cards WHERE front_text IN ('happy', 'excited', 'calm');
DELETE FROM decks WHERE name = 'Test Deck';
DELETE FROM categories WHERE name = 'Test Category';
```

## 테스트 작성 가이드

### 새로운 RPC Function 테스트 작성 시:

1. **테스트 파일 생성**: `claude/scripts/test_<function_name>.py`

2. **기본 구조**:

```python
import pytest
from config.supabase_config import get_supabase_client

class TestYourFunction:
    @pytest.fixture(scope="function")
    def supabase_client(self):
        return get_supabase_client()

    @pytest.fixture(scope="function")
    def test_data(self, supabase_client):
        # Setup: 테스트 데이터 생성
        yield data
        # Teardown: 테스트 데이터 정리

    def test_case_1(self, supabase_client, test_data):
        # 테스트 로직
        assert condition, "error message"
```

3. **문서화**: `claude/docs/testing_guide.md` 업데이트

## 주의사항

### 프로덕션 데이터 보호

- 테스트는 **실제 Supabase 데이터베이스**에서 실행됩니다
- 테스트 데이터는 고유 UUID를 사용하여 프로덕션 데이터와 분리
- Fixture의 teardown이 항상 실행되도록 `try-finally` 사용

### 태그 검색 로직 (&&) 이해

Supabase의 `&&` 연산자는 배열 간 **overlap (겹침)** 을 체크합니다:

```sql
-- cs.tags && p_user_tags
-- 예: cs.tags = ['cafe', 'positive']
--     p_user_tags = ['cafe', 'home']
-- 결과: TRUE (cafe가 겹침)
```

### 랜덤 정렬

Function은 `ORDER BY random()`을 사용하므로 동일한 조건으로 호출해도 순서가 다를 수 있습니다.

## CI/CD 통합 (향후)

향후 GitHub Actions 또는 CI/CD 파이프라인 추가 시:

```yaml
# .github/workflows/test.yml
- name: Run Supabase RPC Tests
  run: |
    cd claude
    source venv/bin/activate
    pytest scripts/ -v
```

## 트러블슈팅

### pytest를 찾을 수 없음

```bash
pip install pytest>=8.0.0
```

### Supabase 연결 오류

`.env` 파일 확인:
```bash
cat ../.env | grep SUPABASE
```

### RPC function이 존재하지 않음

`database/vibe_sentences_rpc.sql`을 Supabase SQL Editor에서 실행했는지 확인

---

**작성일**: 2026-01-03
**작성자**: AI Assistant (Claude)
**관련 파일**:
- `claude/scripts/test_get_vibe_sentences_for_deck.py`
- `database/vibe_sentences_rpc.sql`
- `claude/config/supabase_config.py`

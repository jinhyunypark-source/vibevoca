---
name: vibevoca-workflow
description: VibeVoca 프로젝트 작업 가이드. 작업 이력 기록 및 개발 워크플로우 규칙
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# VibeVoca 프로젝트 작업 가이드

VibeVoca는 AI 기반 영어 어휘 학습 앱입니다. 이 스킬은 프로젝트의 작업 방법과 규칙을 정의합니다.

## 프로젝트 구조

```
vibevoca/
├── lib/                    # Flutter 앱 코드
├── claude/                 # 🎯 AI 작업 및 이력 관리 디렉토리
│   ├── docs/              # 작업 문서 및 아키텍처 문서
│   ├── scripts/           # Python 스크립트 (단어 관리, AI 생성)
│   ├── prompts/           # AI 프롬프트 템플릿
│   ├── config/            # Supabase 등 설정
│   ├── migrations/        # 데이터베이스 마이그레이션
│   └── README.md          # 전체 시스템 개요
├── database/              # Supabase 스키마 정의
├── .claude/               # Claude Code 설정 (스킬, 명령어)
└── .env                   # 환경 변수
```

## 🎯 핵심 작업 규칙

### 1. 작업 이력 기록 위치

**모든 작업 이력과 문서는 `claude/` 디렉토리에 기록합니다.**

- **새 기능 설계/아키텍처**: `claude/docs/` 에 마크다운 문서로 작성
  - 예: `claude/docs/contextual_sentence_architecture.md`
  - 예: `claude/docs/sentence_system_v2.md`

- **Python 스크립트**: `claude/scripts/` 에 작성
  - 예: `claude/scripts/word_manager.py` (단어 CRUD)
  - 예: `claude/scripts/ai_generator.py` (AI 컨텐츠 생성)

- **AI 프롬프트**: `claude/prompts/` 에 작성
  - 예: `claude/prompts/word_prompts.md`

- **데이터베이스 변경**: `claude/migrations/` 에 기록
  - 마이그레이션 스크립트 또는 변경 내역 문서

### 2. 데이터베이스 규칙

- **DB 시스템**: Supabase (외부 호스팅)
- **연결 정보**: `.env` 파일에 `SUPABASE_URL`, `SUPABASE_KEY` 저장
- **DB 설정 코드**: `claude/config/supabase_config.py`
- **주요 테이블**:
  - `cards`: 단어 카드 (front_text, back_text, example_sentences, audio_url)
  - `decks`: 단어 데크 모음
  - `categories`: 카테고리
  - `contexts`: 컨텍스트 정보 (place, emotion, environment)

### 3. 개발 워크플로우

#### 새 기능 개발 시:

1. **문서 작성**: `claude/docs/` 에 아키텍처/설계 문서 작성
2. **스크립트 구현**: 필요 시 `claude/scripts/` 에 Python 도구 작성
3. **Flutter 구현**: `lib/` 에서 앱 코드 작성
4. **DB 변경**: `database/` 또는 `claude/migrations/` 에 스키마 변경 기록

#### 작업 이력 업데이트:

- 새로운 작업을 시작할 때마다 `claude/docs/` 에 문서로 기록
- 작업 완료 후 `claude/README.md` 업데이트 (필요 시)
- 중요한 의사결정이나 아키텍처 변경은 반드시 문서화

### 4. Python 스크립트 사용

```bash
# 가상환경 활성화
cd claude
source venv/bin/activate

# 단어 관리
python scripts/word_manager.py list-categories
python scripts/word_manager.py add-word <deck_id> --word "..." --meaning "..."

# AI 생성
python scripts/ai_generator.py generate-words <deck_id> --count 5
```

### 5. Python 스크립트 작성 표준

**모든 Python 스크립트는 다음 표준을 따릅니다:**

#### 📋 필수 구조

```python
#!/usr/bin/env python3
"""
스크립트 설명 (한 줄)

상세 설명 및 사용 예시:
    python script_name.py --option1 value1
    python script_name.py --help
"""

import sys
import os
import argparse

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.supabase_config import get_supabase_client


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description='스크립트 설명',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='사용 예시 및 추가 설명'
    )

    # 인자 정의
    parser.add_argument('--option', help='옵션 설명')

    # 인자 없이 실행 시 사용법 출력
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # 실제 로직 구현
    # ...


if __name__ == '__main__':
    main()
```

#### ✅ 작성 규칙

1. **CLI 인터페이스 (필수)**
   - `argparse`를 사용한 명령줄 인자 처리
   - 인자 없이 실행 시 자동으로 사용법 표시
   - `-h`, `--help` 옵션 제공

2. **사용자 친화적 옵션**
   - `--list-*`: 관련 정보 목록 출력 (예: `--list-decks`, `--list-tags`)
   - `-v`, `--verbose`: 상세 출력 모드
   - 짧은 옵션 (`-d`) + 긴 옵션 (`--deck`) 병행 제공

3. **자동화된 처리**
   - 사용자가 이름만 입력하면 ID 자동 조회
   - 부분 일치 검색 지원
   - 대소문자 무시 검색

4. **친절한 에러 메시지**
   - 에러 발생 시 원인 설명
   - 해결 방법 제시
   - 관련 명령어 안내

5. **시각적 출력**
   - 이모지 사용으로 가독성 향상
   - `=` 또는 `-`로 섹션 구분
   - 단계별 진행 상황 표시 (Step 1, Step 2...)

6. **문서화**
   - Docstring 필수 (모듈, 함수)
   - 사용 예시 포함
   - 주요 기능 설명

#### 📌 예시: 표준을 따르는 스크립트

```python
#!/usr/bin/env python3
"""
get_vibe_sentences_for_deck RPC Function 테스트 스크립트

사용 예시:
    python test_vibe_sentences.py --deck LOGIC_CLARITY --tags home
    python test_vibe_sentences.py --list-decks
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description='Vibe Sentences 테스트')
    parser.add_argument('-d', '--deck', help='데크 이름')
    parser.add_argument('-t', '--tags', nargs='+', help='태그 리스트')
    parser.add_argument('--list-decks', action='store_true', help='데크 목록')
    parser.add_argument('-v', '--verbose', action='store_true', help='상세 모드')

    if len(sys.argv) == 1:
        print_usage()  # 사용법 출력 함수
        sys.exit(0)

    args = parser.parse_args()
    # ... 구현
```

#### 🎯 주요 패턴

**패턴 1: 이름으로 ID 자동 조회**

```python
def find_deck_by_name(client, deck_name):
    """데크 이름으로 데크 정보 조회 (정확 일치 → 대소문자 무시 → 부분 일치)"""
    # 1. 정확한 일치
    response = client.table('decks').select('*').eq('title', deck_name).execute()
    if response.data:
        return response.data[0]

    # 2. 대소문자 무시
    response = client.table('decks').select('*').ilike('title', deck_name).execute()
    if response.data:
        return response.data[0]

    # 3. 부분 일치
    response = client.table('decks').select('*').ilike('title', f'%{deck_name}%').execute()
    if response.data:
        return response.data[0]

    return None
```

**패턴 2: 리스트 출력 옵션**

```python
def list_all_items(client):
    """사용 가능한 항목 목록 출력"""
    print("\n📋 사용 가능한 항목:")
    print("=" * 80)

    response = client.table('items').select('*').order('name', desc=False).execute()

    for i, item in enumerate(response.data, 1):
        print(f"{i:<5} {item['name']:<30}")

    print(f"\n총 {len(response.data)}개")
```

**패턴 3: Verbose 모드**

```python
def process(verbose=False):
    """처리 로직"""
    if verbose:
        print(f"📌 상세 정보: ...")

    # 핵심 출력은 항상 표시
    print(f"✅ 완료!")
```

#### 🔧 테스트 스크립트 특별 규칙

테스트 스크립트 (`test_*.py`)는 추가로:

1. **단계별 출력**: Step 1, Step 2 형식
2. **결과 검증**: ✅ 성공, ⚠️ 경고, ❌ 실패
3. **매칭 확인**: 예상 결과와 실제 결과 비교
4. **테스트 완료 표시**: 🏁 테스트 완료

#### 📚 참고 파일

- 표준 적용 예시: `claude/scripts/test_vibe_sentences.py`
- 기존 스크립트: `claude/scripts/word_manager.py`, `claude/scripts/ai_generator.py`

### 6. 환경 변수

프로젝트 루트의 `.env` 파일에 다음이 설정되어 있습니다:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

## 작업 체크리스트

새 작업을 시작할 때 다음을 확인하세요:

- [ ] 관련 문서를 `claude/docs/` 에서 확인했는가?
- [ ] 데이터베이스 스키마 (`database/` 또는 `claude/config/`) 를 이해했는가?
- [ ] 새로운 아키텍처 변경 시 `claude/docs/` 에 문서를 작성했는가?
- [ ] Python 스크립트 필요 시 `claude/scripts/` 에 작성했는가?
- [ ] 작업 완료 후 관련 문서를 업데이트했는가?

## 주요 디렉토리별 역할

| 디렉토리 | 용도 | 예시 |
|---------|------|------|
| `claude/docs/` | 작업 이력, 아키텍처 문서 | `contextual_sentence_architecture.md` |
| `claude/scripts/` | 데이터 관리 Python 스크립트 | `word_manager.py`, `ai_generator.py` |
| `claude/prompts/` | AI 프롬프트 템플릿 | `word_prompts.md` |
| `claude/config/` | DB 연결 등 설정 | `supabase_config.py` |
| `claude/migrations/` | DB 마이그레이션 이력 | SQL 또는 마이그레이션 문서 |
| `lib/` | Flutter 앱 코드 | Dart 파일들 |
| `database/` | Supabase 스키마 정의 | SQL 스키마 파일 |

## 도움말

- 전체 시스템 이해: `claude/README.md` 읽기
- 기존 작업 확인: `claude/docs/` 내 마크다운 파일 검토
- 단어 관리 방법: `claude/scripts/word_manager.py --help`
- AI 생성 사용법: `claude/scripts/ai_generator.py --help`

---

**중요**: 모든 작업 이력과 문서는 `claude/` 디렉토리에 집중 관리됩니다. 새로운 작업을 시작하기 전에 반드시 `claude/docs/` 를 확인하세요.

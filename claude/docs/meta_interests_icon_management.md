# meta_interests 아이콘 관리 가이드

## 개요

`meta_interests` 테이블은 사용자 프로필에서 선택할 수 있는 직업, 취미, 관심사 메타데이터를 저장합니다. 각 항목은 Material Icon으로 시각화되며, 이 문서는 아이콘 관리 방법을 설명합니다.

## 테이블 구조

```sql
CREATE TABLE meta_interests (
    id UUID PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,           -- 고유 식별자 (예: 'soccer', 'developer')
    label_en TEXT NOT NULL,              -- 영어 레이블 (예: 'Soccer', 'Developer')
    label_ko TEXT NOT NULL,              -- 한국어 레이블 (예: '축구', '개발자')
    icon TEXT,                           -- Material Icon 이름 (예: 'sports_soccer')
    category TEXT DEFAULT 'job',         -- 'job', 'hobby', 'vibe'
    tags TEXT[] DEFAULT '{}',            -- 검색/추천용 태그 배열
    order_index INT DEFAULT 0,           -- 정렬 순서
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Material Icons 선택 가이드

### 1. 아이콘 검색

Material Icons 공식 사이트에서 적절한 아이콘을 검색합니다:
- https://fonts.google.com/icons

### 2. 명명 규칙

- Flutter/Material Design에서는 **스네이크 케이스** 사용
- 예시:
  - ✅ `sports_soccer` (올바름)
  - ❌ `sportsSoccer` (잘못됨)
  - ❌ `sports-soccer` (잘못됨)

### 3. 카테고리별 권장 아이콘

#### Hobby (취미)

| Code | Label (KO) | Icon | 설명 |
|------|-----------|------|------|
| soccer | 축구 | `sports_soccer` | 축구공 아이콘 |
| travel | 여행 | `flight` | 비행기 아이콘 |
| movie | 영화 | `movie` | 영화 필름 아이콘 |
| food | 음식/맛집 | `restaurant` | 레스토랑 아이콘 |
| health | 건강 | `favorite` | 하트 아이콘 |
| social | 소셜/사교 | `groups` | 사람들 아이콘 |
| learning | 학습/공부 | `school` | 학교 아이콘 |
| technology | IT/기술 | `computer` | 컴퓨터 아이콘 |

#### Job (직업)

| Code | Label (KO) | Icon | 설명 |
|------|-----------|------|------|
| student | 학생 | `school` | 졸업모 아이콘 |
| developer | 개발자 | `code` | 코드 아이콘 |
| business | 직장인 | `business_center` | 서류가방 아이콘 |
| designer | 디자이너 | `palette` | 팔레트 아이콘 |
| teacher | 교사 | `school` | 학교 아이콘 |
| medical | 의료인 | `medical_services` | 의료 아이콘 |

## 아이콘 업데이트 방법

### 방법 1: Python 스크립트 (권장)

#### 준비

```bash
cd /path/to/vibevoca
source claude/venv/bin/activate
```

#### 단일 업데이트

```python
#!/usr/bin/env python3
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv('.env')

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
client = create_client(url, key)

# 단일 아이콘 업데이트
client.table('meta_interests').update({
    'icon': 'sports_soccer'
}).eq('code', 'soccer').execute()

print("✅ 아이콘 업데이트 완료")
```

#### 배치 업데이트

`database/update_icons.py` 스크립트 사용:

```python
#!/usr/bin/env python3
"""
meta_interests 아이콘 배치 업데이트

사용 예시:
    python database/update_icons.py
"""
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv('.env')

# 업데이트할 아이콘 목록
ICON_UPDATES = {
    'soccer': 'sports_soccer',
    'travel': 'flight',
    'developer': 'code',
    'student': 'school',
    'movie': 'movie',
    'health': 'favorite',
}

def update_icons():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    client = create_client(url, key)

    print("\n" + "="*80)
    print("Updating meta_interests icons...")
    print("="*80 + "\n")

    updated_count = 0
    for code, icon in ICON_UPDATES.items():
        try:
            client.table('meta_interests').update({
                'icon': icon
            }).eq('code', code).execute()
            print(f"✓ Updated {code:20} -> icon: {icon}")
            updated_count += 1
        except Exception as e:
            print(f"✗ Failed to update {code}: {e}")

    print(f"\n✅ Updated {updated_count} icons")

if __name__ == "__main__":
    update_icons()
```

실행:

```bash
python database/update_icons.py
```

### 방법 2: SQL 직접 실행

Supabase Dashboard의 SQL Editor에서:

```sql
-- 단일 업데이트
UPDATE meta_interests
SET icon = 'sports_soccer'
WHERE code = 'soccer';

-- 배치 업데이트
UPDATE meta_interests SET icon = 'sports_soccer' WHERE code = 'soccer';
UPDATE meta_interests SET icon = 'flight' WHERE code = 'travel';
UPDATE meta_interests SET icon = 'code' WHERE code = 'developer';
UPDATE meta_interests SET icon = 'school' WHERE code = 'student';

-- 결과 확인
SELECT code, label_ko, icon, category
FROM meta_interests
ORDER BY category, order_index;
```

## 문제 해결

### 문제 1: 아이콘이 중복으로 표시됨

**증상**: 여러 항목이 같은 아이콘(예: 삼각형+원)으로 표시됨

**원인**:
- 아이콘 이름이 잘못 입력됨 (예: `groups` 대신 `group`)
- 아이콘 이름이 null이거나 빈 문자열
- Material Icons에 존재하지 않는 이름 사용

**해결**:
1. 현재 아이콘 상태 확인:
   ```sql
   SELECT code, label_ko, icon
   FROM meta_interests
   WHERE icon IS NULL OR icon = '';
   ```

2. 올바른 아이콘으로 업데이트:
   ```bash
   python database/update_icons.py
   ```

### 문제 2: 환경 변수 로딩 오류

**증상**: `ValueError: SUPABASE_URL 또는 SUPABASE_KEY가 설정되지 않았습니다.`

**원인**: `.env` 파일이 올바르게 로드되지 않음

**해결**:

```python
# 올바른 .env 로딩
from dotenv import load_dotenv
import os

# 프로젝트 루트의 .env 파일 명시적으로 로드
load_dotenv('/path/to/vibevoca/.env')

# 또는 상대 경로 사용
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
```

### 문제 3: 권한 오류

**증상**: `Permission denied` 또는 `RLS policy violation`

**원인**: `ANON_KEY`로 관리자 작업 시도

**해결**: `SERVICE_ROLE_KEY` 사용

```python
# ❌ 잘못된 방법
key = os.getenv("SUPABASE_ANON_KEY")

# ✅ 올바른 방법
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
```

## Flutter에서 아이콘 사용 (개선된 방식)

### ✨ 이제 한 곳만 수정!

**2026-01-09 개선**: 하드코딩된 switch문 제거, 동적 아이콘 매핑 도입

meta_interests 아이콘을 변경할 때 **`MaterialIconsMapper` 한 곳만 수정**하면 됩니다!

### MaterialIconsMapper 유틸리티

**파일**: `lib/core/utils/material_icons_mapper.dart`

Material Icons의 CodePoint를 사용하여 동적으로 아이콘을 생성합니다:

```dart
// 사용법
IconData icon = MaterialIconsMapper.getIcon('sports_soccer');
Icon(icon)
```

### 새 아이콘 추가 방법

1. **Material Icons에서 아이콘 선택**:
   - https://fonts.google.com/icons
   - Flutter Icons 클래스에서 이름 확인: `Icons.music_note`

2. **MaterialIconsMapper에 등록**:

```dart
// lib/core/utils/material_icons_mapper.dart
static final Map<String, IconData> _iconMap = {
  // 기존 아이콘들...
  'music_note': Icons.music_note,  // ← 새 아이콘 추가 (Icons 클래스 직접 참조)
};
```

3. **데이터베이스에 아이콘 이름 저장**:

```sql
UPDATE meta_interests SET icon = 'music_note' WHERE code = 'music';
```

4. **끝!** Flutter 앱 재시작하면 자동으로 표시됩니다.

### 장점

- ✅ **단일 소스**: MaterialIconsMapper 한 곳에서 관리
- ✅ **유지보수 용이**: 새 아이콘 추가 시 1줄만 추가
- ✅ **확장성**: 커스텀 폰트도 쉽게 추가
- ✅ **타입 안전**: IconData 타입 보장

### 상세 가이드

자세한 사용법은 다음 문서 참고:
- **새 아이콘 추가 가이드**: `claude/docs/add_new_interest_icon.md`

## 작업 이력

### 2026-01-09: 아이콘 중복 문제 해결

**문제**:
- 사용자 프로필 화면에서 여러 관심사 항목이 같은 아이콘(삼각형+원 조합)으로 표시됨
- 16개 항목 중 대부분이 중복 아이콘 사용

**분석**:
- `meta_interests` 테이블의 `icon` 필드 확인
- 잘못된 아이콘 이름 또는 null 값 발견
- Material Icons 이름 규칙 미준수

**1차 해결 (데이터베이스)**:
1. `database/update_icons.py` 스크립트 작성
2. 각 관심사에 고유한 Material Icon 할당
3. 16개 interest 아이콘 업데이트:
   - Hobby: soccer, social, travel, activity, career, learning, conversation, marketing, health, friendship, movie, technology, medical
   - Job: student, developer, business

**2차 문제 발견**:
- 데이터베이스 업데이트 후에도 아이콘이 여전히 중복으로 표시됨
- 원인: Flutter 코드의 `_getIconData()` 함수에 새 아이콘 이름이 매핑되지 않음
- 데이터베이스의 `sports_soccer`, `groups` 등이 Flutter switch문에 없어서 default case인 `Icons.category`가 표시됨

**2차 해결 (Flutter)**:
1. `lib/features/profile/profile_setup_page.dart` 파일 수정
2. `_getIconData()` 함수에 모든 데이터베이스 아이콘 추가
3. 추가된 아이콘:
   ```dart
   case 'sports_soccer': return Icons.sports_soccer;
   case 'groups': return Icons.groups;
   case 'directions_run': return Icons.directions_run;
   case 'chat': return Icons.chat;
   case 'campaign': return Icons.campaign;
   case 'favorite': return Icons.favorite;
   case 'diversity_1': return Icons.diversity_1;
   case 'movie': return Icons.movie;
   case 'computer': return Icons.computer;
   case 'medical_services': return Icons.medical_services;
   case 'work': return Icons.work;
   ```

**2차 결과**:
- ✅ 데이터베이스: 16개 항목 고유 아이콘 할당
- ✅ Flutter: 모든 아이콘 이름 매핑 완료
- ✅ 사용자 화면에서 각 관심사가 고유한 아이콘으로 표시

**3차 문제 발견**:
- 아이콘 추가 시 데이터베이스와 Flutter 코드 두 곳 모두 수정해야 함
- 하드코딩된 switch문(40줄)이 유지보수 어려움
- 확장성 부족

**3차 해결 (아키텍처 개선)**:
1. `MaterialIconsMapper` 유틸리티 클래스 생성
2. Material Icons CodePoint 기반 동적 매핑
3. 하드코딩된 switch문 완전 제거
4. 단일 소스 원칙 적용

**개선 결과**:
```dart
// Before: 40줄의 하드코딩된 switch문
IconData _getIconData(String? iconName) {
  switch (iconName) {
    case 'sports_soccer': return Icons.sports_soccer;
    // ... 35줄 더
    default: return Icons.category;
  }
}

// After: 1줄로 단순화
Icon(MaterialIconsMapper.getIcon(item.icon))
```

**최종 결과**:
- ✅ 한 곳만 수정: `MaterialIconsMapper._iconMap`
- ✅ 코드 40줄 → 1줄로 감소
- ✅ 확장성 및 유지보수성 대폭 향상
- ✅ 데이터베이스는 아이콘 이름만 저장 (역할 분리)

**핵심 교훈 (최종)**:
✨ **이제 MaterialIconsMapper 한 곳만 관리하면 됩니다!**

**생성/수정 파일**:
- `lib/core/utils/material_icons_mapper.dart` - ⭐ 새로운 아이콘 매핑 유틸리티
- `lib/features/profile/profile_setup_page.dart` - 하드코딩 제거, MaterialIconsMapper 사용
- `claude/docs/add_new_interest_icon.md` - ⭐ 새 아이콘 추가 가이드
- `claude/scripts/update_meta_interests_icons.py` - 아이콘 관리 스크립트
- `database/update_icons.py` - 초기 스크립트 (참고용)
- `claude/docs/meta_interests_icon_management.md` - 이 문서

## 참고 자료

- [Material Icons 공식 사이트](https://fonts.google.com/icons)
- [Flutter Icon 클래스 문서](https://api.flutter.dev/flutter/material/Icons-class.html)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)

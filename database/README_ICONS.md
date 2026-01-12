# meta_interests 아이콘 관리

이 디렉토리에는 Supabase `meta_interests` 테이블의 아이콘 관리 관련 파일들이 있습니다.

## 파일 설명

### update_icons.py (임시 작업 파일)
- **상태**: 작업 완료, 참고용
- **용도**: 2026-01-09 아이콘 중복 문제 해결 시 사용한 초기 스크립트
- **대체**: `claude/scripts/update_meta_interests_icons.py` 사용 권장

### fix_meta_interests_icons.sql (참고용)
- **용도**: SQL로 아이콘 업데이트하는 방법 참고
- **사용**: Supabase SQL Editor에서 직접 실행 가능

### check_meta_interests.py (참고용)
- **용도**: 현재 meta_interests 데이터 확인
- **사용**: 간단한 조회용

## ✨ 새로운 방식 (권장)

**2026-01-09 개선**: 이제 `MaterialIconsMapper` 한 곳만 관리하면 됩니다!

### 새 아이콘 추가

1. **Material Icons에서 CodePoint 확인**:
   - https://fonts.google.com/icons
   - 예: `music_note` → `e3a8`

2. **MaterialIconsMapper에 등록**:
   ```dart
   // lib/core/utils/material_icons_mapper.dart
   'music_note': 0xe3a8,
   ```

3. **데이터베이스 업데이트**:
   ```bash
   python claude/scripts/update_meta_interests_icons.py
   ```

상세 가이드: `claude/docs/add_new_interest_icon.md`

## 기존 스크립트 (참고용)

데이터베이스 아이콘 일괄 업데이트:

```bash
# 가상환경 활성화
cd /path/to/vibevoca
source claude/venv/bin/activate

# 현재 상태 확인
python claude/scripts/update_meta_interests_icons.py --check

# 전체 목록 출력
python claude/scripts/update_meta_interests_icons.py --list

# 아이콘 업데이트 (시뮬레이션)
python claude/scripts/update_meta_interests_icons.py --dry-run

# 실제 업데이트 실행
python claude/scripts/update_meta_interests_icons.py
```

## 상세 가이드

자세한 사용법과 문제 해결 방법은 다음 문서를 참고하세요:

- **상세 가이드**: `claude/docs/meta_interests_icon_management.md`
- **프로젝트 워크플로우**: `.claude/skills/vibevoca-workflow/SKILL.md`

## 작업 이력

- **2026-01-09**: meta_interests 아이콘 중복 문제 해결 (3단계 개선)
  - **1차**: 데이터베이스 아이콘 업데이트 (16개 interest)
  - **2차**: Flutter 코드 아이콘 매핑 수정
    - 문제: 데이터베이스만 업데이트해도 Flutter에서 매핑 누락
    - 해결: `lib/features/profile/profile_setup_page.dart`의 `_getIconData()` 수정
  - **3차**: 아키텍처 개선 ⭐
    - 문제: 하드코딩된 switch문(40줄)으로 유지보수 어려움
    - 해결: `MaterialIconsMapper` 유틸리티 클래스 생성
    - 결과: 코드 40줄 → 1줄, 단일 소스 원칙 적용
  - Material Icons 표준화
  - 스크립트 개선 및 문서화

### ✨ 개선 결과

이제 `MaterialIconsMapper` 한 곳만 관리하면 됩니다!
- ✅ 하드코딩 제거
- ✅ 유지보수 용이
- ✅ 확장성 향상

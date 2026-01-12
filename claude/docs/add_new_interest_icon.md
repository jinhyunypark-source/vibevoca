# 새 관심사 아이콘 추가 가이드

## 개요

새로운 관심사(interest)를 추가하거나 아이콘을 변경할 때, **이제 한 곳만 수정**하면 됩니다!

## ✨ 개선된 아키텍처

### Before (기존 방식)
- ❌ 데이터베이스 업데이트
- ❌ Flutter 코드에서 switch문 수정 (하드코딩)
- ❌ 두 곳을 모두 동기화해야 함

### After (개선된 방식)
- ✅ `MaterialIconsMapper` 유틸리티 한 곳만 수정
- ✅ 데이터베이스는 아이콘 이름만 저장
- ✅ 동적으로 IconData 변환

## 📋 새 아이콘 추가 절차

### 1. Material Icons에서 아이콘 선택

https://fonts.google.com/icons 에서 원하는 아이콘 선택

예: "music_note" 아이콘을 추가한다고 가정

### 2. MaterialIconsMapper에 등록

**파일**: `lib/core/utils/material_icons_mapper.dart`

```dart
static final Map<String, IconData> _iconMap = {
  // 기존 아이콘들...

  // 새로 추가
  'music_note': Icons.music_note,  // ← Icons 클래스 직접 참조
};
```

**주의**: Icons 클래스를 직접 참조하므로 정확한 아이콘 이름만 사용하면 됩니다!

### 3. 데이터베이스에 추가

Python 스크립트 사용:

```python
# claude/scripts/update_meta_interests_icons.py 수정

ICON_UPDATES = {
    # 기존 항목들...

    # 새로 추가
    'music': 'music_note',  # code -> icon name
}
```

또는 직접 SQL:

```sql
INSERT INTO meta_interests (code, label_en, label_ko, icon, category, tags, order_index)
VALUES ('music', 'Music', '음악', 'music_note', 'hobby', ARRAY['music'], 23);
```

### 4. 끝!

Flutter 앱을 재시작하면 자동으로 아이콘이 표시됩니다.

## 🔧 MaterialIconsMapper 상세

### 동작 원리

Material Icons는 Flutter의 Icons 클래스로 제공됩니다. MaterialIconsMapper는 이를 문자열로 매핑합니다.

```dart
// Icons 클래스 직접 참조:
static final _iconMap = {
  'sports_soccer': Icons.sports_soccer,
  'flight': Icons.flight,
};

// MaterialIconsMapper 사용:
MaterialIconsMapper.getIcon('sports_soccer')
// → Icons.sports_soccer 반환
```

### 주요 메서드

```dart
// 아이콘 가져오기
IconData icon = MaterialIconsMapper.getIcon('sports_soccer');

// 아이콘 존재 여부 확인
bool exists = MaterialIconsMapper.hasIcon('sports_soccer');

// 등록된 모든 아이콘 목록
List<String> allIcons = MaterialIconsMapper.getAllIconNames();

// 런타임에 아이콘 추가 (디버깅용)
MaterialIconsMapper.registerIcon('custom_icon', Icons.star);
```

### 에러 처리

매핑되지 않은 아이콘 이름을 요청하면:
- 자동으로 `help_outline` 아이콘 반환
- 디버그 로그 출력: `⚠️ Unknown icon name: xxx`

## 📝 체크리스트

새 아이콘 추가 시:

- [ ] Material Icons에서 아이콘 선택
- [ ] Flutter Icons 클래스에서 아이콘 이름 확인 (예: `Icons.music_note`)
- [ ] `MaterialIconsMapper._iconMap`에 추가
- [ ] 데이터베이스에 아이콘 이름 저장
- [ ] Flutter 앱 재시작 및 테스트

## 🎯 장점

### 1. 단일 소스 원칙 (Single Source of Truth)
- MaterialIconsMapper 한 곳에서 모든 아이콘 관리
- 데이터베이스는 아이콘 '이름'만 저장 (역할 분리)

### 2. 유지보수 용이
- 새 아이콘 추가 시 한 줄만 추가
- switch문 40줄 → Map 1줄

### 3. 확장성
- 커스텀 폰트 아이콘도 쉽게 추가 가능
- 아이콘 별칭(alias) 지원 가능

### 4. 타입 안전성
- IconData 타입 보장
- null 안전성 자동 처리

## 🚀 고급 사용법

### 커스텀 폰트 아이콘 추가

```dart
// 커스텀 폰트 사용
static IconData getCustomIcon(String? iconName) {
  return IconData(
    _iconMap[iconName] ?? _iconMap['help_outline']!,
    fontFamily: 'CustomIcons',  // ← 커스텀 폰트
  );
}
```

### 아이콘 별칭 (Alias) 지원

```dart
static final Map<String, String> _aliases = {
  'football': 'sports_soccer',  // football → sports_soccer
  'code_dev': 'code',           // code_dev → code
};

static IconData getIcon(String? iconName) {
  // 별칭 확인
  final resolvedName = _aliases[iconName] ?? iconName;
  // ...
}
```

## 📚 참고 자료

- [Material Icons 공식 사이트](https://fonts.google.com/icons)
- [Flutter IconData 문서](https://api.flutter.dev/flutter/widgets/IconData-class.html)
- [Material Design Icons](https://material.io/resources/icons/)

## 문제 해결

### Q: 아이콘이 □ (빈 사각형)으로 표시됩니다

**원인**: Icons 클래스의 아이콘 이름이 잘못되었습니다.

**해결**:
1. Flutter의 Icons 클래스에서 아이콘 이름 확인
2. 정확한 아이콘 이름 사용 (예: `Icons.music_note`)
3. 오타 확인

### Q: 아이콘이 help_outline으로 표시됩니다

**원인**: MaterialIconsMapper에 등록되지 않은 아이콘 이름

**해결**:
1. 디버그 로그 확인: `⚠️ Unknown icon name: xxx`
2. MaterialIconsMapper에 아이콘 추가
3. 아이콘 이름 오타 확인

### Q: Hot Reload 후에도 아이콘이 안 바뀝니다

**해결**: MaterialIconsMapper는 static이므로 **전체 재시작** 필요
- Android Studio: Stop 후 Run
- VS Code: Restart
- CLI: `flutter run`

## 마이그레이션 노트

기존 하드코딩된 switch문에서 마이그레이션:

**Before**:
```dart
IconData _getIconData(String? iconName) {
  switch (iconName) {
    case 'sports_soccer': return Icons.sports_soccer;
    case 'flight': return Icons.flight;
    // ... 40줄
    default: return Icons.category;
  }
}
```

**After**:
```dart
// 함수 삭제, import 추가
import 'package:vibevoca/core/utils/material_icons_mapper.dart';

// 사용
Icon(MaterialIconsMapper.getIcon(item.icon))
```

40줄 → 1줄로 단순화!

# 카테고리별 이미지 다운로드 시스템

작성일: 2026-01-13

## 개요

기존 1,568개 단어 이미지를 앱 번들에 모두 포함하던 방식에서, 카테고리 단위로 분리하여 온디맨드 다운로드 방식으로 변경.

### 문제점
- 모든 이미지(~18MB)가 앱에 번들되어 앱 크기 증가
- 단일 폴더에 1,500+ 이미지로 인한 로딩 성능 저하
- 스와이프 시 멈춤 현상 발생

### 해결책
- 데모 카테고리(첫 번째)만 앱에 번들 (~1.75MB, 156개 이미지)
- 나머지 카테고리는 Supabase Storage에서 필요시 다운로드
- 로그인 사용자만 다운로드 가능 (Private Storage)

---

## 구현 내용

### Phase 1: Python 스크립트

| 파일 | 기능 |
|------|------|
| `claude/prepare_category_zips.py` | 카테고리별 ZIP 파일 생성 |
| `claude/upload_to_supabase.py` | Supabase Storage 업로드 |
| `claude/extract_demo_category.py` | 데모 카테고리 이미지 추출 |

**실행 방법:**
```bash
source backend/venv/bin/activate

# 1. 카테고리별 ZIP 생성
python claude/prepare_category_zips.py --create-all

# 2. Supabase Storage 업로드
python claude/upload_to_supabase.py --create-bucket  # 최초 1회
python claude/upload_to_supabase.py --upload-all

# 3. 데모 이미지 추출
python claude/extract_demo_category.py
```

### Phase 2: Flutter 서비스

| 파일 | 기능 |
|------|------|
| `lib/core/services/image_pack_service.dart` | ZIP 다운로드/추출, 로컬 캐시 관리 |
| `lib/core/services/models/download_state.dart` | 다운로드 상태 모델 (Freezed) |

**주요 메서드:**
```dart
// 다운로드 여부 확인
Future<bool> isPackDownloaded(String categoryId);

// 로컬 이미지 경로 조회
Future<String?> getLocalImagePath(String cardId);

// ZIP 다운로드 및 추출
Future<void> downloadPack(String categoryId, {Function(double)? onProgress});

// 팩 삭제
Future<int> deletePack(String categoryId);
```

### Phase 3: Provider 레이어

| 파일 | 기능 |
|------|------|
| `lib/features/context/providers/image_pack_provider.dart` | Riverpod Provider |

**주요 Provider:**
```dart
// 서비스 프로바이더
final imagePackServiceProvider = Provider<ImagePackService>(...);

// 카테고리별 다운로드 상태 (Family)
categoryDownloadStateProvider(categoryId)

// 유틸리티
const demoCategoryId = 'eec83079-d8a3-4516-bf30-fc78977f72cd';
bool isDemoCategory(String categoryId);
```

### Phase 4: FlashCard 이미지 로딩

**이미지 조회 우선순위:**
1. 로컬 캐시 (다운로드된 이미지) → `Image.file()`
2. 번들 에셋 (데모 카테고리) → `Image.asset()`
3. 플레이스홀더 → `GenerativeCardBackground`

**수정된 파일:** `lib/features/battle/widgets/flash_card.dart`

### Phase 5: 다운로드 UI

**수정된 파일:** `lib/features/context/deck_selection_page.dart`

카테고리 헤더에 다운로드 상태 표시:
- ✅ 데모 카테고리/다운로드 완료 → 체크 아이콘
- ☁️ 다운로드 안됨 → 클라우드 다운로드 아이콘 (탭하여 다운로드)
- 🔄 다운로드 중 → 진행률 표시
- ❌ 에러 → 재시도 버튼

**비로그인 사용자:** 로그인 유도 다이얼로그 표시

### Phase 6: pubspec.yaml 변경

```yaml
# Before
assets:
  - assets/word_images/  # 전체 이미지 (~18MB)

# After
assets:
  - assets/word_images_demo/  # 데모 카테고리만 (~1.75MB)
```

---

## 디렉토리 구조

```
assets/
├── word_images/          # 전체 이미지 (1,568개, git에서 제외 가능)
└── word_images_demo/     # 데모 카테고리 이미지 (156개, 번들에 포함)

claude/
├── category_zips/        # 생성된 ZIP 파일
│   ├── {category_id}.zip
│   └── manifest.json
└── scripts/
    ├── prepare_category_zips.py
    ├── upload_to_supabase.py
    └── extract_demo_category.py

lib/
├── core/services/
│   ├── image_pack_service.dart
│   └── models/download_state.dart
└── features/context/providers/
    └── image_pack_provider.dart
```

---

## Supabase Storage 구조

**Bucket:** `category-images` (Private)

**파일:**
```
category-images/
├── manifest.json              # 메타데이터
├── {category_id_1}.zip       # 카테고리 1 이미지
├── {category_id_2}.zip       # 카테고리 2 이미지
└── ...
```

---

## 하위 호환성

- 기존 앱 버전에 영향 없음
- DB 스키마 변경 없음
- 새로운 Storage bucket만 추가

---

## 향후 개선 사항

1. 설정 페이지에서 캐시 용량 확인/삭제 기능
2. 자동 다운로드 옵션 (WiFi 연결 시)
3. 다운로드 재개 기능 (중단된 경우)

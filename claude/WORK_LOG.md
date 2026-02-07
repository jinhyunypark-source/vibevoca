# 작업 이력

이 파일은 claude 디렉토리에서 수행한 작업들의 이력을 기록합니다.

---

## 2026-01-12: Supabase cards 테이블 영단어 추출

### 작업 내용
Supabase의 cards 테이블에 있는 영어 단어를 가져와서 36개씩 나누어 텍스트 파일로 저장

### 배경
- cards 테이블에 약 1500여개의 영어 단어가 저장되어 있음
- 각 카드의 `front_text` 필드에 영어 단어가 저장됨
- 학습 또는 외부 활용을 위해 단어 목록을 파일로 추출 필요

### 사용한 스크립트
- **파일명**: `export_words.py`
- **위치**: `/Users/jin/dev/vibevoca/claude/export_words.py`

### 스크립트 주요 기능
1. Supabase 클라이언트 생성 (환경변수 사용)
2. cards 테이블에서 `front_text` 필드 조회
3. 페이지네이션을 통해 전체 데이터 가져오기 (1000개씩)
4. 단어를 36개씩 그룹으로 나누어 파일 생성

### 실행 방법

```bash
# 백엔드 가상환경 활성화 후 실행
source backend/venv/bin/activate
python claude/export_words.py
```

또는

```bash
# claude 디렉토리에서 직접 실행 (가상환경 활성화 필요)
cd claude
source ../backend/venv/bin/activate
python export_words.py
```

### 결과물
- **총 단어 수**: 1,568개
- **생성된 파일 수**: 44개
- **파일 위치**: `/Users/jin/dev/vibevoca/claude/word_files/`
- **파일명**: `1.txt` ~ `44.txt`
- **파일 형식**:
  - 영어 단어만 한 줄씩 저장
  - 각 파일당 36개 단어 (마지막 44.txt는 20개)
  - UTF-8 인코딩

### 파일 예시

**1.txt** (36개 단어):
```
Articulate
Coherent
Candid
Frank
Logical
...
```

**44.txt** (20개 단어):
```
Revenue
Profit
Margin
Dividend
Interest
...
```

### 필요 패키지
- supabase-py
- python-dotenv

### 환경 변수
프로젝트 루트의 `.env` 파일에 필요:
- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_ANON_KEY` 또는 `SUPABASE_KEY`: API 키

### 참고 사항
- Supabase는 기본적으로 1000개까지만 반환하므로 페이지네이션 처리
- `range()` 메서드를 사용하여 offset과 limit 설정
- 각 단어는 중복 체크 없이 DB에서 가져온 순서대로 저장됨

---

## 2026-01-12: 단어별 이미지 생성 프롬프트 자동 생성

### 작업 내용
word_files의 각 txt 파일을 읽어서 이미지 생성용 프롬프트를 자동으로 생성하는 스크립트 작성

### 배경
- 1568개의 영어 단어를 시각적으로 학습하기 위해 이미지 생성 필요
- 각 단어 그룹(36개)마다 6x6 그리드 형태의 이미지 생성 계획
- AI 이미지 생성 도구(DALL-E, Midjourney 등)에 사용할 프롬프트 자동 생성
- 프롬프트 템플릿은 향후 수정 가능하도록 변수화

### 사용한 스크립트
- **파일명**: `generate_prompts.py`
- **위치**: `/Users/jin/dev/vibevoca/claude/generate_prompts.py`

### 스크립트 주요 기능
1. `word_files/` 디렉토리의 모든 txt 파일 읽기 (1.txt ~ 44.txt)
2. 각 파일에서 단어 목록 추출
3. 프롬프트 템플릿에 단어 목록 삽입
4. 생성된 프롬프트를 `word_prompts_output/` 디렉토리에 저장

### 프롬프트 템플릿
스크립트 상단에 `PROMPT_TEMPLATE` 변수로 정의되어 있으며, 필요에 따라 쉽게 수정 가능:

```python
PROMPT_TEMPLATE = """단어 하나의 의미를 가장 직관적으로 이해할수 있는 하나의 이미지를 만들고, 그 이미지를 총 36개 가로 6개 세로 6개 모은 하나의 이미지를 만든다. 단어는 다음과 같다.

{words}

각 단어의 이미지는:
- 단어의 핵심 의미를 직관적으로 표현
- 간결하고 명확한 비주얼
- 6x6 그리드 형태로 배열
- 각 이미지는 동일한 크기
"""
```

### 실행 방법

```bash
# 프로젝트 루트에서 실행
python3 claude/generate_prompts.py
```

또는

```bash
# claude 디렉토리에서 실행
cd claude
python3 generate_prompts.py
```

### 결과물
- **생성된 파일 수**: 44개
- **파일 위치**: `/Users/jin/dev/vibevoca/claude/word_prompts_output/`
- **파일명**: `1_prompt.txt` ~ `44_prompt.txt`
- **파일 형식**:
  - 각 프롬프트는 해당 단어 파일의 모든 단어 포함
  - 콤마로 구분된 단어 목록
  - 이미지 생성 지침 포함

### 프롬프트 예시

**1_prompt.txt** (36개 단어):
```
단어 하나의 의미를 가장 직관적으로 이해할수 있는 하나의 이미지를 만들고, 그 이미지를 총 36개 가로 6개 세로 6개 모은 하나의 이미지를 만든다. 단어는 다음과 같다.

Articulate,
Coherent,
Candid,
Frank,
...

각 단어의 이미지는:
- 단어의 핵심 의미를 직관적으로 표현
- 간결하고 명확한 비주얼
- 6x6 그리드 형태로 배열
- 각 이미지는 동일한 크기
```

**44_prompt.txt** (20개 단어):
```
단어 하나의 의미를 가장 직관적으로 이해할수 있는 하나의 이미지를 만들고, 그 이미지를 총 36개 가로 6개 세로 6개 모은 하나의 이미지를 만든다. 단어는 다음과 같다.

Revenue,
Profit,
Margin,
...
```

### 프롬프트 템플릿 수정 방법
프롬프트 내용을 변경하고 싶을 경우:
1. `generate_prompts.py` 파일을 열기
2. 상단의 `PROMPT_TEMPLATE` 변수 수정
3. 필요시 `PROMPT_PREFIX`, `PROMPT_SUFFIX` 추가
4. 스크립트 재실행

### 활용 방안
생성된 프롬프트를 AI 이미지 생성 도구에 입력하여:
- DALL-E 3
- Midjourney
- Stable Diffusion
- 기타 이미지 생성 AI

각 프롬프트로 6x6 그리드 이미지를 생성하여 단어 학습 자료로 활용

### 필요 패키지
- Python 3 기본 라이브러리만 사용 (외부 패키지 불필요)
- glob, os 모듈 사용

### 참고 사항
- 파일 번호 순서대로 정렬하여 처리 (자연수 정렬)
- 빈 단어는 자동으로 필터링
- UTF-8 인코딩으로 저장
- 단어 목록은 콤마와 줄바꿈으로 구분하여 가독성 향상

---

## 2026-01-12: 단어 그룹 크기 변경 (36개 → 64개)

### 작업 내용
기존 36개(6x6 그리드)에서 64개(8x8 그리드)로 단어 그룹 크기 변경 및 프롬프트 업데이트

### 변경 이유
- 더 많은 단어를 한 이미지에 포함하여 파일 수 감소
- 8x8 그리드가 2048x2048 픽셀에서 더 효율적 (각 셀 256x256)
- AI 이미지 생성 시 더 정확한 픽셀 단위 분할 가능

### 수정한 파일

#### 1. export_words.py
```python
# 변경 전
words_per_file = 36

# 변경 후
words_per_file = 64
```

#### 2. generate_prompts.py
프롬프트 템플릿 업데이트:
```python
PROMPT_TEMPLATE = """단어 하나당 하나씩의 이미지를 만들고, 그 이미지를 총 64개 가로 8개 세로 8개 모은 더 큰 하나의 이미지를 만든다. 이미지는 제시된 단어의 순서대로 좌상단에서 우상단으로, 그리고 다음줄로 순서를 반드시 지켜야 한다. 단어는 다음과 같다. 최종 아웃풋은 정확하게 픽셀로 자를수 있게 2048*2048 크기로 만든다.

{words}

각 단어의 이미지는:
- 단어의 핵심 의미를 직관적으로 표현
- 간결하고 명확한 비주얼
- 8*8 그리드 정사각 형태로 배열
- 각 이미지는 동일한 크기
- 단어의 이미지 테두리 표시 하지 않고, 배경 흰색으로 통일
"""
```

### 실행한 작업
1. 기존 word_files 디렉토리 삭제
2. export_words.py 재실행으로 64개씩 단어 파일 재생성
3. 기존 word_prompts_output 디렉토리 삭제
4. generate_prompts.py 재실행으로 새 프롬프트 생성

### 결과물 비교

| 항목 | 변경 전 (36개) | 변경 후 (64개) |
|------|----------------|----------------|
| 그리드 크기 | 6x6 | 8x8 |
| 이미지 크기 | 명시 안 함 | 2048x2048 픽셀 |
| 총 파일 수 | 44개 | 25개 |
| 마지막 파일 단어 수 | 20개 | 32개 |
| 단어당 픽셀 크기 | - | 256x256 |
| 테두리/배경 | 명시 안 함 | 테두리 없음, 흰색 배경 |

### 새로운 결과물
- **총 단어 수**: 1,568개 (동일)
- **생성된 파일 수**: 25개 (44개 → 25개)
- **파일 위치**: `/Users/jin/dev/vibevoca/claude/word_files/`
- **파일명**: `1.txt` ~ `25.txt`
- **프롬프트 파일**: `/Users/jin/dev/vibevoca/claude/word_prompts_output/`
- **프롬프트 파일명**: `1_prompt.txt` ~ `25_prompt.txt`

### 이미지 생성 시 참고사항
- 최종 이미지: 2048x2048 픽셀
- 각 단어 이미지: 256x256 픽셀 (2048÷8=256)
- 배열 순서: 좌상단에서 우상단으로, 다음 줄로 이동
- 배경: 흰색 통일
- 테두리: 없음
- 각 셀은 정확하게 픽셀 단위로 분할 가능

---

## 2026-01-13: 이미지 분할 및 단어-이미지 매핑 시스템

### 작업 내용
AI 이미지 생성 도구(나노바나나 등)로 생성된 2048x2048 그리드 이미지를 64개의 개별 이미지로 분할하고, 각 이미지와 단어, card_id를 매핑하는 시스템 구축

### 배경
- 프롬프트를 통해 8x8 그리드 형태의 단어 이미지를 생성
- 생성된 이미지를 개별 단어 이미지로 분리 필요
- cards 테이블의 card_id와 연동하여 앱에서 활용 가능하도록 매핑 필요
- 이미지 순서와 단어 순서의 정확한 매핑 보장 필요

### 사용한 스크립트
- **파일명**: `split_images.py`
- **위치**: `/Users/jin/dev/vibevoca/claude/split_images.py`

### 스크립트 주요 기능
1. Supabase cards 테이블에서 id, front_text 가져오기
2. input_image/ 폴더의 2048x2048 이미지를 8x8 그리드로 분할
3. 각 분할 이미지를 256x256 PNG로 저장
4. 단어-이미지-card_id 매핑 파일 생성 (CSV, JSON, TXT)

### 입력 및 출력 구조

```
입력:
  input_image/1.png (2048x2048) ← word_files/1.txt의 64개 단어
  input_image/2.png (2048x2048) ← word_files/2.txt의 64개 단어
  ...

출력:
  output_images/
    1_1.png ~ 1_64.png (256x256, 1.png에서 분할)
    2_1.png ~ 2_64.png (256x256, 2.png에서 분할)
    ...

  매핑 파일:
    word_image_mapping.csv   - 상세 매핑 정보
    word_image_mapping.json  - JSON 형태 (메타데이터 포함)
    word_image_summary.txt   - 간단한 요약
```

### 이미지 분할 순서
```
좌상단 → 우상단 → 다음줄 → ...

[1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]
[9]  [10] [11] [12] [13] [14] [15] [16]
[17] [18] [19] [20] [21] [22] [23] [24]
[25] [26] [27] [28] [29] [30] [31] [32]
[33] [34] [35] [36] [37] [38] [39] [40]
[41] [42] [43] [44] [45] [46] [47] [48]
[49] [50] [51] [52] [53] [54] [55] [56]
[57] [58] [59] [60] [61] [62] [63] [64]
```

### 실행 방법

```bash
cd /Users/jin/dev/vibevoca
source backend/venv/bin/activate
python claude/split_images.py
```

### 매핑 파일 형식

#### CSV (word_image_mapping.csv)
```csv
image_file,word,card_id,original_image,position,word_file,row,col
1_1.png,Articulate,2caa0b2a-dad1-4cc7-ad56-02982280cd86,1.png,1,1.txt,1,1
1_2.png,Coherent,659726be-8658-43cc-9630-c124d6c5984e,1.png,2,1.txt,1,2
...
```

#### JSON (word_image_mapping.json)
```json
{
  "metadata": {
    "total_images": 192,
    "grid_size": "8x8",
    "cell_size": "256x256",
    "original_size": "2048x2048",
    "created_at": "..."
  },
  "mappings": [
    {
      "image_file": "1_1.png",
      "word": "Articulate",
      "card_id": "2caa0b2a-...",
      "original_image": "1.png",
      "position": 1,
      "word_file": "1.txt",
      "row": 1,
      "col": 1
    },
    ...
  ]
}
```

### 결과물 (2026-01-13 실행)
- **입력 이미지**: 3개 (1.png, 2.png, 3.png)
- **생성된 분할 이미지**: 192개 (3 × 64)
- **각 이미지 크기**: 256 × 256 픽셀
- **매핑된 카드**: 192개 (cards 테이블 연동)

### 필요 패키지
- Pillow (PIL)
- supabase-py
- python-dotenv

### 향후 활용
1. **앱 연동**: card_id를 통해 cards 테이블과 연동
2. **이미지 업로드**: 분할된 이미지를 Supabase Storage에 업로드
3. **card 업데이트**: cards 테이블의 image_url 필드 업데이트

### 참고 사항
- 이미지 순서는 프롬프트에서 지정한 순서와 동일 (좌상단 → 우상단 → 다음줄)
- word_files/N.txt와 input_image/N.png는 1:1 대응
- 단어가 cards 테이블에 없는 경우 card_id는 null로 기록됨
- row, col 정보로 그리드 내 위치 확인 가능

---

## 2026-01-13: PNG → JPG 변환으로 용량 최적화

### 작업 내용
output_images/ 폴더의 PNG 이미지를 JPG로 변환하여 용량 대폭 절감

### 배경
- 분할된 PNG 이미지 총 용량이 약 134MB로 앱 번들에 포함하기엔 과다
- JPG 포맷으로 변환 시 품질 유지하면서 용량 80% 이상 절감 가능
- 단어 학습용 이미지는 JPG 손실 압축에도 충분한 품질 유지

### 사용한 스크립트
- **파일명**: `convert_to_jpg.py`
- **위치**: `/Users/jin/dev/vibevoca/claude/convert_to_jpg.py`

### 스크립트 주요 기능
1. output_images/ 폴더의 모든 PNG 파일 읽기
2. RGBA → RGB 변환 (흰색 배경에 합성)
3. JPG 품질 85로 최적화 압축
4. output_images_jpg/ 폴더에 저장

### 설정 값
```python
JPG_QUALITY = 85  # 품질 (1-100, 높을수록 품질 좋고 용량 큼)
```

### 실행 방법
```bash
cd /Users/jin/dev/vibevoca
source backend/venv/bin/activate
python claude/convert_to_jpg.py
```

### 결과물
- **변환된 파일**: 1,600개
- **원본 총 용량 (PNG)**: 133.79 MB
- **변환 후 용량 (JPG)**: 19.57 MB
- **절감된 용량**: 114.22 MB (85.4%)

### 필요 패키지
- Pillow (PIL)

---

## 2026-01-13: Flutter 앱 이미지 번들링 및 FlashCard 연동

### 작업 내용
1. JPG 이미지를 card_id 기반 파일명으로 Flutter assets에 복사
2. 버전 관리용 manifest.json 생성
3. FlashCard 위젯에서 이미지 표시 기능 추가

### 배경
- 변환된 JPG 이미지를 앱에 번들로 포함하여 배포 필요
- card_id 기반 파일명으로 DB 연동 간소화
- 향후 이미지 업데이트를 위한 버전 관리 체계 필요

### 사용한 스크립트
- **파일명**: `prepare_assets.py`
- **위치**: `/Users/jin/dev/vibevoca/claude/prepare_assets.py`

### 스크립트 주요 기능
1. word_image_mapping.json에서 card_id 매핑 정보 로드
2. output_images_jpg/ 이미지를 {card_id}.jpg로 복사
3. assets/word_images/ 폴더에 저장
4. 버전 관리용 manifest.json 생성

### 실행 방법
```bash
cd /Users/jin/dev/vibevoca
source backend/venv/bin/activate
python claude/prepare_assets.py
```

### 결과물

#### 이미지 파일
- **위치**: `assets/word_images/`
- **파일명**: `{card_id}.jpg` (예: `2caa0b2a-dad1-4cc7-ad56-02982280cd86.jpg`)
- **총 파일 수**: 1,423개
- **총 용량**: ~19 MB

#### Manifest 파일 (버전 관리)
- **위치**: `assets/word_images/manifest.json`
- **형식**:
```json
{
  "version": "1.0.0",
  "created_at": "2026-01-13T...",
  "total_images": 1423,
  "image_format": "jpg",
  "image_size": "256x256",
  "images": {
    "2caa0b2a-dad1-4cc7-ad56-02982280cd86": {
      "filename": "2caa0b2a-dad1-4cc7-ad56-02982280cd86.jpg",
      "word": "Articulate",
      "hash": "abc123...",
      "size": 12345,
      "original_file": "1_1.png"
    },
    ...
  }
}
```

### pubspec.yaml 업데이트
```yaml
flutter:
  assets:
    - assets/images/decks/
    - assets/sherpa_models/vits-piper-en_US-amy-low/
    - assets/word_images/  # 추가
```

### FlashCard 위젯 수정
**파일**: `lib/features/battle/widgets/flash_card.dart`

#### 추가된 기능
1. `_getWordImagePath()`: card.id로 이미지 경로 생성
2. `_checkImageExists()`: 이미지 존재 여부 확인 (캐시 사용)
3. FutureBuilder로 이미지 로딩 및 표시

#### 주요 코드
```dart
/// 카드 ID로 이미지 경로 생성
String _getWordImagePath() {
  return 'assets/word_images/${widget.card.id}.jpg';
}

/// 이미지 파일 존재 여부 확인 (캐시 사용)
static final Map<String, bool> _imageExistsCache = {};

Future<bool> _checkImageExists(String path) async {
  if (_imageExistsCache.containsKey(path)) {
    return _imageExistsCache[path]!;
  }
  try {
    await rootBundle.load(path);
    _imageExistsCache[path] = true;
    return true;
  } catch (_) {
    _imageExistsCache[path] = false;
    return false;
  }
}
```

#### UI 변경사항
- 이미지가 있는 경우: 이미지를 배경으로 표시 + 그라데이션 오버레이 (텍스트 가독성)
- 이미지가 없는 경우: 기존 GenerativeCardBackground 사용 (폴백)

### 향후 계획 (버전 업데이트)
manifest.json을 활용한 이미지 업데이트 시스템 (추후 구현):
1. 앱 시작 시 서버의 manifest 버전 확인
2. 새 버전이 있으면 변경된 이미지만 다운로드
3. 로컬 manifest 업데이트
4. 파일 해시로 무결성 검증

---


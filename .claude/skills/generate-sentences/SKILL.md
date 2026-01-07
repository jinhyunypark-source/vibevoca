# Generate Sentences Skill

영어 단어 학습을 위한 예문을 자동으로 생성하는 skill입니다.

## 목적

단어 목록과 관심사 태그 정보를 받아서 각 단어별로 자연스럽고 기억하기 쉬운 영어 예문을 생성합니다.

## 실행 방법

```bash
/generate-sentences <words_file> <tags_file> <output_file>
```

또는

```bash
/generate-sentences
```

파라미터 없이 실행하면 대화형으로 파일 경로를 물어봅니다.

## 입력 파일 형식

### words_file (예: words.json)

```json
[
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "meaning": "매우 피곤한",
    "deck_id": "uuid-5678",
    "deck_name": "Daily Essentials"
  },
  {
    "card_id": "uuid-2345",
    "word": "brilliant",
    "meaning": "훌륭한, 빛나는",
    "deck_id": "uuid-5678",
    "deck_name": "Daily Essentials"
  }
]
```

### tags_file (예: tags.json)

```json
{
  "tags_by_interest": {
    "baseball": ["baseball", "sports", "mlb", "kbo"],
    "soccer": ["soccer", "football", "sports", "premier_league"],
    "music": ["music", "concert", "album", "kpop"],
    "gaming": ["gaming", "esports", "video_game"],
    "technology": ["technology", "tech", "ai", "startup"]
  },
  "all_unique_tags": ["ai", "album", "baseball", "..."],
  "total_interests": 15,
  "total_unique_tags": 45
}
```

## 출력 파일 형식

### output_file (예: sentences.json)

```json
[
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "sentence_en": "After the marathon, I felt completely exhausted.",
    "sentence_ko": "마라톤 후에 완전히 지쳤다.",
    "tags": ["fitness", "sports"],
    "deck_name": "Daily Essentials"
  },
  {
    "card_id": "uuid-1234",
    "word": "exhausted",
    "sentence_en": "The pitcher looked exhausted after nine innings.",
    "sentence_ko": "9이닝 후 투수는 지쳐 보였다.",
    "tags": ["baseball", "sports"],
    "deck_name": "Daily Essentials"
  }
]
```

## 예문 생성 요구사항

각 단어에 대해 **5-10개의 예문**을 생성하며, 다음 기준을 따릅니다:

1. **자연스러움**: 실생활에서 사용 가능한 문장
2. **길이**: 10-20 단어 정도
3. **태그 활용**: 입력받은 관심사 태그를 자연스럽게 활용
4. **다양성**: 다양한 맥락과 상황 포함
5. **정확성**: 단어의 의미와 용법이 정확해야 함
6. **기억 용이성**: 학습자가 쉽게 기억할 수 있는 예문

## 처리 흐름

1. **파일 읽기**: words.json과 tags.json 로드
2. **단어 순회**: 각 단어에 대해 반복
3. **예문 생성**:
   - 단어의 의미 파악
   - 관련 태그 선택 (1-3개)
   - 태그를 활용한 자연스러운 예문 작성
   - 한국어 번역/설명 추가
4. **결과 저장**: sentences.json에 저장
5. **진행 상황 보고**: 처리된 단어 수, 생성된 예문 수 출력

## 예시

### 입력 단어: "exhausted" (매우 피곤한)

### 생성 예문:

1. **[fitness, sports]**
   - EN: "After running the marathon, I felt completely exhausted."
   - KO: "마라톤을 뛴 후 완전히 지쳤다."

2. **[baseball, sports]**
   - EN: "The pitcher looked exhausted after throwing 120 pitches in the game."
   - KO: "경기에서 120개의 공을 던진 후 투수는 지쳐 보였다."

3. **[gaming, esports]**
   - EN: "Faker seemed exhausted after the intense five-game series."
   - KO: "치열한 5경기 시리즈 후 페이커는 지쳐 보였다."

4. **[work, technology]**
   - EN: "The developer felt exhausted from debugging code all night."
   - KO: "밤새 코드 디버깅을 하느라 개발자는 지쳤다."

5. **[music, concert]**
   - EN: "The band was exhausted but happy after their three-hour concert."
   - KO: "3시간 콘서트 후 밴드는 지쳤지만 행복했다."

## 주의사항

- 모든 태그를 사용할 필요 없음 (자연스러운 것만 선택)
- 태그가 부자연스러우면 사용하지 않고 일반 예문 작성 가능
- 각 예문은 독립적이어야 함 (문맥 의존성 없음)
- 한국어 번역은 직역보다는 자연스러운 의역 권장
- JSON 형식을 정확히 준수해야 함

## 에러 처리

- 파일을 찾을 수 없는 경우: 파일 경로 확인 메시지 출력
- JSON 파싱 오류: 형식 오류 위치 표시
- 빈 단어 목록: 경고 메시지 출력 후 종료
- 태그 정보 없음: 일반 예문만 생성

## 성능

- 단어당 약 5-10초 소요 (LLM 생성 시간)
- 50개 단어 기준 약 4-5분
- 진행 상황은 10개 단어마다 중간 저장 권장

## 통합 방법

이 skill은 sentence_generation_agent.py의 Step 3에서 호출됩니다:

```python
# Step 3에서 skill 호출
subprocess.run([
    "claude",  # Claude Code CLI
    "/generate-sentences",
    words_file,
    tags_file,
    output_file
])
```

#!/bin/bash
# Deck Sentence Generator - 간편 실행 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="/Users/jin/dev/vibevoca/claude/venv"

# 가상환경 활성화
source "$VENV_PATH/bin/activate"

# 작업 디렉토리로 이동
cd "$SCRIPT_DIR"

# 명령어 파싱
COMMAND="${1:-}"

case "$COMMAND" in
  "all"|"")
    echo "전체 덱 자동 처리를 시작합니다..."
    python3 process_all_decks_auto.py
    ;;

  "status")
    echo "진행상황을 확인합니다..."
    python3 process_all_decks_auto.py --status
    ;;

  "retry")
    echo "실패한 덱을 재시도합니다..."
    python3 process_all_decks_auto.py
    ;;

  "reset")
    echo "진행상황을 초기화합니다..."
    read -p "정말로 진행상황을 초기화하시겠습니까? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      rm -f output/batch_progress.json
      echo "✓ 진행상황이 초기화되었습니다."
    else
      echo "취소되었습니다."
    fi
    ;;

  "clean")
    echo "출력 파일을 정리합니다..."
    read -p "정말로 모든 출력 파일을 삭제하시겠습니까? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      rm -rf output/*.json
      echo "✓ 출력 파일이 정리되었습니다."
    else
      echo "취소되었습니다."
    fi
    ;;

  "help"|"-h"|"--help")
    cat << EOF
Deck Sentence Generator - 덱 예문 자동 생성 도구

사용법:
  ./run_deck_generator.sh [COMMAND]

명령어:
  (없음)    전체 덱 자동 처리 (Resume 모드)
  all       전체 덱 자동 처리
  status    진행상황 확인
  retry     실패한 덱만 재시도
  reset     진행상황 초기화
  clean     출력 파일 정리
  help      이 도움말 표시

예시:
  ./run_deck_generator.sh           # 전체 덱 처리
  ./run_deck_generator.sh status    # 진행상황 확인
  ./run_deck_generator.sh retry     # 재시도

문서:
  자세한 내용은 README_DECK_SENTENCE_GENERATOR.md 참조

EOF
    ;;

  *)
    # 덱 이름으로 간주하여 단일 덱 처리
    DECK_NAME="$COMMAND"
    echo "덱 '$DECK_NAME'을(를) 처리합니다..."

    TIMESTAMP=$(date +%Y%m%d_%H%M%S)

    echo "[1/4] 단어 추출 중..."
    python3 extract_words_from_deck.py \
      --deck-name "$DECK_NAME" \
      --output "output/words_${DECK_NAME}_${TIMESTAMP}.json"

    if [ $? -ne 0 ]; then
      echo "✗ 단어 추출 실패"
      exit 1
    fi

    echo "[2/4] 태그 추출 중..."
    python3 extract_all_tags.py \
      --output "output/tags_${DECK_NAME}_${TIMESTAMP}.json"

    if [ $? -ne 0 ]; then
      echo "✗ 태그 추출 실패"
      exit 1
    fi

    echo "[3/4] 예문 생성 중..."
    python3 generate_sentences_automated.py \
      "output/words_${DECK_NAME}_${TIMESTAMP}.json" \
      "output/tags_${DECK_NAME}_${TIMESTAMP}.json" \
      "output/sentences_${DECK_NAME}_${TIMESTAMP}.json" \
      10

    if [ $? -ne 0 ]; then
      echo "✗ 예문 생성 실패"
      exit 1
    fi

    echo "[4/4] 데이터베이스 업로드 중..."
    python3 upload_sentences_to_db.py \
      --input "output/sentences_${DECK_NAME}_${TIMESTAMP}.json" \
      --skip-duplicates

    if [ $? -ne 0 ]; then
      echo "✗ 업로드 실패"
      exit 1
    fi

    echo "✓ 덱 '$DECK_NAME' 처리 완료!"
    ;;
esac

exit 0

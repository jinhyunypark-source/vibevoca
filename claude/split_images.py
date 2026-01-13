"""
이미지 분할 및 단어-이미지 매핑 스크립트

작업 내용:
1. input_image/ 폴더의 2048x2048 이미지를 64개의 256x256 이미지로 분할
2. 분할된 이미지와 단어, card_id를 매핑하는 파일 생성
3. cards 테이블의 데이터와 연동하여 추적 가능하도록 구성

파일 구조:
- 입력: input_image/{N}.png (2048x2048, 8x8 그리드)
- 출력: output_images/{N}_{1-64}.png (256x256)
- 매핑: word_image_mapping.csv, word_image_mapping.json

이미지 분할 순서:
- 좌상단(1) → 우상단(8) → 다음줄(9) → ... → 우하단(64)
- 프롬프트에서 지정한 순서와 동일

실행 방법:
    source backend/venv/bin/activate
    python claude/split_images.py

작성일: 2026-01-12
자세한 내용: WORK_LOG.md 참고
"""
import os
import json
import csv
from PIL import Image
from supabase import create_client
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

# ==================== 설정 ====================
# 이미지 분할 설정
GRID_SIZE = 8  # 8x8 그리드
IMAGE_SIZE = 2048  # 원본 이미지 크기
CELL_SIZE = IMAGE_SIZE // GRID_SIZE  # 256x256

# 디렉토리 설정
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, 'input_image')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_images')
WORD_FILES_DIR = os.path.join(SCRIPT_DIR, 'word_files')
MAPPING_DIR = SCRIPT_DIR  # 매핑 파일 저장 위치

# ============================================


def get_supabase_client():
    """Supabase 클라이언트 생성"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or os.environ.get("SUPABASE_ANON_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL 또는 SUPABASE_KEY/SUPABASE_ANON_KEY가 설정되지 않았습니다.")

    return create_client(url, key)


def fetch_cards_with_ids():
    """
    Supabase cards 테이블에서 id와 front_text를 가져옴
    export_words.py와 동일한 순서로 가져옴 (order_index 또는 기본 순서)

    Returns:
        list: [{'id': card_id, 'front_text': word}, ...]
    """
    print("Supabase에서 카드 데이터 가져오는 중...")
    supabase = get_supabase_client()

    all_cards = []
    batch_size = 1000
    offset = 0

    while True:
        response = supabase.table("cards").select("id, front_text").range(offset, offset + batch_size - 1).execute()

        if not response.data:
            break

        all_cards.extend(response.data)
        print(f"  {offset + 1}~{offset + len(response.data)}번째 카드 가져오기 완료")

        if len(response.data) < batch_size:
            break

        offset += batch_size

    print(f"총 {len(all_cards)}개의 카드를 가져왔습니다.\n")
    return all_cards


def read_word_file(file_path):
    """단어 파일에서 단어 목록 읽기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words


def split_image(image_path, output_prefix, output_dir):
    """
    2048x2048 이미지를 64개의 256x256 이미지로 분할

    Args:
        image_path: 원본 이미지 경로
        output_prefix: 출력 파일 접두사 (예: "1" → "1_1.png", "1_2.png", ...)
        output_dir: 출력 디렉토리

    Returns:
        list: 생성된 파일 정보 [(position, filename), ...]
    """
    img = Image.open(image_path)

    # 이미지 크기 확인
    if img.size != (IMAGE_SIZE, IMAGE_SIZE):
        print(f"  경고: {image_path}의 크기가 {img.size}입니다. 예상 크기: ({IMAGE_SIZE}, {IMAGE_SIZE})")

    created_files = []
    position = 1

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # 자를 영역 계산 (left, upper, right, lower)
            left = col * CELL_SIZE
            upper = row * CELL_SIZE
            right = left + CELL_SIZE
            lower = upper + CELL_SIZE

            # 이미지 자르기
            cell_img = img.crop((left, upper, right, lower))

            # 파일명 생성 및 저장
            filename = f"{output_prefix}_{position}.png"
            output_path = os.path.join(output_dir, filename)
            cell_img.save(output_path, 'PNG')

            created_files.append((position, filename))
            position += 1

    return created_files


def create_mapping(cards, word_files_dir, input_dir, output_dir):
    """
    이미지 분할 및 매핑 정보 생성

    Returns:
        list: 매핑 정보 리스트
        [{'image_file': '1_1.png', 'word': 'Articulate', 'card_id': 'uuid',
          'original_image': '1.png', 'position': 1, 'word_file': '1.txt'}, ...]
    """
    # 카드를 단어로 인덱싱 (빠른 조회를 위해)
    word_to_card = {}
    for card in cards:
        word = card.get('front_text', '')
        if word:
            word_to_card[word] = card['id']

    print(f"단어-카드ID 매핑 생성 완료 ({len(word_to_card)}개)\n")

    # 입력 이미지 파일 찾기
    input_images = sorted(
        [f for f in os.listdir(input_dir) if f.endswith('.png')],
        key=lambda x: int(x.split('.')[0])
    )

    print(f"처리할 입력 이미지: {len(input_images)}개")
    for img in input_images:
        print(f"  - {img}")
    print()

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    all_mappings = []
    total_images_created = 0
    unmatched_words = []

    for input_image in input_images:
        image_num = input_image.split('.')[0]  # "1.png" → "1"
        word_file = f"{image_num}.txt"
        word_file_path = os.path.join(word_files_dir, word_file)

        # 단어 파일 확인
        if not os.path.exists(word_file_path):
            print(f"경고: {word_file}을 찾을 수 없습니다. {input_image} 건너뜀.")
            continue

        # 단어 목록 읽기
        words = read_word_file(word_file_path)
        print(f"{input_image} 처리 중... ({len(words)}개 단어)")

        # 이미지 분할
        input_image_path = os.path.join(input_dir, input_image)
        created_files = split_image(input_image_path, image_num, output_dir)

        # 매핑 정보 생성
        for (position, filename), word in zip(created_files, words):
            card_id = word_to_card.get(word)

            if card_id is None:
                unmatched_words.append({'word': word, 'image_file': filename})

            mapping = {
                'image_file': filename,
                'word': word,
                'card_id': card_id,
                'original_image': input_image,
                'position': position,
                'word_file': word_file,
                'row': (position - 1) // GRID_SIZE + 1,
                'col': (position - 1) % GRID_SIZE + 1
            }
            all_mappings.append(mapping)

        total_images_created += len(created_files)
        print(f"  → {len(created_files)}개 이미지 생성 완료")

    print(f"\n총 {total_images_created}개의 분할 이미지 생성됨")

    if unmatched_words:
        print(f"\n경고: {len(unmatched_words)}개의 단어가 cards 테이블에서 찾을 수 없습니다:")
        for item in unmatched_words[:5]:  # 처음 5개만 표시
            print(f"  - {item['word']} ({item['image_file']})")
        if len(unmatched_words) > 5:
            print(f"  ... 외 {len(unmatched_words) - 5}개")

    return all_mappings


def save_mapping_csv(mappings, output_path):
    """매핑 정보를 CSV 파일로 저장"""
    fieldnames = ['image_file', 'word', 'card_id', 'original_image', 'position', 'word_file', 'row', 'col']

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(mappings)

    print(f"CSV 매핑 파일 저장: {output_path}")


def save_mapping_json(mappings, output_path):
    """매핑 정보를 JSON 파일로 저장"""
    # 추가 메타데이터 포함
    output_data = {
        'metadata': {
            'total_images': len(mappings),
            'grid_size': f"{GRID_SIZE}x{GRID_SIZE}",
            'cell_size': f"{CELL_SIZE}x{CELL_SIZE}",
            'original_size': f"{IMAGE_SIZE}x{IMAGE_SIZE}",
            'created_at': __import__('datetime').datetime.now().isoformat()
        },
        'mappings': mappings
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print(f"JSON 매핑 파일 저장: {output_path}")


def save_summary(mappings, output_path):
    """
    간단한 요약 파일 저장 (이미지 파일명과 단어만)
    빠른 참조용
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 이미지-단어 매핑 요약\n")
        f.write("# 형식: 이미지파일명 | 단어 | card_id\n")
        f.write("# " + "=" * 60 + "\n\n")

        current_original = None
        for m in mappings:
            if m['original_image'] != current_original:
                if current_original is not None:
                    f.write("\n")
                f.write(f"## {m['original_image']} ({m['word_file']})\n")
                current_original = m['original_image']

            card_id_short = m['card_id'][:8] + '...' if m['card_id'] else 'N/A'
            f.write(f"{m['image_file']:12} | {m['word']:20} | {card_id_short}\n")

    print(f"요약 파일 저장: {output_path}")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("이미지 분할 및 단어-이미지 매핑 스크립트")
    print("=" * 60 + "\n")

    # 1. Supabase에서 카드 데이터 가져오기
    cards = fetch_cards_with_ids()

    # 2. 이미지 분할 및 매핑 생성
    mappings = create_mapping(cards, WORD_FILES_DIR, INPUT_DIR, OUTPUT_DIR)

    if not mappings:
        print("생성된 매핑이 없습니다. 종료합니다.")
        return

    # 3. 매핑 파일 저장
    print("\n매핑 파일 저장 중...")
    csv_path = os.path.join(MAPPING_DIR, 'word_image_mapping.csv')
    json_path = os.path.join(MAPPING_DIR, 'word_image_mapping.json')
    summary_path = os.path.join(MAPPING_DIR, 'word_image_summary.txt')

    save_mapping_csv(mappings, csv_path)
    save_mapping_json(mappings, json_path)
    save_summary(mappings, summary_path)

    # 4. 완료 메시지
    print("\n" + "=" * 60)
    print("작업 완료!")
    print("=" * 60)
    print(f"\n결과물:")
    print(f"  - 분할 이미지: {OUTPUT_DIR}/")
    print(f"  - CSV 매핑: {csv_path}")
    print(f"  - JSON 매핑: {json_path}")
    print(f"  - 요약 파일: {summary_path}")
    print(f"\n총 {len(mappings)}개의 이미지-단어 매핑이 생성되었습니다.")


if __name__ == "__main__":
    main()

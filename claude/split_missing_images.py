"""
누락 이미지 분할 스크립트

작업 내용:
1. input_image/missing_X.png 파일을 8x8 그리드로 분할
2. missing_prompts_output/missing_X.txt의 단어와 매핑
3. missing_images.json의 card_id와 연결
4. 단어가 없는 셀(공백)은 건너뜀

실행 방법:
    source backend/venv/bin/activate
    python claude/split_missing_images.py

작성일: 2026-01-13
"""
import os
import json
from PIL import Image

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# 입력
INPUT_IMAGE_DIR = os.path.join(SCRIPT_DIR, 'input_image')
WORD_FILES_DIR = os.path.join(SCRIPT_DIR, 'missing_prompts_output')
MISSING_JSON = os.path.join(SCRIPT_DIR, 'missing_images.json')

# 출력
OUTPUT_IMAGES_DIR = os.path.join(SCRIPT_DIR, 'output_images')
OUTPUT_JPG_DIR = os.path.join(SCRIPT_DIR, 'output_images_jpg')

# 그리드 설정
GRID_SIZE = 8
CELL_SIZE = 256  # 2048 / 8 = 256
IMAGE_SIZE = 2048

# 특수 파일 설정 (그리드 크기가 다른 경우)
SPECIAL_GRID = {
    '3': 3  # missing_3.png는 3x3 그리드
}

# JPG 품질
JPG_QUALITY = 85
# ============================================


def load_missing_card_mapping():
    """missing_images.json에서 단어 → card_id 매핑 로드"""
    with open(MISSING_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 단어 → card_id 리스트 (같은 단어가 여러 card에 있을 수 있음)
    word_to_cards = {}
    for card in data['cards']:
        word = card['word']
        card_id = card['id']
        if word not in word_to_cards:
            word_to_cards[word] = []
        word_to_cards[word].append(card_id)

    return word_to_cards


def load_word_list(file_num):
    """missing_X.txt에서 단어 목록 로드"""
    filepath = os.path.join(WORD_FILES_DIR, f'missing_{file_num}.txt')
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    return words


def split_image(image_path, words, word_to_cards, file_num, output_png_dir, output_jpg_dir):
    """이미지를 분할하고 단어/card_id와 매핑"""
    img = Image.open(image_path)
    results = []
    used_card_ids = set()  # 이미 사용한 card_id 추적

    # 특수 그리드 크기 확인
    grid_size = SPECIAL_GRID.get(str(file_num), GRID_SIZE)
    cell_size = IMAGE_SIZE // grid_size

    if grid_size != GRID_SIZE:
        print(f"  특수 그리드 처리: {grid_size}x{grid_size} (셀 크기: {cell_size}px)")

    for idx, word in enumerate(words):
        # 그리드 위치 계산
        row = idx // grid_size
        col = idx % grid_size

        # 이미지 자르기
        left = col * cell_size
        upper = row * cell_size
        right = left + cell_size
        lower = upper + cell_size

        cell_img = img.crop((left, upper, right, lower))

        # 표준 크기(256x256)로 리사이즈 (특수 그리드인 경우)
        if grid_size != GRID_SIZE:
            cell_img = cell_img.resize((CELL_SIZE, CELL_SIZE), Image.Resampling.LANCZOS)

        # card_id 찾기
        card_ids = word_to_cards.get(word, [])
        card_id = None
        for cid in card_ids:
            if cid not in used_card_ids:
                card_id = cid
                used_card_ids.add(cid)
                break

        if not card_id:
            print(f"  경고: '{word}'의 card_id를 찾을 수 없음 (이미 모두 사용됨)")
            continue

        # PNG 저장 (파일명: missing_{file_num}_{position}.png)
        position = idx + 1
        png_filename = f"missing_{file_num}_{position}.png"
        png_path = os.path.join(output_png_dir, png_filename)
        cell_img.save(png_path, 'PNG')

        # JPG 저장 (파일명: {card_id}.jpg) - 바로 card_id로 저장
        jpg_filename = f"{card_id}.jpg"
        jpg_path = os.path.join(output_jpg_dir, jpg_filename)

        # RGBA → RGB 변환
        if cell_img.mode == 'RGBA':
            background = Image.new('RGB', cell_img.size, (255, 255, 255))
            background.paste(cell_img, mask=cell_img.split()[3])
            cell_img_rgb = background
        else:
            cell_img_rgb = cell_img.convert('RGB')

        cell_img_rgb.save(jpg_path, 'JPEG', quality=JPG_QUALITY, optimize=True)

        results.append({
            'png_file': png_filename,
            'jpg_file': jpg_filename,
            'word': word,
            'card_id': card_id,
            'position': position,
            'row': row + 1,
            'col': col + 1
        })

    return results


def copy_to_assets(output_jpg_dir):
    """JPG 파일을 assets/word_images/로 복사"""
    assets_dir = os.path.join(PROJECT_ROOT, 'assets', 'word_images')

    if not os.path.exists(assets_dir):
        print(f"경고: assets 폴더가 없습니다: {assets_dir}")
        return 0

    import shutil
    copied = 0

    for filename in os.listdir(output_jpg_dir):
        if filename.startswith('missing_'):
            continue  # missing_X_Y.png 형식은 건너뜀

        if filename.endswith('.jpg'):
            src = os.path.join(output_jpg_dir, filename)
            dst = os.path.join(assets_dir, filename)
            shutil.copy2(src, dst)
            copied += 1

    return copied


def main():
    """메인 실행"""
    print("=" * 60)
    print("누락 이미지 분할 스크립트")
    print("=" * 60 + "\n")

    # 출력 폴더 생성
    os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_JPG_DIR, exist_ok=True)

    # card_id 매핑 로드
    print("card_id 매핑 로드 중...")
    word_to_cards = load_missing_card_mapping()
    print(f"매핑된 단어 수: {len(word_to_cards)}개\n")

    # missing 이미지 파일 찾기
    missing_images = []
    for filename in sorted(os.listdir(INPUT_IMAGE_DIR)):
        if filename.startswith('missing_') and filename.endswith('.png'):
            missing_images.append(filename)

    if not missing_images:
        print("처리할 missing 이미지가 없습니다.")
        print(f"input_image/ 폴더에 missing_1.png, missing_2.png 등의 파일을 추가하세요.")
        return

    print(f"처리할 이미지: {len(missing_images)}개")
    for img in missing_images:
        print(f"  - {img}")
    print()

    # 이미지 분할
    all_results = []
    for img_filename in missing_images:
        # 파일 번호 추출 (missing_1.png → 1)
        file_num = img_filename.replace('missing_', '').replace('.png', '')

        print(f"처리 중: {img_filename}")

        # 단어 목록 로드
        words = load_word_list(file_num)
        if not words:
            print(f"  경고: missing_{file_num}.txt 파일이 없거나 비어있음")
            continue

        print(f"  단어 수: {len(words)}개")

        # 이미지 분할
        image_path = os.path.join(INPUT_IMAGE_DIR, img_filename)
        results = split_image(
            image_path, words, word_to_cards, file_num,
            OUTPUT_IMAGES_DIR, OUTPUT_JPG_DIR
        )

        all_results.extend(results)
        print(f"  분할 완료: {len(results)}개 이미지 생성\n")

    # assets 폴더로 복사
    print("assets/word_images/로 복사 중...")
    copied = copy_to_assets(OUTPUT_JPG_DIR)
    print(f"복사된 파일: {copied}개\n")

    # 결과 저장
    result_file = os.path.join(SCRIPT_DIR, 'missing_split_result.json')
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_images': len(all_results),
            'results': all_results
        }, f, ensure_ascii=False, indent=2)

    # 결과 요약
    print("=" * 60)
    print("완료!")
    print("=" * 60)
    print(f"\n결과:")
    print(f"  - 분할된 이미지: {len(all_results)}개")
    print(f"  - PNG 출력: {OUTPUT_IMAGES_DIR}")
    print(f"  - JPG 출력: {OUTPUT_JPG_DIR}")
    print(f"  - Assets 복사: {copied}개")
    print(f"  - 결과 파일: {result_file}")

    # manifest 업데이트 안내
    print("\n" + "-" * 60)
    print("다음 단계:")
    print("-" * 60)
    print("1. prepare_assets.py 재실행하여 manifest.json 업데이트")
    print("2. 또는 수동으로 assets/word_images/manifest.json 업데이트")
    print("-" * 60)


if __name__ == "__main__":
    main()

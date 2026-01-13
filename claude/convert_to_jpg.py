"""
PNG 이미지를 JPG로 변환하여 용량 절감

작업 내용:
- output_images/ 폴더의 PNG 파일을 JPG로 변환
- output_images_jpg/ 폴더에 저장
- 용량 비교 결과 출력

실행 방법:
    python claude/convert_to_jpg.py

작성일: 2026-01-13
"""
import os
from PIL import Image

# ==================== 설정 ====================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(SCRIPT_DIR, 'output_images')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output_images_jpg')

# JPG 품질 설정 (1-100, 높을수록 품질 좋고 용량 큼)
JPG_QUALITY = 85
# ============================================


def convert_png_to_jpg(input_path, output_path, quality=85):
    """
    PNG 이미지를 JPG로 변환

    Args:
        input_path: 입력 PNG 파일 경로
        output_path: 출력 JPG 파일 경로
        quality: JPG 품질 (1-100)

    Returns:
        tuple: (원본 크기, 변환 후 크기)
    """
    # PNG 이미지 열기
    img = Image.open(input_path)

    # RGBA인 경우 RGB로 변환 (JPG는 알파 채널 지원 안 함)
    if img.mode == 'RGBA':
        # 흰색 배경에 합성
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 알파 채널을 마스크로 사용
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # JPG로 저장
    img.save(output_path, 'JPEG', quality=quality, optimize=True)

    # 파일 크기 반환
    original_size = os.path.getsize(input_path)
    converted_size = os.path.getsize(output_path)

    return original_size, converted_size


def format_size(size_bytes):
    """바이트를 읽기 쉬운 형식으로 변환"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("PNG → JPG 변환 스크립트")
    print(f"JPG 품질: {JPG_QUALITY}")
    print("=" * 60 + "\n")

    # 입력 폴더 확인
    if not os.path.exists(INPUT_DIR):
        print(f"오류: 입력 폴더가 없습니다: {INPUT_DIR}")
        return

    # 출력 폴더 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # PNG 파일 목록
    png_files = sorted(
        [f for f in os.listdir(INPUT_DIR) if f.endswith('.png')],
        key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1].split('.')[0]))
    )

    if not png_files:
        print("변환할 PNG 파일이 없습니다.")
        return

    print(f"변환할 파일: {len(png_files)}개\n")

    total_original = 0
    total_converted = 0

    for i, png_file in enumerate(png_files, 1):
        input_path = os.path.join(INPUT_DIR, png_file)
        jpg_file = png_file.replace('.png', '.jpg')
        output_path = os.path.join(OUTPUT_DIR, jpg_file)

        original_size, converted_size = convert_png_to_jpg(
            input_path, output_path, JPG_QUALITY
        )

        total_original += original_size
        total_converted += converted_size

        # 진행 상황 (10개마다 또는 마지막)
        if i % 50 == 0 or i == len(png_files):
            print(f"  {i}/{len(png_files)} 파일 변환 완료...")

    # 결과 출력
    saved = total_original - total_converted
    saved_percent = (saved / total_original) * 100 if total_original > 0 else 0

    print("\n" + "=" * 60)
    print("변환 완료!")
    print("=" * 60)
    print(f"\n결과:")
    print(f"  - 변환된 파일: {len(png_files)}개")
    print(f"  - 원본 총 용량 (PNG): {format_size(total_original)}")
    print(f"  - 변환 후 용량 (JPG): {format_size(total_converted)}")
    print(f"  - 절감된 용량: {format_size(saved)} ({saved_percent:.1f}%)")
    print(f"\n출력 폴더: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

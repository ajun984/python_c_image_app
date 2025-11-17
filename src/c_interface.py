import ctypes       # Python과 C 언어를 연결해주는 핵심 모듈입니다.
import os           # 파일이나 폴더의 경로를 다루기 위한 운영체제 관련 모듈입니다.

# 이 함수는 C 공유 라이브러리를 로드하고 모든 C 함수를 정의하는 역할을 합니다.
def load_c_filters_library():
    # --- 1. C 공유 라이브러리 로드 ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    library_path = os.path.join(current_dir, 'c_filters.so')

    try:
        c_library = ctypes.CDLL(library_path)
        print(f"C_Interface: '{library_path}' 라이브러리가 성공적으로 로드되었습니다.")
    except OSError as e:
        print(f"오류: C_Interface: C 라이브러리 로드 실패 - {e}")
        print(f"경로를 확인해주세요: {library_path}")
        print("c_filters.so 파일이 src 폴더에 있거나, 경로가 정확한지 확인하세요.")
        exit()

    # --- 2. C 함수(apply_grayscale_c)의 인자 및 반환형 정의 ---
    # C 함수 시그니처: void apply_grayscale_c(unsigned char *pixels, int width, int height)
    c_library.apply_grayscale_c.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte),  # pixels
        ctypes.c_int,                    # width
        ctypes.c_int                     # height
    ]
    c_library.apply_grayscale_c.restype = None
    print("C_Interface: C 함수 'apply_grayscale_c'의 시그니처가 성공적으로 정의되었습니다.")

    # --- NEW: C 함수(apply_brightness_c)의 인자 및 반환형 정의 ---
    # C 함수 시그니처: void apply_brightness_c(unsigned char *pixels, int width, int height, int brightness_factor)
    c_library.apply_brightness_c.argtypes = [
        ctypes.POINTER(ctypes.c_ubyte),  # pixels
        ctypes.c_int,                    # width
        ctypes.c_int,                    # height
        ctypes.c_int                     # brightness_factor (밝기 조절 계수)
    ]
    c_library.apply_brightness_c.restype = None
    print("C_Interface: C 함수 'apply_brightness_c'의 시그니처도 성공적으로 정의되었습니다.")

    return c_library

# --- 모듈이 직접 실행될 때만 실행되는 코드 블록 (자체 테스트 용도) ---
if __name__ == '__main__':
    print("\n--- src/c_interface.py 모듈 자체 테스트 시작 ---")
    c_lib = load_c_filters_library() # 위에서 정의한 함수를 호출하여 C 라이브러리를 로드하고 설정합니다.

    # --- 흑백 필터 테스트 ---
    print("\n--- 흑백 필터 테스트 ---")
    dummy_width = 1 # 가로 1픽셀
    dummy_height = 1 # 세로 1픽셀
    # 빨강색 픽셀 [255, 0, 0]
    dummy_pixels_grayscale = (ctypes.c_ubyte * (dummy_width * dummy_height * 3))(255, 0, 0)
    print(f"더미 픽셀 데이터 (흑백 적용 전): {list(dummy_pixels_grayscale)}")
    c_lib.apply_grayscale_c(dummy_pixels_grayscale, dummy_width, dummy_height)
    print(f"더미 픽셀 데이터 (흑백 적용 후): {list(dummy_pixels_grayscale)}")
    # 예상: [85, 85, 85] (255+0+0)/3 = 85

    # --- 밝기 조절 필터 테스트 ---
    print("\n--- 밝기 조절 필터 테스트 ---")
    dummy_brightness_width = 1
    dummy_brightness_height = 1
    # 초기 픽셀은 중간 밝기의 회색 (128, 128, 128)으로 설정해봅시다.
    dummy_brightness_pixels = (ctypes.c_ubyte * (dummy_brightness_width * dummy_brightness_height * 3))(128, 128, 128)

    print(f"더미 픽셀 데이터 (밝기 조절 전): {list(dummy_brightness_pixels)}")

    # 밝기 50만큼 증가 (+50)
    # 128 + 50 = 178
    c_lib.apply_brightness_c(dummy_brightness_pixels, dummy_brightness_width, dummy_brightness_height, 50)
    print(f"더미 픽셀 데이터 (밝기 +50 적용 후): {list(dummy_brightness_pixels)}") # 예상: [178, 178, 178]

    # 밝기 다시 -100만큼 감소 (현재 178에서 -100)
    # 178 - 100 = 78
    c_lib.apply_brightness_c(dummy_brightness_pixels, dummy_brightness_width, dummy_brightness_height, -100)
    print(f"더미 픽셀 데이터 (밝기 -100 적용 후): {list(dummy_brightness_pixels)}") # 예상: [78, 78, 78]

    # 밝기 다시 -200만큼 감소 (현재 78에서 -200 = -122. C 함수에서 0으로 클리핑됨)
    c_lib.apply_brightness_c(dummy_brightness_pixels, dummy_brightness_width, dummy_brightness_height, -200)
    print(f"더미 픽셀 데이터 (밝기 -200 적용 후, 클리핑): {list(dummy_brightness_pixels)}") # 예상: [0, 0, 0]

    print("--- src/c_interface.py 모듈 자체 테스트 완료 ---\n")
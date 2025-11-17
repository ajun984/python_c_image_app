import ctypes       # <--- Python과 C 언어를 연결해주는 핵심 모듈입니다.
                    #      'C types'의 줄임말로, C 언어의 데이터 타입을 파이썬에서 다루게 해줘요.
import os           # <--- 파일이나 폴더의 경로를 다루기 위한 운영체제 관련 모듈입니다.

# 이 함수는 C 공유 라이브러리를 로드하고 C 함수를 정의하는 모든 로직을 캡슐화(하나로 묶어)합니다.
# 이렇게 하면 다른 파이썬 파일에서 이 함수만 호출하면 C 라이브러리를 바로 사용할 준비가 됩니다.
def load_c_filters_library(): # 함수 이름은 역할에 맞게 'c_filters_library'를 로드한다고 지었습니다.
    # --- 1. C 공유 라이브러리 로드 (불러오기) ---

    # 우리가 만든 'src/c_filters.so' 파일이 어디에 있는지 파이썬에게 정확히 알려줘야 합니다.
    # 이 'c_interface.py' 모듈이 들어있는 'src' 폴더를 기준으로 'c_filters.so'의 경로를 찾습니다.
    # 'os.path.abspath(__file__)'은 현재 이 파일(c_interface.py)의 전체 경로를 알려줍니다.
    # 'os.path.dirname()'은 그 경로에서 'src'라는 '폴더 부분'만 떼어냅니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 'os.path.join()'은 운영체제(Linux)에 맞게 경로를 합쳐줍니다.
    # 최종적으로 'src/c_filters.so'와 같은 경로가 만들어집니다.
    library_path = os.path.join(current_dir, 'c_filters.so')

    try: # 'try' 블록 안의 코드를 실행하다가 문제가 생기면 'except' 블록으로 점프합니다.
        # ctypes.CDLL() 함수를 써서 'c_filters.so' 파일을 메모리에 로드합니다.
        # 이 작업은 C 라이브러리의 코드를 파이썬 프로그램이 사용할 수 있도록 메모리에 올리는 것입니다.
        c_library = ctypes.CDLL(library_path)
        print(f"C_Interface: '{library_path}' 라이브러리가 성공적으로 로드되었습니다.")
    except OSError as e: # 만약 파일을 찾지 못하거나 불러오는 데 문제가 생기면 (예: 파일 이름 오타, 권한 문제)
        print(f"오류: C_Interface: C 라이브러리 로드 실패 - {e}") # 어떤 오류인지 출력
        print(f"경로를 확인해주세요: {library_path}") # 혹시 경로가 틀렸는지 확인하라는 힌트
        print("c_filters.so 파일이 src 폴더에 있거나, 경로가 정확한지 확인하세요.")
        exit() # 라이브러리를 로드하지 못했으므로 프로그램 종료

    # --- 2. C 함수(apply_grayscale_c)의 인자(입력값) 및 반환형(출력값) 정의 ---
    # 파이썬은 C 함수가 어떤 타입의 데이터를 받고 돌려주는지 모르기 때문에, 우리가 명확하게 알려줘야 합니다.
    # 우리가 만든 C 함수 시그니처: void apply_grayscale_c(unsigned char *pixels, int width, int height)

    # c_library.apply_grayscale_c.argtypes = [...]
    # 이 부분에서 'apply_grayscale_c' 함수의 '인자(argument)'들의 타입을 정의합니다.
    # 리스트에 C 함수의 인자 순서대로 파이썬 ctypes 타입들을 넣어줍니다.
    c_library.apply_grayscale_c.argtypes = [
        # 첫 번째 인자: 'unsigned char *pixels' (픽셀 데이터의 메모리 주소)
        # C의 'unsigned char*'는 'ctypes.POINTER(ctypes.c_ubyte)'로 매핑됩니다.
        # 'POINTER'는 메모리 주소를 가리키고, 'c_ubyte'는 0-255 범위의 바이트 값을 의미합니다.
        ctypes.POINTER(ctypes.c_ubyte),
        # 두 번째 인자: 'int width' (이미지의 너비)
        # C의 'int'는 'ctypes.c_int'로 매핑됩니다.
        ctypes.c_int,
        # 세 번째 인자: 'int height' (이미지의 높이)
        ctypes.c_int
    ]

    # c_library.apply_grayscale_c.restype = None
    # 이 부분에서 C 함수의 '반환(return) 타입'을 정의합니다.
    # C 함수가 'void'였으므로, 파이썬에서는 '아무것도 반환하지 않음'을 뜻하는 'None'을 사용합니다.
    c_library.apply_grayscale_c.restype = None

    print("C_Interface: C 함수 'apply_grayscale_c'의 시그니처가 성공적으로 정의되었습니다.")

    # 이 함수가 성공적으로 C 라이브러리를 로드하고 설정하면,
    # 해당 라이브러리 객체(c_library)를 다른 모듈에서 사용할 수 있도록 반환합니다.
    return c_library

# --- 모듈이 '직접 실행될 때만' 실행되는 코드 블록 (자체 테스트 용도) ---
# 'if __name__ == "__main__":' 이 코드는 현재 이 파이썬 파일이
# 1) 'python3 src/c_interface.py' 처럼 직접 실행될 때만
# 2) 다른 파이썬 파일에서 'import src.c_interface' 처럼 불러와질 때는 실행되지 않습니다.
# 이렇게 하면 모듈이 독립적으로도 기능 테스트를 할 수 있으면서,
# 다른 곳에 포함될 때는 불필요한 테스트 코드가 실행되지 않아 깔끔합니다.
if __name__ == '__main__':
    print("\n--- src/c_interface.py 모듈 자체 테스트 시작 ---")
    c_lib = load_c_filters_library() # 위에서 정의한 함수를 호출하여 C 라이브러리를 로드하고 설정합니다.

    # --- 더미 픽셀 데이터로 C 함수 호출 테스트 ---
    # 실제 이미지는 아니지만, C 함수가 픽셀 배열을 어떻게 처리하는지
    # 개념적으로 이해하기 위한 '가상 데이터'입니다.
    dummy_width = 1 # 가로 1픽셀
    dummy_height = 1 # 세로 1픽셀
    # (ctypes.c_ubyte * N)은 C의 'unsigned char[N]' 배열처럼 동작하는 파이썬 객체를 만듭니다.
    # 1x1 픽셀 RGB 이미지이므로 3바이트: [Red, Green, Blue]
    dummy_pixels = (ctypes.c_ubyte * (dummy_width * dummy_height * 3))(255, 0, 0) # 빨강색 픽셀 [255, 0, 0]

    print(f"\n더미 픽셀 데이터 (적용 전): {list(dummy_pixels)}")
    # 이제 C 라이브러리를 통해 C 함수 'apply_grayscale_c'를 호출합니다!
    c_lib.apply_grayscale_c(dummy_pixels, dummy_width, dummy_height)
    print(f"더미 픽셀 데이터 (적용 후, 흑백): {list(dummy_pixels)}")

    # 흑백 변환 로직 (R+G+B)/3 이었으므로: (255 + 0 + 0) / 3 = 85
    # 결과가 [85, 85, 85]로 나온다면 C 함수가 파이썬 데이터에 성공적으로 접근하고 수정한 것입니다!
    print("--- src/c_interface.py 모듈 자체 테스트 완료 ---\n")
from PIL import Image         # <--- 'Pillow' 라이브러리에서 'Image' 모듈을 가져옵니다.
                              #      이것이 파이썬에서 이미지 파일을 열고 저장하고 조작하는 핵심 도구예요.
import ctypes                 # <--- C 언어와 연결하기 위해 역시 필요합니다. (픽셀 데이터 변환에 사용)
import sys
import os                     # <--- 파일 경로를 다룰 때 사용합니다.

# --- 중요: 파이썬 모듈 검색 경로 설정 ---
# 이 코드는 현재 스크립트(image_handler.py)가 들어있는 'src' 폴더의 부모 폴더 (즉, 'python_c_image_app' 폴더)를
# 파이썬이 모듈을 찾는 경로에 추가해 줍니다.
# 이렇게 해야 'from src import c_interface'와 같이 다른 모듈을 패키지처럼 불러올 수 있습니다.
# (이것은 직접 서브 모듈을 실행할 때 발생하는 흔한 오류를 해결하는 방법입니다.)
current_script_dir = os.path.dirname(os.path.abspath(__file__)) # 현재 파일(image_handler.py)이 있는 폴더 (예: .../python_c_image_app/src)
project_root_dir = os.path.abspath(os.path.join(current_script_dir, '..')) # src 폴더의 부모 폴더 (예: .../python_c_image_app)
sys.path.insert(0, project_root_dir) # 이 프로젝트 루트 폴더를 파이썬 모듈 검색 경로의 가장 앞에 추가!
# --- 여기까지 새롭게 추가되는 코드 ---

import numpy as np            # <--- 숫자 배열을 효율적으로 다루기 위한 라이브러리 (옵션이지만 매우 유용!)
                              #      'pip install numpy'로 설치해야 할 수도 있습니다.

# 우리가 만든 '통역가' 모듈을 가져옵니다.
# 이렇게 다른 모듈의 기능을 가져다 쓰는 것이 모듈화의 장점입니다!
from src import c_interface

# ImageHandler 클래스를 정의합니다.
# 클래스는 여러 함수(메서드)와 데이터를 한 덩어리로 묶어서 관리하는 '청사진' 또는 '템플릿'입니다.
# ImageHandler 객체를 만들면, 이미지 처리와 관련된 모든 기능을 깔끔하게 사용할 수 있어요.
class ImageHandler:
    def __init__(self):
        # ImageHandler 객체가 처음 만들어질 때 자동으로 실행되는 부분입니다.
        # 여기서 C 라이브러리 '통역가'를 불러와 준비시킵니다.
        # c_interface.load_c_filters_library() 함수가 C 라이브러리를 로드하고 C 함수를 정의하는 일을 해줍니다.
        self.c_lib = c_interface.load_c_filters_library()
        print("ImageHandler: C 라이브러리(통역가)가 ImageHandler에 연결되었습니다.")

    def load_image(self, image_path):
        # image_path: 불러올 이미지 파일의 경로 (예: 'assets/test_image.jpg')

        try:
            # Image.open(image_path): Pillow를 사용하여 지정된 경로의 이미지 파일을 엽니다.
            # .convert('RGB'): 이미지가 어떤 형식(예: CMYK, RGBA)이든 상관없이 항상 RGB (빨강, 초록, 파랑) 3채널 형식으로 변환합니다.
            #                  우리가 만든 C 함수가 RGB만 처리하므로 중요합니다.
            image = Image.open(image_path).convert('RGB')
            print(f"ImageHandler: '{image_path}' 이미지를 성공적으로 불러왔습니다. ({image.width}x{image.height})")
            return image # 불러온 Image 객체를 반환합니다.
        except FileNotFoundError:
            print(f"오류: ImageHandler: 파일을 찾을 수 없습니다: {image_path}")
            return None
        except Exception as e:
            print(f"오류: ImageHandler: 이미지 불러오기 실패 - {e}")
            return None

    def apply_grayscale(self, image_obj):
        # image_obj: load_image() 함수에서 반환받은 Pillow Image 객체입니다.

        if not image_obj: # 혹시 이미지가 제대로 로드되지 않았으면 처리하지 않습니다.
            print("ImageHandler: 이미지가 유효하지 않아 흑백 필터를 적용할 수 없습니다.")
            return None

        width, height = image_obj.size # Image 객체에서 이미지의 가로(width)와 세로(height) 크기를 가져옵니다.

        # --- 픽셀 데이터를 C 언어가 이해할 수 있는 형태로 준비 ---
        # image_obj.tobytes(): Image 객체의 픽셀 데이터를 바이트(byte) 배열 형태로 변환합니다.
        #                      이것은 R, G, B 순서로 쭉 이어진 큰 숫자 덩어리입니다.
        # len(byte_data): 전체 픽셀 데이터의 바이트 크기입니다. (width * height * 3)
        byte_data = image_obj.tobytes()
        num_bytes = len(byte_data)

        # (ctypes.c_ubyte * num_bytes)(*byte_data):
        # 1. C 언어의 unsigned char 배열과 같은 파이썬 객체를 만듭니다.
        # 2. 이 객체에 기존 바이트 데이터 (byte_data)를 채워 넣습니다.
        #    이렇게 만들어진 'raw_pixels_ptr'는 C 함수로 직접 전달될 수 있는 형태가 됩니다.
        raw_pixels_ptr = (ctypes.c_ubyte * num_bytes).from_buffer_copy(byte_data)
        # from_buffer_copy()를 사용하면 C 배열 객체가 byte_data의 복사본을 만들어서,
        # C 함수가 이 복사본을 안전하게 수정할 수 있게 합니다.

        print(f"ImageHandler: 흑백 필터 적용 전 - {width}x{height} 이미지 픽셀 데이터 준비 완료.")

        # --- C 언어 흑백 필터 함수 호출 ---
        # self.c_lib.apply_grayscale_c(): '통역가'를 통해 C 함수를 호출합니다!
        # 우리가 정의한 C 함수의 인자 순서대로 데이터를 전달합니다: 픽셀 포인터, 너비, 높이.
        self.c_lib.apply_grayscale_c(raw_pixels_ptr, width, height)

        print("ImageHandler: C 흑백 필터 적용 완료.")

        # --- 처리된 픽셀 데이터를 다시 파이썬 Image 객체로 변환 ---
        # Image.frombytes('RGB', (width, height), raw_pixels_ptr):
        # 흑백으로 처리되어 변경된 'raw_pixels_ptr' 데이터를 가져와서,
        # 다시 'RGB' 형식의 (width, height) 크기 Image 객체로 만듭니다.
        processed_image = Image.frombytes('RGB', (width, height), raw_pixels_ptr)
        return processed_image # 흑백으로 변환된 새 Image 객체를 반환합니다.

    def save_image(self, image_obj, output_path):
        # image_obj: 저장할 Pillow Image 객체 (흑백으로 처리된 이미지)
        # output_path: 저장할 파일 경로 (예: 'assets/output_grayscale.jpg')

        if not image_obj: # 혹시 이미지가 제대로 없으면 저장하지 않습니다.
            print("ImageHandler: 저장할 이미지가 유효하지 않습니다.")
            return False

        try:
            image_obj.save(output_path) # Image 객체를 지정된 경로에 파일로 저장합니다.
            print(f"ImageHandler: 이미지를 '{output_path}'에 성공적으로 저장했습니다.")
            return True
        except Exception as e:
            print(f"오류: ImageHandler: 이미지 저장 실패 - {e}")
            return False

# --- 모듈이 직접 실행될 때만 실행되는 코드 블록 (자체 테스트 용도) ---
# 이 블록은 'python3 src/image_handler.py'처럼 직접 실행할 때만 동작합니다.
# 다른 파일에서 import 할 때는 실행되지 않으므로, 이 모듈의 기능을 테스트하기 좋습니다.
if __name__ == '__main__':
    print("\n--- src/image_handler.py 모듈 자체 테스트 시작 ---")

    # 테스트에 사용할 이미지 파일 경로를 지정합니다.
    # assets 폴더에 test_image.jpg 파일을 하나 복사해두면 좋습니다. (어떤 이미지든 상관 없음)
    # 만약 test_image.jpg가 없다면, 웹에서 아무 JPG 파일이나 다운로드하여 assets 폴더에 넣어주세요.
    # 예시: assets/test_image.jpg
    input_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'test_image.jpg')
    output_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'output_grayscale.jpg')

    # ImageHandler 객체를 생성합니다. (__init__ 메서드에서 C 라이브러리 로드)
    handler = ImageHandler()

    # --- 이미지 불러오기 테스트 ---
    original_image = handler.load_image(input_image_path)

    if original_image: # 이미지가 성공적으로 불러와졌다면
        # --- 흑백 필터 적용 테스트 ---
        grayscale_image = handler.apply_grayscale(original_image)

        if grayscale_image: # 흑백 필터 적용도 성공했다면
            # --- 이미지 저장 테스트 ---
            handler.save_image(grayscale_image, output_image_path)
            # 저장된 이미지를 확인해보세요!
            print(f"테스트 완료: '{output_image_path}' 파일을 열어 흑백 이미지를 확인해주세요.")
        else:
            print("테스트 실패: 흑백 필터 적용에 실패했습니다.")
    else:
        print("테스트 실패: 이미지 불러오기에 실패했습니다.")

    print("--- src/image_handler.py 모듈 자체 테스트 완료 ---\n")
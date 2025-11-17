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
        # ImageHandler 객체가 처음 만들어질 때 자동으로 실행됩니다.
        # 여기서 C 라이브러리 '통역가'를 불러와 준비시킵니다.
        self.c_lib = c_interface.load_c_filters_library()
        print("ImageHandler: C 라이브러리(통역가)가 ImageHandler에 연결되었습니다.")

    # --- 여기서부터 `ImageHandler` 클래스의 메서드들입니다. ---
    # --- class ImageHandler: 줄 바로 아래에 네 칸(스페이스 4번 또는 탭 1번) 들여쓰기가 되어야 합니다. ---

    # COMMENT: 빨간색으로 표시된 이 두 함수는 반드시 `class ImageHandler:` 안에 정의되어야 합니다.
    # COMMENT: `def __init__` 메서드와 같은 들여쓰기 레벨에 있어야 합니다.
    def _prepare_pixels_for_c(self, image_obj):
        byte_data = image_obj.tobytes()
        num_bytes = len(byte_data)
        raw_pixels_ptr = (ctypes.c_ubyte * num_bytes).from_buffer_copy(byte_data)
        return raw_pixels_ptr, image_obj.width, image_obj.height

    def _create_image_from_c_pixels(self, raw_pixels_ptr, width, height):
        return Image.frombytes('RGB', (width, height), raw_pixels_ptr)
    # COMMENT: 이 두 함수가 위 `class ImageHandler:` 아래의 들여쓰기 레벨에 정확히 있는지 확인해주세요.


    def load_image(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            print(f"ImageHandler: '{image_path}' 이미지를 성공적으로 불러왔습니다. ({image.width}x{image.height})")
            return image
        except FileNotFoundError:
            print(f"오류: ImageHandler: 파일을 찾을 수 없습니다: {image_path}")
            return None
        except Exception as e:
            print(f"오류: ImageHandler: 이미지 불러오기 실패 - {e}")
            return None

    def apply_grayscale(self, image_obj):
        if not image_obj:
            print("ImageHandler: 이미지가 유효하지 않아 흑백 필터를 적용할 수 없습니다.")
            return None
        raw_pixels_ptr, width, height = self._prepare_pixels_for_c(image_obj)
        print(f"ImageHandler: 흑백 필터 적용 전 - {width}x{height} 이미지 픽셀 데이터 준비 완료.")
        self.c_lib.apply_grayscale_c(raw_pixels_ptr, width, height)
        print("ImageHandler: C 흑백 필터 적용 완료.")
        processed_image = self._create_image_from_c_pixels(raw_pixels_ptr, width, height)
        return processed_image

    def apply_brightness(self, image_obj, brightness_factor):
        if not image_obj:
            print("ImageHandler: 이미지가 유효하지 않아 밝기 필터를 적용할 수 없습니다.")
            return None
        raw_pixels_ptr, width, height = self._prepare_pixels_for_c(image_obj)
        print(f"ImageHandler: 밝기 필터 적용 전 - {width}x{height} 이미지 픽셀 데이터 준비 완료.")
        self.c_lib.apply_brightness_c(raw_pixels_ptr, width, height, brightness_factor)
        print(f"ImageHandler: C 밝기 필터 (+/- {brightness_factor}) 적용 완료.")
        processed_image = self._create_image_from_c_pixels(raw_pixels_ptr, width, height)
        return processed_image

    def save_image(self, image_obj, output_path):
        if not image_obj:
            print("ImageHandler: 저장할 이미지가 유효하지 않습니다.")
            return False
        try:
            image_obj.save(output_path)
            print(f"ImageHandler: 이미지를 '{output_path}'에 성공적으로 저장했습니다.")
            return True
        except Exception as e:
            print(f"오류: ImageHandler: 이미지 저장 실패 - {e}")
            return False

if __name__ == '__main__':
    print("\n--- src/image_handler.py 모듈 자체 테스트 시작 ---")
    input_image_path = os.path.join(project_root_dir, 'assets', 'test_image.jpg')
    output_grayscale_path = os.path.join(project_root_dir, 'assets', 'output_grayscale.jpg')
    output_bright_path = os.path.join(project_root_dir, 'assets', 'output_bright.jpg')
    output_dark_path = os.path.join(project_root_dir, 'assets', 'output_dark.jpg')

    handler = ImageHandler()

    original_image = handler.load_image(input_image_path)

    if original_image:
        print("\n--- 흑백 필터 테스트 ---")
        grayscale_image = handler.apply_grayscale(original_image.copy())
        if grayscale_image:
            handler.save_image(grayscale_image, output_grayscale_path)
            print(f"테스트 완료: '{output_grayscale_path}' 파일을 열어 흑백 이미지를 확인해주세요.")
        else:
            print("테스트 실패: 흑백 필터 적용에 실패했습니다.")

        print("\n--- 밝기 필터 테스트 ---")
        bright_image = handler.apply_brightness(original_image.copy(), 50)
        if bright_image:
            handler.save_image(bright_image, output_bright_path)
            print(f"테스트 완료: '{output_bright_path}' 파일을 열어 밝아진 이미지를 확인해주세요.")
        else:
            print("테스트 실패: 밝기 필터 (밝게) 적용에 실패했습니다.")

        dark_image = handler.apply_brightness(original_image.copy(), -50)
        if dark_image:
            handler.save_image(dark_image, output_dark_path)
            print(f"테스트 완료: '{output_dark_path}' 파일을 열어 어두워진 이미지를 확인해주세요.")
        else:
            print("테스트 실패: 밝기 필터 (어둡게) 적용에 실패했습니다.")
    else:
        print("테스트 실패: 이미지 불러오기에 실패했습니다. assets 폴더에 test_image.jpg가 있는지 확인하세요.")
    print("--- src/image_handler.py 모듈 자체 테스트 완료 ---\n")
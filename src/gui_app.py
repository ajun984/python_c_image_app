import tkinter as tk                  # <--- Tkinter 라이브러리를 tk라는 짧은 이름으로 가져옵니다.
from tkinter import filedialog, messagebox # <--- 파일 열기/저장 창과 알림 메시지 창을 위해 가져옵니다.
from PIL import Image, ImageTk        # <--- 이미지 로드/표시를 위해 Pillow 라이브러리와 Tkinter용 확장 기능을 가져옵니다.
import os                             # <--- 파일 경로를 다룰 때 사용합니다.
import sys                            # <--- 모듈 검색 경로를 설정하기 위해 필요합니다.

# --- 중요: 파이썬 모듈 검색 경로 설정 ---
# 이 gui_app.py 파일이 다른 모듈(image_handler)을 잘 찾을 수 있도록 경로를 설정합니다.
# 다른 모듈에서도 동일하게 적용했던 방식입니다.
current_script_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = os.path.abspath(os.path.join(current_script_dir, '..'))
sys.path.insert(0, project_root_dir)

# 이제 image_handler 모듈을 불러올 수 있습니다.
from src.image_handler import ImageHandler # <--- 우리가 만든 '이미지 처리 담당자' 모듈을 가져옵니다.

# ImageApp 클래스: 우리 앱의 '얼굴'과 모든 기능을 총괄하는 역할을 합니다.
# 마치 자동차 설계도처럼, 이 클래스로 '앱'이라는 자동차를 만들 수 있어요.
class ImageApp:
    def __init__(self, master):
        self.master = master
        master.title("Python-C Image Filter App")

        self.image_handler = ImageHandler()

        self.original_image = None
        self.processed_image = None
        self.tk_image = None
        self.current_brightness = 0 # COMMENT: 빨간색으로 표시된 추가 코드입니다. 현재 밝기 값을 저장할 변수

        # --- GUI 요소들을 생성합니다 ---

        # 1. 이미지 표시 영역 (Label 위젯을 사용)
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10)

        # 2. 버튼 프레임 (버튼들을 묶어서 관리하는 틀)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5)

        # 3. '이미지 열기' 버튼
        self.open_button = tk.Button(self.button_frame, text="이미지 열기", command=self.load_image)
        self.open_button.pack(side=tk.LEFT, padx=5)

        # 4. '흑백 필터 적용' 버튼
        self.grayscale_button = tk.Button(self.button_frame, text="흑백 필터 적용", command=self.apply_grayscale_filter) # COMMENT: 빨간색으로 표시된 수정 코드입니다. (메서드명 변경)
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        # 5. '이미지 저장' 버튼
        self.save_button = tk.Button(self.button_frame, text="이미지 저장", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # --- NEW CODE START --- (COMMENT: 빨간색으로 표시된 추가 코드입니다.)
        # 6. 밝기 조절 프레임 (슬라이더와 레이블을 묶어서 관리)
        self.brightness_frame = tk.Frame(master)
        self.brightness_frame.pack(pady=5)

        # 7. 밝기 조절 슬라이더
        # Scale 위젯: 범위(from_=-100, to=100) 내에서 값을 선택할 수 있는 슬라이더
        # orient=tk.HORIZONTAL: 가로 방향 슬라이더
        # command=self.update_brightness: 슬라이더 값이 변경될 때마다 update_brightness 함수 호출
        # length: 슬라이더의 길이
        self.brightness_scale = tk.Scale(self.brightness_frame, from_=-100, to=100, orient=tk.HORIZONTAL,
                                        label="밝기 조절", command=self.update_brightness, length=300)
        self.brightness_scale.set(self.current_brightness) # 초기 밝기 값 설정
        self.brightness_scale.pack(side=tk.LEFT, padx=5)

        # 8. 밝기 값 표시 레이블
        self.brightness_value_label = tk.Label(self.brightness_frame, text=f"{self.current_brightness}")
        self.brightness_value_label.pack(side=tk.LEFT, padx=5)

        # 9. 밝기 초기화 버튼
        self.reset_brightness_button = tk.Button(self.brightness_frame, text="밝기 초기화", command=self.reset_brightness)
        self.reset_brightness_button.pack(side=tk.LEFT, padx=5)
        # --- NEW CODE END ---


    # --- 버튼을 눌렀을 때 실행될 기능들 (메서드) ---

    def load_image(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.path.join(project_root_dir, 'assets'),
            title="이미지 파일 선택",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*"))
        )
        if file_path:
            loaded_img = self.image_handler.load_image(file_path)
            if loaded_img:
                self.original_image = loaded_img # 원본 이미지를 저장해 둡니다.
                self.processed_image = loaded_img.copy() # 처리할 이미지도 원본 복사본으로 초기화합니다.
                self.display_image(self.processed_image) # 불러온 이미지를 GUI 창에 표시합니다.
                self.reset_brightness() # COMMENT: 빨간색으로 표시된 추가 코드입니다. 이미지 로드 시 밝기 초기화
                print(f"GUI: 이미지 '{file_path}' 로드 완료.")
            else:
                messagebox.showerror("오류", "이미지 불러오기 실패!")
                print(f"GUI: 이미지 '{file_path}' 로드 실패.")


    # COMMENT: 빨간색으로 표시된 수정 코드입니다. 메서드명을 apply_grayscale_filter로 변경하여 다른 메서드와 구분
    def apply_grayscale_filter(self):
        if self.processed_image:
            # '이미지 처리 담당자'에게 흑백 필터 적용을 시킵니다.
            filtered_img = self.image_handler.apply_grayscale(self.processed_image.copy()) # COMMENT: 빨간색으로 표시된 수정 코드입니다. (copy() 추가)
            if filtered_img:
                self.processed_image = filtered_img
                self.display_image(self.processed_image)
                print("GUI: 흑백 필터 적용 완료.")
            else:
                messagebox.showerror("오류", "흑백 필터 적용 실패!")
                print("GUI: 흑백 필터 적용 실패.")
        else:
            messagebox.showinfo("정보", "먼저 이미지를 불러와 주세요.")
            print("GUI: 흑백 필터 적용을 위해 이미지 불러오기 필요.")

    # --- NEW CODE START --- (COMMENT: 빨간색으로 표시된 추가 코드입니다.)
    def update_brightness(self, value):
        # 슬라이더 값이 변경될 때마다 호출되는 함수
        self.current_brightness = int(value) # 현재 밝기 값을 정수로 업데이트
        self.brightness_value_label.config(text=f"{self.current_brightness}") # 레이블 텍스트 업데이트

        if self.original_image: # 원본 이미지가 불러와진 상태라면
            # 원본 이미지의 복사본에 밝기 필터를 적용하여 표시합니다.
            # processed_image는 항상 원본 이미지로부터 시작해서 필터링 결과를 보여줍니다.
            temp_image = self.original_image.copy()
            adjusted_image = self.image_handler.apply_brightness(temp_image, self.current_brightness)
            if adjusted_image:
                self.processed_image = adjusted_image # 밝기 조절된 이미지를 처리된 이미지로 저장
                self.display_image(self.processed_image) # GUI에 표시
            else:
                print("GUI: 밝기 조절 이미지 처리 실패.")
        else:
            # 이미지가 없는데 슬라이더가 움직인 경우
            print("GUI: 이미지가 없어 밝기 조절을 할 수 없습니다.")

    def reset_brightness(self):
        # 밝기 슬라이더와 값, 그리고 이미지 상태를 초기화합니다.
        self.brightness_scale.set(0) # 슬라이더를 0으로 설정
        self.current_brightness = 0 # 밝기 값 초기화
        self.brightness_value_label.config(text=f"{self.current_brightness}") # 레이블 업데이트
        if self.original_image: # 원본 이미지가 있다면
            self.processed_image = self.original_image.copy() # 처리된 이미지를 원본으로 되돌리고
            self.display_image(self.processed_image) # GUI에 다시 표시
            print("GUI: 밝기 조절 초기화 완료.")
        else:
            print("GUI: 원본 이미지가 없어 밝기 조절을 초기화할 수 없습니다.")
    # --- NEW CODE END ---

    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                initialfile="processed_image.jpg", # COMMENT: 빨간색으로 표시된 수정 코드입니다. (초기 파일명 변경)
                filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
            )
            if file_path:
                saved = self.image_handler.save_image(self.processed_image, file_path)
                if saved:
                    messagebox.showinfo("성공", f"이미지를 '{os.path.basename(file_path)}'에 성공적으로 저장했습니다.")
                    print(f"GUI: 이미지 '{file_path}' 저장 완료.")
                else:
                    messagebox.showerror("오류", "이미지 저장 실패!")
                    print(f"GUI: 이미지 '{file_path}' 저장 실패.")
            else:
                print("GUI: 이미지 저장 취소.")
        else:
            messagebox.showinfo("정보", "저장할 이미지가 없습니다.")
            print("GUI: 저장할 이미지가 없어 작업 취소.")

    def display_image(self, image):
        max_width = self.master.winfo_width() - 40
        if max_width <= 0: max_width = 800
        max_height = self.master.winfo_height() - 150
        if max_height <= 0: max_height = 600

        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)

        if ratio < 1:
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            resized_image = image

        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.tk_image)
        self.image_label.image = self.tk_image

# --- 앱 실행 시작점 ---
if __name__ == '__main__':
    root = tk.Tk()
    app = ImageApp(root)
    root.geometry("800x700")
    root.mainloop()
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
        # ImageApp 객체가 처음 만들어질 때 자동으로 실행되는 부분입니다.
        # 여기서 앱의 기본 창을 만들고, 필요한 도구들을 준비합니다.

        self.master = master # master는 Tkinter의 메인 창(Root Window)을 의미합니다.
        master.title("Python-C Image Filter App") # 창의 제목을 설정합니다.

        # '이미지 처리 담당자' (ImageHandler)를 준비합니다.
        # 이 담당자는 이미지 불러오기, 흑백 처리, 저장 등 모든 실질적인 일을 해줄 거예요.
        self.image_handler = ImageHandler()

        self.original_image = None # 사용자가 불러온 원본 이미지를 저장할 변수 (초기에는 없음)
        self.processed_image = None # 처리된 이미지(흑백 등)를 저장할 변수 (초기에는 없음)
        self.tk_image = None       # Tkinter에 이미지를 표시하기 위해 변환된 이미지 객체 (초기에는 없음)

        # --- GUI 요소들을 생성합니다 ---

        # 1. 이미지 표시 영역 (Label 위젯을 사용)
        # 이미지를 보여줄 공간을 만듭니다. 처음에는 비어 있습니다.
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=10) # 창에 배치하고 위아래로 약간의 여백을 줍니다.

        # 2. 버튼 프레임 (버튼들을 묶어서 관리하는 틀)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=5) # 창에 배치하고 위아래로 약간의 여백을 줍니다.

        # 3. '이미지 열기' 버튼
        # 사용자가 이 버튼을 누르면 이미지를 불러올 수 있도록 합니다.
        self.open_button = tk.Button(self.button_frame, text="이미지 열기", command=self.load_image)
        self.open_button.pack(side=tk.LEFT, padx=5) # 왼쪽에 배치하고 좌우로 여백을 줍니다.

        # 4. '흑백 필터 적용' 버튼
        # 사용자가 이 버튼을 누르면 현재 이미지에 흑백 필터를 적용합니다.
        self.grayscale_button = tk.Button(self.button_frame, text="흑백 필터 적용", command=self.apply_grayscale)
        self.grayscale_button.pack(side=tk.LEFT, padx=5)

        # 5. '이미지 저장' 버튼
        # 사용자가 이 버튼을 누르면 처리된 이미지를 파일로 저장합니다.
        self.save_button = tk.Button(self.button_frame, text="이미지 저장", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

    # --- 버튼을 눌렀을 때 실행될 기능들 (메서드) ---

    def load_image(self):
        # 'filedialog.askopenfilename()'을 사용해서 파일 열기 대화 상자를 띄웁니다.
        # 사용자가 선택한 파일의 전체 경로를 반환합니다.
        file_path = filedialog.askopenfilename(
            initialdir=os.path.join(project_root_dir, 'assets'), # 초기 디렉토리를 assets 폴더로 지정
            title="이미지 파일 선택",
            filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All files", "*.*"))
        )
        if file_path: # 파일이 선택되었다면
            # '이미지 처리 담당자'에게 이미지를 불러오도록 시킵니다.
            loaded_img = self.image_handler.load_image(file_path)
            if loaded_img: # 이미지가 성공적으로 불러와졌다면
                self.original_image = loaded_img # 원본 이미지를 저장해 둡니다.
                self.processed_image = loaded_img.copy() # 처리할 이미지도 원본 복사본으로 초기화합니다.
                self.display_image(self.processed_image) # 불러온 이미지를 GUI 창에 표시합니다.
                print(f"GUI: 이미지 '{file_path}' 로드 완료.")
            else:
                messagebox.showerror("오류", "이미지 불러오기 실패!")
                print(f"GUI: 이미지 '{file_path}' 로드 실패.")


    def apply_grayscale(self):
        if self.processed_image: # 현재 창에 표시된 이미지가 있다면
            # '이미지 처리 담당자'에게 흑백 필터 적용을 시킵니다.
            # 이 담당자가 C 라이브러리(통역가)를 이용해서 이미지를 흑백으로 만들어 줄 거예요.
            filtered_img = self.image_handler.apply_grayscale(self.processed_image)
            if filtered_img: # 흑백 필터 적용에 성공했다면
                self.processed_image = filtered_img # 처리된 이미지를 현재 이미지로 업데이트합니다.
                self.display_image(self.processed_image) # 흑백 이미지를 GUI 창에 다시 표시합니다.
                print("GUI: 흑백 필터 적용 완료.")
            else:
                messagebox.showerror("오류", "흑백 필터 적용 실패!")
                print("GUI: 흑백 필터 적용 실패.")
        else:
            messagebox.showinfo("정보", "먼저 이미지를 불러와 주세요.")
            print("GUI: 흑백 필터 적용을 위해 이미지 불러오기 필요.")


    def save_image(self):
        if self.processed_image: # 처리된 이미지가 있다면
            # 'filedialog.asksaveasfilename()'을 사용해서 파일 저장 대화 상자를 띄웁니다.
            # 사용자가 입력한 저장할 파일의 전체 경로를 반환합니다.
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg", # 기본 확장자를 .jpg로 설정
                initialfile="grayscale_image.jpg", # 기본 파일 이름 지정
                filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
            )
            if file_path: # 저장 경로가 선택되었다면
                # '이미지 처리 담당자'에게 현재 이미지를 지정된 경로에 저장하도록 시킵니다.
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
        # Pillow Image 객체를 Tkinter가 표시할 수 있는 형식으로 변환합니다.
        # GUI 창의 크기를 벗어나지 않도록 이미지 크기를 조절하는 기능도 포함합니다.
        max_width = self.master.winfo_width() - 40 # 창 너비에 맞춰 여백 고려
        if max_width <= 0: max_width = 800 # 초기 창 크기가 아직 없을 경우 기본값
        max_height = self.master.winfo_height() - 150 # 창 높이에 맞춰 여백 고려
        if max_height <= 0: max_height = 600

        # 이미지 비율을 유지하며 최대 크기에 맞춰 리사이즈
        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)

        if ratio < 1: # 이미지가 너무 커서 창 크기를 넘어가면
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else: # 이미지가 창 크기보다 작거나 적당하면
            resized_image = image

        self.tk_image = ImageTk.PhotoImage(resized_image) # Tkinter가 표시할 수 있는 객체로 변환
        self.image_label.config(image=self.tk_image) # image_label에 이미지를 설정합니다.
        self.image_label.image = self.tk_image # Tkinter의 버그를 방지하기 위해 참조를 유지합니다.


# --- 앱 실행 시작점 ---
# 이 블록은 이 gui_app.py 파일이 'python3 src/gui_app.py'처럼 직접 실행될 때만 작동합니다.
# 이렇게 모듈화하면 각 파일이 자신의 역할에만 집중하고, 필요한 경우에만 메인 실행 흐름을 가질 수 있습니다.
if __name__ == '__main__':
    root = tk.Tk() # Tkinter 메인 창 객체를 생성합니다. (우리 앱의 가장 바깥 틀)
    app = ImageApp(root) # ImageApp 클래스로 우리 앱의 '얼굴' 객체를 만듭니다.
    root.geometry("800x700") # 창의 초기 크기를 800x700 픽셀로 설정합니다.
    root.mainloop() # Tkinter 앱을 실행하고 사용자의 입력을 기다립니다. 이 줄이 없으면 창이 바로 닫힙니다.
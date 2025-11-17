# Python-C Image Filter App 🚀

## ✨ 프로젝트 개요 (Project Overview)

이 프로젝트는 **C 언어의 높은 처리 속도**를 활용하여 이미지 필터의 핵심 로직을 구현하고, **Python의 Tkinter 라이브러리**로 사용하기 쉬운 GUI(그래픽 사용자 인터페이스)를 구축하여 C 함수를 호출하는 방식으로 동작하는 이미지 처리 애플리케이션입니다. C와 Python의 연동(Functinoal Foreign Interface, FFI) 방식을 학습하고 실습하기 위해 기획되었습니다.

-   **개발 목표:** C와 Python의 장점(C의 성능, Python의 개발 속도 및 GUI 편리성)을 결합하여 효율적인 이미지 처리 애플리케이션 개발.
-   **핵심 기능:** 이미지 파일 불러오기, 흑백 필터 적용, 처리된 이미지 저장.

## 🌟 기술 스택 (Tech Stack)

이 프로젝트에 사용된 주요 기술 및 라이브러리 목록입니다.

-   **언어:** `Python 3.x`, `C`
-   **Python 라이브러리:**
    -   `Tkinter`: GUI (그래픽 사용자 인터페이스) 구축
    -   `Pillow`: 이미지 파일 로드, 저장 및 픽셀 데이터 관리
    -   `ctypes`: Python과 C 공유 라이브러리 (`.so`) 연동
    -   `os`, `sys`: 파일 시스템 및 시스템 경로 관리
-   **C 라이브러리:**
    -   `libc`: C 표준 라이브러리 (기본 내장)
-   **개발 도구:**
    -   `VS Code`: 통합 개발 환경 (IDE)
    -   `Git`: 버전 관리 시스템
    -   `GitHub`: 원격 코드 저장소 및 협업 플랫폼
    -   `Notion`: 프로젝트 관리 및 문서화

## 📁 프로젝트 구조 (Project Structure)

프로젝트는 기능별로 명확하게 모듈화되어 관리됩니다.

python_c_image_app/ ├── src/ # 모든 소스 코드 │ ├── c_filters.c # C 언어 이미지 필터 로직 (흑백 변환) │ ├── c_filters.so # 컴파일된 C 공유 라이브러리 (Python에서 사용) │ ├── c_interface.py # Python-C 연동 (ctypes를 통해 C 함수 정의) │ ├── image_handler.py # 이미지 파일 로드, C 필터 적용 및 저장 관리 │ └── gui_app.py # Tkinter를 사용한 GUI 애플리케이션 (메인 실행 파일) ├── assets/ # 프로젝트에 사용되는 이미지 및 기타 미디어 파일 │ └── test_image.jpg # 테스트용 원본 이미지 (Git 추적) │ └── output_grayscale.jpg # 필터링 후 저장되는 이미지 (Git 무시) ├── docs/ # 프로젝트 문서 (예: 이 README.md) │ └── README.md └── .gitignore # Git 추적에서 제외할 파일 목록


## 🚀 시작하는 방법 (Getting Started)

프로젝트를 로컬 환경에서 실행하기 위한 단계별 가이드입니다.

### 📋 전제 조건 (Prerequisites)

-   **운영체제:** Ubuntu 22.04 (Linux 기반)
-   **Python 3.x:** (기본 설치되어 있을 것입니다)
-   **Git & GitHub Desktop:** 소스 코드 관리
-   **`gcc`:** C 언어 컴파일러 (`sudo apt-get install build-essential` 또는 `sudo apt-get install gcc`로 설치 가능)
-   **`tkinter` 개발 패키지:** Tkinter GUI와 Pillow 연동에 필요
    ```bash
    sudo apt-get update
    sudo apt-get install python3-tk python3-dev tk-dev
    ```

### 📦 설치 (Installation)

1.  **리포지토리 클론:**
    ```bash
    git clone https://github.com/YourGitHubUsername/python_c_image_app.git
    cd python_c_image_app
    ```
    (만약 이전에 이미 폴더를 만들었다면 이 단계를 건너뛰고 바로 `cd` 명령어를 사용합니다.)

2.  **Python 가상 환경 설정 (권장):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *   (이후 모든 `pip install` 명령은 가상 환경 안에서 진행됩니다.)

3.  **Python 종속성 설치:**
    ```bash
    pip install Pillow numpy
    ```
    *   **주의:** `Pillow` 설치 시 `tkinter` 개발 패키지 (`tk-dev`)가 없으면 `ImageTk` 기능이 누락될 수 있습니다. 위에 명시된 `tk-dev`를 먼저 설치했는지 확인하세요.

4.  **C 공유 라이브러리 컴파일:**
    `src` 폴더로 이동하여 C 소스 코드를 공유 라이브러리로 컴파일합니다.
    ```bash
    cd src
    gcc -shared -o c_filters.so c_filters.c -fPIC
    cd .. # 다시 프로젝트 루트 디렉토리로 이동
    ```

### ▶️ 실행 (Usage)

1.  **가상 환경 활성화 (선택 사항이지만 권장):**
    ```bash
    source venv/bin/activate
    ```

2.  **애플리케이션 실행:**
    ```bash
    python3 src/gui_app.py
    ```

3.  **애플리케이션 사용법:**
    -   GUI 창이 열리면 "이미지 열기" 버튼을 클릭하여 `assets` 폴더의 `test_image.jpg` (또는 다른 이미지)를 선택합니다.
    -   "흑백 필터 적용" 버튼을 클릭하여 이미지를 흑백으로 변환합니다.
    -   "이미지 저장" 버튼을 클릭하여 처리된 이미지를 원하는 경로에 저장합니다.

## 🤝 기여 (Contributing)

버그 리포트, 기능 제안 또는 코드 기여를 환영합니다. GitHub 리포지토리의 Issues 섹션을 사용하거나 Pull Request를 제출해 주세요.

## 📄 라이선스 (License)

이 프로젝트는 MIT 라이선스에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.
(현재 `LICENSE` 파일은 없으니, 만약 사용하고 싶지 않으시면 이 섹션을 삭제하셔도 됩니다.)

## 📞 연락처 (Contact)

-   **김준연 (Junyeon Kim)**
-   **GitHub:** [https://github.com/YourGitHubUsername](https://github.com/YourGitHubUsername)

---
(본 문서는 2025년 11월 17일 기준으로 작성되었으며, 필요에 따라 업데이트될 수 있습니다.)
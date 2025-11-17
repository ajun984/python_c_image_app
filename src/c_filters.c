#include <stdio.h>
// C 언어의 표준 입출력 라이브러리를 포함하는 지시어입니다.
// 이 코드를 포함한다고 해서 꼭 출력 기능(printf)을 사용해야 하는 것은 아니지만,
// C 파일을 만들 때 관례적으로 포함시키는 경우가 많습니다.
// 여기서는 이미지 필터 로직 자체에는 필수적이지 않지만, 혹시 모를 디버깅 등에 대비해 둘 수 있습니다.

// --- 이제 이미지를 흑백으로 변환하는 C 함수를 정의할 차례입니다 ---
// 이 함수는 파이썬에서 호출되어 실제 이미지 픽셀 데이터에 접근하고 수정할 것입니다.

// 함수의 '시작 부분(선언부)'입니다.
// void apply_grayscale_c(unsigned char *pixels, int width, int height)

// 1. 'void': 이 함수는 특정 값을 계산해서 돌려주는(반환하는) 것이 아니라,
//           전달받은 'pixels' 데이터를 직접 수정하는 방식으로 작동합니다.
//           그래서 '아무것도 반환하지 않는다'는 의미로 'void' 키워드를 사용합니다.

// 2. 'apply_grayscale_c': 우리가 이 함수에 붙여줄 이름입니다.
//                       나중에 파이썬에서 이 이름으로 함수를 불러서 사용할 거예요.
//                       이름만 봐도 '그레이스케일(흑백) 필터를 적용하는 C 함수'라는 것을 알 수 있죠?

// 3. 괄호 안의 내용: 이 함수가 외부(파이썬)로부터 받을 '정보(입력값)'들입니다.
//    a. 'unsigned char *pixels':
//       - 'unsigned char': 0부터 255까지의 정수를 저장하는 데 사용되는 데이터 타입입니다.
//                          이미지의 빨강(R), 초록(G), 파랑(B) 색상 값은 보통 0~255 사이이므로 이 타입을 사용해요.
//       - '*': '포인터'를 나타내는 기호입니다. C 언어에서 포인터는 '메모리 주소'를 저장하는 특별한 변수입니다.
//              'unsigned char *pixels'는 'pixels'라는 변수가 'unsigned char' 타입의 데이터들이 시작하는 '메모리 주소'를 가리킨다는 뜻입니다.
//              이미지 데이터는 픽셀들이 메모리에 길게 이어져 저장되어 있기 때문에, 그 시작 주소만 알면 모든 픽셀에 접근할 수 있어요.

//    b. 'int width': 이미지의 '가로 길이(너비)'를 나타내는 정수형(int) 입력값입니다.
//    c. 'int height': 이미지의 '세로 길이(높이)'를 나타내는 정수형(int) 입력값입니다.
void apply_grayscale_c(unsigned char *pixels, int width, int height) {
    // 중괄호 '{'는 함수의 실제 동작 코드가 시작되는 지점을 나타냅니다.

    // int num_pixels = width * height;
    // 전체 이미지에 있는 픽셀의 총 개수를 계산합니다.
    // 예를 들어, 가로 100픽셀, 세로 50픽셀 이미지라면 총 5000개의 픽셀이 있는 것이죠.
    int num_pixels = width * height;

    // for (int i = 0; i < num_pixels; i++) { ... }
    // 'for 반복문'입니다. 이 반복문은 'i'라는 변수를 0부터 시작해서
    // 'num_pixels'보다 작을 때까지 (즉, 0부터 num_pixels-1까지) 1씩 증가시키면서
    // 중괄호 안의 코드를 반복해서 실행하라는 의미입니다.
    // 우리는 이 반복문을 사용해서 이미지에 있는 '모든 픽셀'에 차례대로 접근할 거예요.
    for (int i = 0; i < num_pixels; i++) {
        // --- 현재 i번째 픽셀의 RGB 색상 값 가져오기 ---
        // RGB 이미지는 한 픽셀당 Red, Green, Blue 3개의 색상 정보(채널)를 가집니다.
        // 그래서 한 픽셀의 데이터는 메모리에서 총 3바이트(unsigned char)를 차지하게 됩니다.
        // 예를 들어, 첫 번째 픽셀의 R, G, B는 pixels[0], pixels[1], pixels[2]에,
        // 두 번째 픽셀의 R, G, B는 pixels[3], pixels[4], pixels[5]에 저장됩니다.
        // i번째 픽셀의 시작은 항상 'i * 3' 메모리 주소에 위치하게 됩니다.

        // unsigned char r = pixels[i*3];
        // i번째 픽셀의 Red(빨강) 색상 값을 'pixels' 배열에서 가져와 'r' 변수에 저장합니다.
        unsigned char r = pixels[i*3];

        // unsigned char g = pixels[i*3 + 1];
        // i번째 픽셀의 Green(초록) 색상 값을 가져와 'g' 변수에 저장합니다. (시작 주소에서 1칸 뒤)
        unsigned char g = pixels[i*3 + 1];

        // unsigned char b = pixels[i*3 + 2];
        // i번째 픽셀의 Blue(파랑) 색상 값을 가져와 'b' 변수에 저장합니다. (시작 주소에서 2칸 뒤)
        unsigned char b = pixels[i*3 + 2];

        // --- 흑백 변환 로직: RGB 값을 회색으로 만들기 ---
        // 이미지를 흑백으로 바꾸려면, 각 픽셀의 색상(R, G, B) 정보를 '밝기' 정보만을 가지는 '회색' 값으로 바꿔야 합니다.
        // 가장 간단한 방법은 R, G, B 세 값의 '평균'을 계산해서 그 평균 값을 원래의 R, G, B 자리에 똑같이 넣어주는 것입니다.
        // (더 정확한 흑백 변환 알고리즘도 있지만, 학습을 위해 여기서는 간단한 평균을 사용합니다.)

        // unsigned char gray = (unsigned char)((r + g + b) / 3);
        // 빨강, 초록, 파랑 값을 모두 더한 후 3으로 나누어 평균을 계산합니다.
        // 그리고 계산된 평균 값은 다시 'unsigned char' 타입으로 변환하여 'gray' 변수에 저장합니다.
        unsigned char gray = (unsigned char)((r + g + b) / 3);

        // --- 계산된 흑백 값을 원래 픽셀 위치에 다시 저장합니다 ---
        // 이제 원본 픽셀의 R, G, B 값 대신, 방금 계산한 'gray' 값으로 각 색상 채널을 덮어씁니다.
        // 이렇게 하면 이 픽셀은 이제 회색으로 변환됩니다.
        pixels[i*3] = gray;     // Red 채널을 'gray' 값으로 변경
        pixels[i*3 + 1] = gray; // Green 채널을 'gray' 값으로 변경
        pixels[i*3 + 2] = gray; // Blue 채널을 'gray' 값으로 변경
    } // for 반복문의 끝
} // 함수의 끝

// --- 밝기 조절 필터 함수 ---
// 이 함수는 파이썬에서 호출되어 이미지의 밝기를 조절하는 역할을 합니다.
// 픽셀 데이터의 배열, 이미지의 너비, 높이, 그리고 밝기 조절 계수를 입력받습니다.
// brightness_factor는 양수이면 밝아지고, 음수이면 어두워집니다.
void apply_brightness_c(unsigned char *pixels, int width, int height, int brightness_factor) {
    // 전체 픽셀의 개수를 계산합니다.
    int num_pixels = width * height;

    // 모든 픽셀에 대해 반복합니다.
    for (int i = 0; i < num_pixels; i++) {
        // 현재 픽셀의 R, G, B 색상 값을 가져옵니다.
        unsigned char r = pixels[i*3];
        unsigned char g = pixels[i*3 + 1];
        unsigned char b = pixels[i*3 + 2];

        // 밝기 조절 로직: 각 R, G, B 값에 brightness_factor를 더합니다.
        // 이때, 픽셀 값이 0보다 작아지거나 255보다 커지지 않도록 제한(클리핑)합니다.
        // 중간 계산을 위해 int 타입 변수를 사용합니다.
        int new_r = r + brightness_factor;
        if (new_r < 0) new_r = 0;       // 0보다 작으면 0으로 고정
        else if (new_r > 255) new_r = 255; // 255보다 크면 255로 고정

        int new_g = g + brightness_factor;
        if (new_g < 0) new_g = 0;
        else if (new_g > 255) new_g = 255;

        int new_b = b + brightness_factor;
        if (new_b < 0) new_b = 0;
        else if (new_b > 255) new_b = 255;

        // 계산된 밝기 값을 원래 픽셀의 R, G, B 채널에 unsigned char 타입으로 변환하여 저장합니다.
        pixels[i*3] = (unsigned char)new_r;
        pixels[i*3 + 1] = (unsigned char)new_g;
        pixels[i*3 + 2] = (unsigned char)new_b;
    }
}
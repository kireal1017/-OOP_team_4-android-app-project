from setting import Joystick, BackgroundScroller
from resource_img import morning_background, sunset_background, midnight_background, start_logo
from PIL import Image, ImageDraw, ImageFont, ImageEnhance  # 밝기 조절
import time

#조이스틱 버튼 값을 받기 위한 클래스
joystick = Joystick()

# 배경 클래스 초기화
scroller = BackgroundScroller(morning_background, joystick.width, joystick.height)

# 배경화면 관련 
background = sunset_background.crop((0, 0, joystick.width, joystick.height))
bg_width, bg_height = background.size # 배경 이미지의 원래 크기 가져오기
bg_offset = [0, 0]                    # 배경 이미지 슬라이드 위치 저장


font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 폰트 설정
font = ImageFont.truetype(font_path, 23)                            # 폰트 크기


# 크로스페이드 관련 변수들
fade_duration = 40                              # 총 크로스페이드 단계 수, 값이 클수록 크로스페이드가 자연스럽게 구현됨
fade_step = 0                                   # 현재 크로스페이드 단계
current_background = morning_background         # 시작 배경화면
next_background = sunset_background             # 다음 배경화면

scroll_vector = True                               # 스크롤 좌우를 제어하기 위한 값


# 로고 사이즈 계산 후 중앙으로 배치하기
logo_width, logo_height = start_logo.size
logo_x = (joystick.width - logo_width) // 2
logo_y = (joystick.height - logo_height) // 2
logo_image = Image.new("RGB", (joystick.width, joystick.height))


#게임 시작 전 보여줄 화면
def game_wait():
    while True:
        if not (joystick.button_U.value and joystick.button_D.value and 
                joystick.button_L.value and joystick.button_R.value and 
                joystick.button_A.value and joystick.button_B.value): break  # 아무 버튼이 눌리면 루프 종료
        
        # 배경 잘라내기
        cropped_current = scroller.get_cropped_image()
        
        if scroll_vector == 1:                      # 오른쪽으로 갈지 왼쪽으로 스크롤할지 지정하는 부분
            scroller.rightScroll(step = 2)
        else:
            scroller.leftScroll(step = 2)
            
        if scroller.scroll_position >= 715:         # 오른쪽 끝에 닿아갈 때 쯤(예시 값을 715 이상으로 지정)
            scroll_vector = False
            fade_step = 0
        elif scroller.scroll_position <= 10:        # 왼쪽 끝에 닿을 때 쯤(마찬가지로 예시 값을 10 이하로 지정)
            scroll_vector = True
            fade_step = 0
        
        
        if fade_step < fade_duration:                               # 크로스페이드 처리, 정한 단계를 넘었을 때 다음 이미지로 체인지하기 위한 조건문
            img_cross = round((fade_step / fade_duration), 3)       # 이미지가 섞이는 값 계산, round를 통해서 소수점 3자리수까지만 출력
            blended_background = Image.blend(current_background, next_background, img_cross) # 두 이미지를 섞는 blend함수(이미지1, 이미지2, 섞일 정도)
            cropped_blended = blended_background.crop(                                       # 이미지를 240x240으로 자름
                (scroller.scroll_position, 0, scroller.scroll_position + joystick.width, joystick.height))
            fade_step += 1
        else:                                       # 크로스페이드 완료 시 다음 이미지로 전환 아침>노을>저녁 순
            current_background = next_background
            if current_background == morning_background:
                next_background = sunset_background
            elif current_background == sunset_background:
                next_background = midnight_background
            else:
                next_background = morning_background
            fade_step = 0  # 단계 초기화
        
        # 배경화면 위치 변경사항 적용하기
        combined_image = Image.new("RGB", (joystick.width, joystick.height))
        combined_image.paste(cropped_blended, (0, 0))
        
        # 텍스트 추가
        draw = ImageDraw.Draw(combined_image)
        text = "Press any button \nto start game"
        
        # 텍스트 경계 상자 계산
        text_box = draw.textbbox((0, 0), text, font=font)
        text_width = text_box[2] - text_box[0]   # 좌우 경계
        text_height = text_box[3] - text_box[1]  # 상하 경계

        # 텍스트를 위치 (중앙에 우선 배치되도록)
        text_x = (joystick.width - text_width) // 2
        text_y = (joystick.height - text_height) // 2 + 70
        
        draw.text((text_x, text_y), text, font=font, fill="#42FF00")  # 글자 출력
        joystick.disp.image(combined_image)                           # 디스플레이에 배경화면 출력
        
        time.sleep(0.03)  # 딜레이

    brightness = 1.0                        # 밝기 값
    fade_out_duration = 30                  # 어둡게 하는 단계
    fade_step = 1 / fade_out_duration

    for i in range(fade_out_duration):      # 밝기를 줄이기
        enhancer = ImageEnhance.Brightness(combined_image)
        dimmed_image = enhancer.enhance(brightness)
        brightness -= fade_step             # 밝기 감소
        joystick.disp.image(dimmed_image)   # 디스플레이에 어두워지는 이미지를 출력
        
    black_background = Image.new("RGB", (joystick.width, joystick.height), "black")
    black_background.paste(start_logo, (logo_x, logo_y), mask=start_logo)           # 로고 출력
    joystick.disp.image(black_background)

    time.sleep(2)

    return 0
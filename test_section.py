from setting import Joystick, BackgroundScroller
from PIL import Image, ImageDraw, ImageFont
import time

#조이스틱 버튼 값을 받기 위한 클래스
joystick = Joystick()

#배경 이미지
original_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_midnight.png')

# 배경 클래스 초기화
scroller = BackgroundScroller(midnight_background, joystick.width, joystick.height)

background = sunset_background.crop((0, 0, joystick.width, joystick.height))
bg_width, bg_height = background.size # 배경 이미지의 원래 크기 가져오기
bg_offset = [0, 0]                    # 배경 이미지 슬라이드 위치 저장

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 폰트 설정
font = ImageFont.truetype(font_path, 20)                            # 폰트 크기


# 크로스페이드 상태 변수
fade_duration = 40                              # 총 크로스페이드 단계 수, 값이 클수록 크로스페이드가 자연스럽게 구현됨
fade_step = 0                                   # 현재 크로스페이드 단계
current_background = original_background        # 시작 배경화면
next_background = sunset_background             # 다음 배경화면

scroll_vector = True                               # 스크롤 좌우를 제어하기 위한 값

while True:
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
        if current_background == original_background:
            next_background = sunset_background
        elif current_background == sunset_background:
            next_background = midnight_background
        else:
            next_background = original_background
        fade_step = 0  # 단계 초기화
    
    # 배경 출력
    combined_image = Image.new("RGB", (joystick.width, joystick.height))
    combined_image.paste(cropped_blended, (0, 0))
    
    # 텍스트 추가
    draw = ImageDraw.Draw(combined_image)
    text = "Hello World"
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (joystick.width - text_width) // 2
    text_y = (joystick.height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill="white")  # 흰색 텍스트 출력
    

    # 디스플레이 출력
    joystick.disp.image(combined_image)

    time.sleep(0.02)  # 딜레이
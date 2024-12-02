import numpy as np
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from adafruit_rgb_display import st7789

from resource_img import player_res  # 외부 파일에서 스프라이트 시트 경로 가져오기

from PIL import Image
import time

class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        self.width = self.disp.width
        self.height = self.disp.height


joystick = Joystick()

frames = [
    Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_player/player1.png').convert("RGBA"),
    Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_player/player2.png').convert("RGBA"),
    Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_player/player3.png').convert("RGBA"),
    Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_player/player4.png').convert("RGBA"),
    Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_player/player5.png').convert("RGBA"),
]

# 프레임을 순차적으로 보여주는 애니메이션 루프
frame_index = 0
flip = False  # 이미지 반전 상태 (기본적으로 반전되지 않음)

while True:
    # 현재 프레임을 가져오기
    frame = frames[frame_index]
    
    # 반전 여부에 따라 이미지 반전
    if flip:
        frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
        
    x = (joystick.width - frame.width) // 2  # 중앙 배치할 X 좌표
    y = (joystick.height - frame.height) // 2  # 중앙 배치할 Y 좌표
        
    # 배경을 흰색으로 설정 (RGB 모드로 새 배경 만들기)
    background = Image.new("RGBA", (joystick.width, joystick.height), (255, 255, 255, 255))  # 흰색 배경
    
    # 배경 위에 애니메이션 프레임 중앙에 그리기
    background.paste(frame, (x, y), frame)  # 알파 채널을 고려하여 프레임을 배경에 합성
    
    # 화면에 현재 프레임 표시 (RGB로 변환하여 디스플레이에 출력)
    joystick.disp.image(background.convert("RGB"))

    
    # 프레임 인덱스를 순차적으로 증가시킴
    frame_index = (frame_index + 1) % len(frames)
    
    # 왼쪽 버튼 눌림 -> 반전
    if not joystick.button_L.value:  # 왼쪽 이동
        flip = True
    
    # 오른쪽 버튼 눌림 -> 반전 해제
    if not joystick.button_R.value:  # 오른쪽 이동
        flip = False
    
    # 0.1초 대기 후 다음 프레임으로 넘어감
    time.sleep(0.1)
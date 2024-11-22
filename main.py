import time
import random
import numpy as np
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

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

'''-------------------------------------------------- 하드웨어 세팅 부분 --------------------------------------------------'''

class Character:
    def __init__(self, width, height):
        self.character_source = Image.open('esw_raspberryPi_game_project/image_source/test_character.png')
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        self.jump_state = False
        self.crawl_state = False


    def move(self, command = None):
        if command['move'] == False:
            self.state = None
        
        else:
            self.state = 'move'

            if command['up_pressed']:
                if self.jump_state == True or self.crawl_state == True:
                    print("점프 또는 기어가는 중")
                else:
                    self.jump_state = True
                    print("점프 실행")
                    self.jump_state = False
                    
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                if self.jump_state == True:
                    print("점프 중")
                else:
                    self.crawl_state = True
                    print("기어가는 중")
                    self.crawl_state = False
                
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5
            
            if command == 'button_A_pressed':
                print("버튼 A 입력")
            
            if command == 'button_B_pressed':
                print("버튼 B 입력")
            
            
            
            print(self.position)
            if self.position[0] < 0 or self.position[2] > 240:
                print("캐릭터가 가로 경계 벗어남")
            if self.position[1] < 0 or self.position[3] > 240:
                print("캐릭터가 세로 경계 벗어남")

'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''


class BackgroundScroller:
    def __init__(self, image, display_width, display_height):
        self.image = image
        self.display_width = display_width
        self.display_height = display_height
        self.scroll_position = 0  # 현재 스크롤 위치
        self.image_width = image.width
        self.maxplayerRange = 5

    def rightScroll(self, step):
        """배경 이미지를 step만큼 이동"""
        if self.scroll_position >= (self.image_width - self.display_width - self.maxplayerRange): #오른쪽 끝에 도달했을 경우
            step = 0 #이 이상으로는 움직이지 않게 끔
        
        print(self.scroll_position)                 #테스트 출력
        self.scroll_position += step
    
    def leftScroll(self, step):
        if self.scroll_position <= self.maxplayerRange: #왼쪽 끝에 도달했을 경우
            step = 0
        
        print(self.scroll_position)                 #테스트 출력
        self.scroll_position -= step
        

    def get_cropped_image(self):
        """현재 스크롤 위치에 맞게 자른 이미지를 반환"""
        left = self.scroll_position
        right = self.scroll_position + self.display_width
        return self.image.crop((left, 0, right, self.display_height))


'''-------------------------------------------------- 배경 세팅 --------------------------------------------------'''

#조이스틱, 캐릭터 초기화
joystick = Joystick()
my_circle = Character(joystick.width, joystick.height)

#배경 이미지
original_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open('esw_raspberryPi_game_project/image_source/background/background_midnight.png')

# 배경 클래스 초기화
scroller = BackgroundScroller(midnight_background, joystick.width, joystick.height)

background = sunset_background.crop((0, 0, joystick.width, joystick.height))

#디스플레이 초기화 및 출력
my_image = Image.new("RGB", (joystick.width, joystick.height)) #디스플레이 초기화

bg_width, bg_height = background.size #배경 이미지의 원래 크기 가져오기
bg_offset = [0, 0] #배경 이미지 슬라이드 위치 저장

print(original_background.size)
print(background.size)


while True:
    command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
    if not joystick.button_U.value:  # up pressed
        if not joystick.button_L.value:
            print("왼쪽 점프")
        elif not joystick.button_R.value:
            print("오른쪽 점프")
            
        command['up_pressed'] = True
        command['move'] = True

    if not joystick.button_D.value:  # down pressed
        scroller.leftScroll(step = 3) # 왼쪽 이동                   <- 반대로 3 + 5가 되어서 더 빨리 이동함
        if not joystick.button_L.value:
            print("왼쪽 기어가기")
        elif not joystick.button_R.value:
            print("오른쪽 기어가기")
            
        command['down_pressed'] = True
        command['move'] = True

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        scroller.leftScroll(step = 5) # 왼쪽 배경 이동


    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        scroller.rightScroll(step = 5) # 오른쪽 배경 이동
        
    if not joystick.button_A.value:
        command['button_A_pressed'] = True
        
    cropped_background = scroller.get_cropped_image() # 현재 스크롤 상태에 맞게 이미지를 가져옴
    joystick.disp.image(cropped_background)
    
    time.sleep(0.02) #딜레이로 속도 조절

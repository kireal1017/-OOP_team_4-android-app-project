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
            
            elif command == 'button_A_pressed':
                print("버튼 A 입력")
            
            elif command == 'button_B_pressed':
                print("버튼 B 입력")
            
            
            
            print(self.position)
            if self.position[0] < 0 or self.position[2] > 240:
                print("캐릭터가 가로 경계 벗어남")
            if self.position[1] < 0 or self.position[3] > 240:
                print("캐릭터가 세로 경계 벗어남")

'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''

joystick = Joystick()
my_circle = Character(joystick.width, joystick.height)

background = Image.open('esw_raspberryPi_game_project/image_source/test_image.png')

my_image = Image.new("RGB", (joystick.width, joystick.height)) #디스플레이 초기화
joystick.disp.image(background)

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
        if not joystick.button_L.value:
            print("왼쪽 기어가기")
        elif not joystick.button_R.value:
            print("오른쪽 기어가기")
            
        command['down_pressed'] = True
        command['move'] = True

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True

    
    '''        
    if not joystick.button_A.value:   #버튼 A
        command = 'button_A_pressed'
    elif not joystick.button_B.value:   #버튼 B
        command = 'button_B_pressed'
    else:
        command = None
    '''

    # 위치 업데이트
    my_circle.move(command)
    
    # 배경 이미지와 캐릭터를 현재 위치에 맞게 그리기
    my_image.paste(background, (0, 0))  # 배경을 먼저 그리기
    my_image.paste(my_circle.character_source, (int(my_circle.position[0]), int(my_circle.position[1])), my_circle.character_source)

    # 디스플레이에 표시
    joystick.disp.image(my_image)

    time.sleep(0.01)  # 너무 빠른 갱신을 방지하기 위해 약간의 딜레이 추가
    

'''
while True:                                                 #실제로 실행되는 부분
    command = None
    if not joystick.button_U.value:  # up pressed
        command = 'up_pressed'

    elif not joystick.button_D.value:  # down pressed
        command = 'down_pressed'

    elif not joystick.button_L.value:  # left pressed
        command = 'left_pressed'

    elif not joystick.button_R.value:  # right pressed
        command = 'right_pressed'
        
    else:
        command = None

    #my_circle.move(command)
    
    #joystick.disp.image(Image.open('image_source/test_character.png'))
   
    
    my_circle.move(command)
    
    # 배경 이미지와 캐릭터를 현재 위치에 맞게 그리기
    my_image.paste(background, (0, 0))  # 배경을 먼저 그리기
    my_image.paste(my_circle.character_source, (int(my_circle.position[0]), int(my_circle.position[1])), my_circle.character_source)

    # 디스플레이에 표시
    joystick.disp.image(Image.open('esw_raspberryPi_game_project/image_source/test_character.png'))

    time.sleep(0.05)  # 너무 빠른 갱신을 방지하기 위해 약간의 딜레이 추가
    
    #이미지가 이동하는 모션을 구현해야함, 내 생각에는 클래스에서 어찌저찌 해보면 될 거 같은데..
    
    '''
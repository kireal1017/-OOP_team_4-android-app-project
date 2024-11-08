import time
import random
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

import numpy as np
class Character:
    def __init__(self):
        self.character_source = Image.open('image_source/test_character.png')
        self.state = None
        self.position = np.array([240/2 - 20, 240/2 - 20, 240/2 + 20, 240/2 + 20])

    def move(self, command = None):
        if command == None:
            self.state = None
        
        else:
            self.state = 'move'

            if command == 'up_pressed':
                self.position[1] -= 5
                self.position[3] -= 5
                print("up")

            elif command == 'down_pressed':
                self.position[1] += 5
                self.position[3] += 5
                print("down")

            elif command == 'left_pressed':
                self.position[0] -= 5
                self.position[2] -= 5
                print("left")
                
            elif command == 'right_pressed':
                self.position[0] += 5
                self.position[2] += 5
                print("right")

'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''

joystick = Joystick()
my_circle = Character()

background = Image.open('image_source/test_image.png')

my_image = Image.new("RGB", (joystick.width, joystick.height)) #디스플레이 초기화
my_draw = ImageDraw.Draw(my_image) #그림 그리기 위한 도구 선언

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(0, 0, 255, 100))
joystick.disp.image(background)



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

    my_circle.move(command)
    
    joystick.disp.image(Image.open('image_source/test_character.png'))
    
    #이미지가 이동하는 모션을 구현해야함, 내 생각에는 클래스에서 어찌저찌 해보면 될 거 같은데..
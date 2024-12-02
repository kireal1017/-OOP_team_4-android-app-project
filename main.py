#from setting import *
from resource_img import *
import time
import random

import numpy as np
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image
from adafruit_rgb_display import st7789

#from start_environment import game_wait #게임 시작화면 불러온 동시에 게임 시작함

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

class Player:
    def __init__(self, width, height, character_size_x, character_size_y):
        
        self.state = None
        #self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        
        #캐릭터 초기 위치
        self.character_x = 240 // 2 - character_size_x // 2
        self.character_y = 240 // 2 - character_size_y // 2
        
        
        #캐릭터와 벽의 최소 거리
        self.move_limit_x = 50
        self.move_limit_y = 30
        
        #캐릭터 프레임 길이와 몇번째 프레임에 있는지 
        self.frame_index = 0
        
        #실제로 플레이어 모션을 보여줄 이미지
        self.show_player_motion = player_wait       # 기본으로 보이는건 대기 이미지
        self.player_move_frames = player_move       # 움직이기
        
        # 캐릭터 이동 관련 커맨드
        self.command = {'move': False, 'up_pressed': False , 'down_pressed': False, 
                        'left_pressed': False, 'right_pressed': False}
        
        self.health = 100            # 내 체력
        self.max_health = 100        # 치료를 염두해둔 최대 체력
        self.last_damage_time = 0    # 마지막으로 데미지 받은 시간
        self.invincibility_time = 2  # 데미지 입지 않는 무적 타임 (2초)
        
        self.last_key_pressed = None       # 마지막으로 누른 키
        self.previous_button_state = True  # 버튼이 눌리지 않은 상태로 시작
        

    def move(self, command = None):
        if command['move'] == False:
            if self.last_key_pressed == 'left': #왼쪽 키를 마지막으로 누르면 대기 이미지도 반전
                self.show_player_motion = player_wait.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                self.show_player_motion = player_wait
        else:
            if command['up_pressed']:       # 위로 이동
                if self.character_y > self.move_limit_y:    #플레이어가 상단 리미트 높이를 벗어나지 않도록 이동 
                    self.character_y -= 5
                        

            if command['down_pressed']:     # 아래 이동
                self.character_y += 5
                
                
            if command['left_pressed']:     # 왼쪽 이동
                self.show_player_motion = self.player_move_frames[self.frame_index].transpose(Image.FLIP_LEFT_RIGHT) # 이미지 반전
                self.frame_index = (self.frame_index + 1) % len(self.player_move_frames) #이건 나중에 파일 참조 할 것
                if self.character_x > self.move_limit_x:
                    self.character_x -= 5
                self.last_key_pressed = 'left'
                
                
            if command['right_pressed']:    # 오른쪽 이동
                self.show_player_motion = self.player_move_frames[self.frame_index]
                self.frame_index = (self.frame_index + 1) % len(self.player_move_frames)
                if self.character_x < self.move_limit_x - self.character_x:
                    self.character_x += 5
                self.last_key_pressed = 'right'
                                    
            
'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''

class BackgroundScroller:
    def __init__(self, image, display_width, display_height):
        self.image = image
        self.display_width = display_width
        self.display_height = display_height
        self.scroll_position = 0  # 현재 스크롤 위치
        self.image_width = image.width
        self.maxplayerRange = 3
        
        # 바다로 들어가지 않도록 y 이동 범위 지정
        self.y_low_limit = 142
        self.y_limit_morning = 72
        self.y_limit_sunset = 97
        self.y_limit_midnight = 62

    def rightScroll(self, step):
        """배경 이미지를 step만큼 이동"""
        if self.scroll_position >= (self.image_width - self.display_width - self.maxplayerRange): #오른쪽 끝에 도달했을 경우
            step = 0 #이 이상으로는 움직이지 않게 끔
        
        print(self.scroll_position)                 #테스트 출력
        print(self.image_width - self.display_width - self.maxplayerRange)
        self.scroll_position += step
    
    def leftScroll(self, step):
        if self.scroll_position <= self.maxplayerRange: # 왼쪽 끝에 도달했을 경우
            step = 0
        
        print(self.scroll_position)                 #테스트 출력
        self.scroll_position -= step
        

    def get_cropped_image(self):
        """현재 스크롤 위치에 맞게 자른 이미지를 반환"""
        left = self.scroll_position
        right = self.scroll_position + self.display_width
        return self.image.crop((left, 0, right, self.display_height))

'''-------------------------------------------------- 배경 세팅 --------------------------------------------------'''

def player_bullet_fire():    
    if not current_button_state and player.previous_button_state:  # 버튼이 눌림 (이전엔 안 눌렸지만 지금 눌림)
        display.paste(cropped_background, (0, 0))                  # 배경 출력
        print("총알 발사")
        for i in range(len(player_shoot)):
            if player.last_key_pressed == 'right':
                display.paste(player_shoot[i], 
                              (player.character_x, player.character_y), 
                              player_shoot[i])
            else:                                                 # 왼쪽을 바라보고 있었으면 반대로 뒤집어서 보이기
                display.paste(player_shoot[i].transpose(Image.FLIP_LEFT_RIGHT), 
                              (player.character_x, player.character_y), 
                              player_shoot[i].transpose(Image.FLIP_LEFT_RIGHT))
            joystick.disp.image(display)
            time.sleep(0.01)
        

#game_wait() # 게임 시작

#조이스틱, 캐릭터 초기화
joystick = Joystick()
player = Player(width = joystick.width, 
                height = joystick.height, 
                character_size_x = 96, 
                character_size_y = 96) #캐릭터 사이즈 96 x 96

scroller = BackgroundScroller(midnight_background, joystick.width, joystick.height) # 배경 클래스 초기화
display = Image.new("RGB", (joystick.width, joystick.height)) # 디스플레이 초기화


while True:
    command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
    if not joystick.button_U.value:  # up pressed
        command['up_pressed'] = True
        command['move'] = True


    if not joystick.button_D.value:  # down pressed
        command['down_pressed'] = True
        command['move'] = True

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        if player.character_x < player.move_limit_x:
            scroller.leftScroll(step = 5)

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        if player.character_x > player.character_x -  player.move_limit_x:
            scroller.rightScroll(step = 5)
    
    current_button_state = joystick.button_A.value  # 현재 버튼 상태
    if not joystick.button_A.value: # A pressed
        player_bullet_fire()            
    # 버튼 상태 갱신
    player.previous_button_state = current_button_state
    
    
            

    player.move(command)
    
    
    
    # print(player.character_x, player.character_y)
    
    
    cropped_background = scroller.get_cropped_image()   # 현재 스크롤 상태에 맞게 이미지를 가져옴
    display.paste(cropped_background, (0, 0))           # 배경 출력
    
    
    
    display.paste(player.show_player_motion, (player.character_x, player.character_y), player.show_player_motion)  # 알파 채널을 고려하여 프레임을 배경에 합성
    # 배경 출력
    joystick.disp.image(display)

    # 프레임 딜레이
    time.sleep(0.01)  # 짧은 시간 딜레이    
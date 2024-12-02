from setting import *
from resource_img import morning_background, sunset_background, midnight_background
from PIL import Image
import time
import random

#from start_environment import game_wait #게임 시작화면 불러온 동시에 게임 시작함

#조이스틱, 캐릭터 초기화
joystick = Joystick()
player = Player(width = joystick.width, 
                height = joystick.height, 
                character_size_x = 96, 
                character_size_y = 96) #캐릭터 사이즈 96 x 96


# 배경 클래스 초기화
scroller = BackgroundScroller(morning_background, joystick.width, joystick.height)

#디스플레이 초기화 및 출력
display = Image.new("RGB", (joystick.width, joystick.height)) # 디스플레이 초기화

#game_wait() # 게임 시작

while True:
    player.command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
    if not joystick.button_U.value:  # up pressed
        player.command['up_pressed'] = True
        player.command['move'] = True
        #print("up")

    if not joystick.button_D.value:  # down pressed
        player.command['down_pressed'] = True
        player.command['move'] = True
        print("d")

    if not joystick.button_L.value:  # left pressed
        player.command['left_pressed'] = True
        player.command['move'] = True
        print("l")


    if not joystick.button_R.value:  # right pressed
        player.command['right_pressed'] = True
        player.command['move'] = True
        print("r")

    if not joystick.button_A.value:
        player.command['button_A_pressed'] = True
    
    # print(player.character_x, player.character_y)
    
    
    cropped_background = scroller.get_cropped_image() # 현재 스크롤 상태에 맞게 이미지를 가져옴
    display.paste(cropped_background, (0, 0))           # 배경 출력
    
    display.paste(player.show_player_motion, (player.character_x, player.character_y), player.show_player_motion)  # 알파 채널을 고려하여 프레임을 배경에 합성
    
    # 배경 출력
    joystick.disp.image(display)

    # 프레임 딜레이
    time.sleep(0.01)  # 짧은 시간 딜레이
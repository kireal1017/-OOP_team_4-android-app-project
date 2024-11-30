from setting import Joystick, Character, BackgroundScroller
from resource_img import morning_background, sunset_background, midnight_background
from PIL import Image
import time
import random

from start_environment import game_wait #게임 시작화면

#조이스틱, 캐릭터 초기화
joystick = Joystick()
my_circle = Character(joystick.width, joystick.height)


# 배경 클래스 초기화
scroller = BackgroundScroller(morning_background, joystick.width, joystick.height)
background = sunset_background.crop((0, 0, joystick.width, joystick.height))

#디스플레이 초기화 및 출력
my_image = Image.new("RGB", (joystick.width, joystick.height)) # 디스플레이 초기화

bg_width, bg_height = background.size   # 배경 이미지의 원래 크기 가져오기
bg_offset = [0, 0]                      # 배경 이미지 슬라이드 위치 저장

# 캐릭터 중앙 위치 계산
character_width, character_height = my_circle.character_source.size
center_x = joystick.width // 2 - character_width // 2
center_y = joystick.height // 2 - character_height // 2


game_wait()
print("게임 끝남")

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
        #scroller.leftScroll(step = 3) # 왼쪽 이동                   <- 반대로 3 + 5가 되어서 더 빨리 이동함
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
    joystick.disp.image(cropped_background)           # 배경 출력
    
     
    # 배경 위에 캐릭터를 중앙에 배치
    combined_image = Image.new("RGB", (joystick.width, joystick.height))
    combined_image.paste(cropped_background, (0, 0))  # 배경 추가
        
    cropped_background = scroller.get_cropped_image()  # 현재 스크롤 상태에 맞게 이미지를 가져옴
    combined_image.paste(cropped_background, (0, 0))  # 배경 추가 (덮어쓰기 아님)
    

    # 캐릭터를 중앙에 유지
    combined_image.paste(my_circle.character_source, (center_x, center_y), mask=my_circle.character_source)

    # 배경 출력
    joystick.disp.image(combined_image)

    # 프레임 딜레이
    time.sleep(0.01)  # 짧은 시간 딜레이
    
'''
    cropped_background = scroller.get_cropped_image() # 현재 스크롤 상태에 맞게 이미지를 가져옴
    joystick.disp.image(cropped_background)
    
    # 배경 위에 캐릭터를 중앙에 배치
    combined_image = Image.new("RGB", (joystick.width, joystick.height))
    combined_image.paste(cropped_background, (0, 0))  # 배경 추가
    
    combined_image.paste(my_circle.character_source,(center_x, center_y)) #캐릭터 출력 
    
    # 배경 출력
    joystick.disp.image(combined_image)
    
    time.sleep(0.01) #딜레이
'''

    
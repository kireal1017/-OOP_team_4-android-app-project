#from setting import *
from resource_img import *
import time
import random

import numpy as np
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
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

class Player:
    def __init__(self, width, height, character_size_x, character_size_y):
        self.state = None
        #캐릭터 초기 위치
        self.character_x = 240 // 2 - character_size_x // 2
        self.character_y = 240 // 2 - character_size_y // 2
        
        self.character_size = np.array([character_size_x, character_size_y]) # 캐릭터 크기
        self.position = np.array([self.character_x, self.character_y]) # 캐릭터 좌상단 좌표

        # 캐릭터의 중심 좌표 계산 (좌상단 기준으로 크기 반영)
        self.center = self.position + (self.character_size // 2)  # 중심 좌표 계산
        
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
        
        self.last_key_pressed = 'right'    # 마지막으로 누른 키, 첫 시작은 플레이어가 오른쪽을 바라보고 있음, None로 초기화하면 시작해서 총쏘자마자 에러 발생
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
    
    
    def damage(self, hit_damage):                   # 플레이어가 데미지 입는 부분
        current_time = time.time()
        
        # 무적 시간 동안은 데미지를 입지 않음
        if current_time - self.last_damage_time < self.invincibility_time:
            return False  # 데미지 무시
        
        self.health -= hit_damage
        self.last_damage_time = current_time
        
        if self.health <= 0:
            print('플레이어 사망')
            return True             # 게임 종료
        
        return False                # 죽기 전까지는 게임 마저 실행
    
    
    def heal(self, heal_point):                     # 힐을 받는 부분, 이부분은 시간나면 해볼 것
        if(self.health <= self.max_health):
            self.health += heal_point
        else:
            self.health = self.max_health
            
    def player_health_bar(self, draw_bar):     # 체력 바 생성
        """
        체력 바를 그리는 함수
        draw: ImageDraw 객체
        position: 체력 바의 중심 위치 (x, y)
        width, height: 체력 바 크기
        health: 현재 체력
        max_health: 최대 체력
        """
        x_calibrate = 45
        y_calibrate = 30
        
        bar_length = 80
        bar_height = 5

        # 체력 비율에 따라 바의 길이 계산
        health_ratio = self.health / self.max_health
        filled_length = int(bar_length * health_ratio)
        
        if int(health_ratio * 100) >= 70 and int(health_ratio * 100) <= 100:
            fill_color = (0, 255, 0)
        elif int(health_ratio * 100) >= 50 and int(health_ratio * 100) < 70:
            fill_color = (255, 255, 0)
        else:
            fill_color = (255, 0, 0)


        # 체력 바
        draw_bar.rectangle(
            [self.character_x - bar_length // 2 + x_calibrate, 
             self.character_y - bar_height // 2 + y_calibrate, 
             self.character_x - bar_length // 2 + x_calibrate + filled_length, 
             self.character_y + bar_height // 2 + y_calibrate],
            fill = fill_color
        )

class Enemy:
    def __init__(self, spawn_position):
        self.appearance = 'circle'
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 25, spawn_position[0] + 25, spawn_position[1] + 25])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
 
        self.speed = 2  # 적의 이동 속도
        self.last_shot_time = 0  # 마지막 총알 발사 시간 기록
        self.health = 100 # 적의 체력
    
    
    def update_center(self):
        """현재 중심 좌표 업데이트"""
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
    
    
    def move_towards(self, player_position, min_distance):
        """
        플레이어를 향해 이동하면서 최소 거리를 유지하는 함수
        player_position: [x, y] 형식의 numpy 배열로 제공
        min_distance: 플레이어와 적 간 최소 거리
        """
        direction = player_position - self.center  # 플레이어와 적 사이의 방향 벡터
        distance = np.linalg.norm(direction)  # 거리 계산
        
        if distance > min_distance:  # 최소 거리보다 멀 때만 이동
            normalized_direction = direction / distance  # 방향 벡터 정규화
            movement = normalized_direction * self.speed  # 속도에 따라 이동량 계산
            
            # 적의 위치 업데이트
            self.position[0] += movement[0]
            self.position[2] += movement[0]
            self.position[1] += movement[1]
            self.position[3] += movement[1]
            
            # 중심 좌표 갱신
            self.update_center()
        
        
    def shoot(self, player_position):
        """
        플레이어의 위치를 기준으로 총알 발사 방향 결정
        player_position: [x, y] 형식의 numpy 배열로 제공
        """
        if player_position[0] > self.center[0]:  # 플레이어가 적의 오른쪽에 있을 때
            direction = 'right'
        else:  # 플레이어가 적의 왼쪽에 있을 때
            direction = 'left'
        return EnemyBullet(self.center, direction)       
    
'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''

class Bullet:
    def __init__(self, last_key_pressed):
        self.speed = 10
        self.damage = 10
        self.state = None
        self.image = player_bullet[0]
        self.x = player.character_x + 55    #총알의 시작 위치 캐릭터 이미지를 생각해서 조금 값을 보정함
        self.y = player.character_y + 58
        
        self.direction = {'left' : False, 'right' : False}

        if last_key_pressed == 'right':
            self.direction['right'] = True
        if last_key_pressed == 'left':
            self.direction['left'] = True

        
    def move(self):
        if self.direction['left']:
            self.x -= self.speed
            
        if self.direction['right']:
            self.x += self.speed
  
           
    def collision_check(self, enemys):      # 적에게 맞았는지 확인
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                enemy.state = 'die'
                self.state = 'hit'
                
    
    
    def draw(self, draw_surface): #현재 총알 이미지를 화면에 출력, (x, y) 좌표는 이미지의 좌상단을 기준으로 출력
        if player.last_key_pressed == 'right':
            draw_surface.paste(self.image, (self.x, self.y), self.image)  # 총알 이미지 출력
        else:
            draw_surface.paste(self.image.transpose(Image.FLIP_LEFT_RIGHT), (self.x, self.y), self.image.transpose(Image.FLIP_LEFT_RIGHT))
    
    def overlap(self, ego_position, other_position):
        '''
        두개의 사각형(bullet position, enemy position)이 겹치는지 확인하는 함수
        좌표 표현 : [x1, y1, x2, y2]
        
        return :
            True : if overlap
            False : if not overlap
        '''
        return ego_position[0] > other_position[0] and ego_position[1] > other_position[1] \
                 and ego_position[2] < other_position[2] and ego_position[3] < other_position[3]
    
    
    def is_out_of_bounds(self, width, height):                            # 총알이 화면 경계를 벗어났는지 확인하는 함수
        if self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            return True
        return False

class EnemyBullet:
    def __init__(self, position, direction):
        self.position = np.array([position[0] - 5, position[1] - 5, position[0] + 5, position[1] + 5])
        self.speed = 5
        self.direction = direction  # 'left' 또는 'right'
        self.state = 'active'
        self.outline = "#FF0000"  # 빨간색 총알

    def move(self):
        """총알 이동"""
        if self.direction == 'left':
            self.position[0] -= self.speed
            self.position[2] -= self.speed
        elif self.direction == 'right':
            self.position[0] += self.speed
            self.position[2] += self.speed

    def is_out_of_bounds(self, width, height):
        """화면 경계 밖으로 나갔는지 확인"""
        x1, y1, x2, y2 = self.position
        return x2 < 0 or x1 > width

'''-------------------------------------------------- 총알 세팅 --------------------------------------------------'''

# --------------------------------------------------------------------------- 게임 시작 전 설정 사항
            


#조이스틱, 캐릭터 초기화
joystick = Joystick()
player = Player(width = joystick.width, 
                height = joystick.height, 
                character_size_x = 96, 
                character_size_y = 96) #캐릭터 사이즈 96 x 96


scroller = BackgroundScroller(midnight_background, joystick.width, joystick.height) # 배경 클래스 초기화
display = Image.new("RGB", (joystick.width, joystick.height))                       # 디스플레이 초기화

draw_bar = ImageDraw.Draw(display)                                                  # 체력 바 및 경고창을 그리기 위한 draw

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 폰트 설정
font = ImageFont.truetype(font_path, 17)                            # 폰트 크기

# ------------------------------------------------------------------------------ 디스플레이 관련 설정


def player_bullet_fire():    #플레이어 총알 발사
    if not current_button_state and player.previous_button_state:  # 버튼이 눌림 (연속적으로 눌린 상태를 읽는 것을 방지)
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
            
        # 총알을 발사할 때 총알 객체를 만들어 bullets 리스트에 추가
        print(f"총알 발사, 방향: {player.last_key_pressed}")
        bullet = Bullet(player.last_key_pressed)
        bullets.append(bullet)

def spawn_random_enemies(num_enemies, width, height):               # 적 랜덤으로 생성
    """
    랜덤한 위치에 적을 생성하는 함수
    num_enemies: 생성할 적의 수
    width, height: 스크린 크기
    """
    new_enemies = []
    for _ in range(num_enemies):
        x = random.randint(50, width - 50)  # 화면 가장자리에서 벗어나도록 최소/최대 값 설정
        y = random.randint(50, height - 50)
        new_enemies.append(Enemy((x, y)))
    return new_enemies

def check_collision(rect1, rect2):                                          # 총알 맞았는지 확인 함수
    """
    두 사각형(rect1, rect2)이 겹치는지 확인하는 함수
    rect1, rect2: [x1, y1, x2, y2] 형태의 사각형 좌표 리스트
    return: True if the rectangles overlap, False otherwise
    """
    return not (
        rect1[2] < rect2[0] or  # rect1의 오른쪽이 rect2의 왼쪽보다 왼쪽
        rect1[0] > rect2[2] or  # rect1의 왼쪽이 rect2의 오른쪽보다 오른쪽
        rect1[3] < rect2[1] or  # rect1의 아래쪽이 rect2의 위쪽보다 위
        rect1[1] > rect2[3]     # rect1의 위쪽이 rect2의 아래쪽보다 아래
    )

enemys_list = []    # 적 리스트 초기화
enemy_bullets = []  # 적 총알 리스트 초기화
bullets = []        # 내 총알 리스트

#game_wait() # ---------------------------------------------------------------------- 게임 시작 전 출력 화면

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
    
    # ------------------------------------------------------------------------ 플레이어 총알 발사
    current_button_state = joystick.button_A.value  # 현재 버튼 상태
    if not joystick.button_A.value and player.previous_button_state: # A pressed
        player_bullet_fire()        # 발사 모션

    # 버튼 상태 갱신
    player.previous_button_state = current_button_state
    
    
    # ------------------------------------------------------------------------ 플레이어 및 적 이동 확인
    player.move(command) #플레이어 이동 갱신
    
    
    # ----------------------------------------------------------------------- 총알들의 유효성 및 피격 여부
     
    # 사용자 총알 위치 확인
    bullets_to_keep = []
    for bullet in bullets:
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"총알이 화면 밖으로 나갔습니다: {bullet.x} {bullet.y}")
        elif bullet.state == 'hit':
            print(f"총알 충돌로 제거: {bullet.x,} {bullet.y}")
        else:
            bullet.move()
            bullets_to_keep.append(bullet)  # 유효한 총알만 유지
    bullets = bullets_to_keep  # 유효한 총알로 리스트 업데이트
    
    #print(len(bullets_to_keep)) # 총알 갯수 확인하기
    
    #적이 총에 맞았다면 즉시 제거 됨
    remaining_enemies = []
    for enemy in enemys_list:
        if enemy.state == 'die':
            print(f"적 제거: {enemy.position}")
        else:
            remaining_enemies.append(enemy)  # 유효한 적만 유지
    enemys_list = remaining_enemies          # 유효한 적으로 리스트 업데이트
    
    
    # 적이 모두 제거되었을 경우 새로운 적 3개 생성
    if len(enemys_list) == 0:
        print("새로운 적을 생성합니다!")
        enemys_list.extend(spawn_random_enemies(3, joystick.width, joystick.height))  # 적 추가
        
    
    # 적이 플레이어를 향해 이동하고 일정 시간마다 총알 발사
    current_time = time.time()
    for enemy in enemys_list:
        if enemy.state == 'alive':
            enemy.move_towards(player.center, min_distance = 80)  # 플레이어를 향해 이동, 일정 거리 떨어져서 옴
            if current_time > enemy.last_shot_time + 1:  # 2초마다 발사
                enemy_bullet = enemy.shoot(player.center)  # 플레이어 위치 전달
                enemy_bullets.append(enemy_bullet)
                enemy.last_shot_time = current_time  # 발사 시간 갱신
    
    # 적 총알 이동 및 화면 경계 처리       
    enemy_bullets_to_keep = []
    for bullet in enemy_bullets:
        bullet.move()
        
        # 플레이어와 충돌 확인
        if check_collision(bullet.position, player.position):
            print("플레이어가 적의 총알에 맞았습니다!")
            if player.damage(10):  # 체력 감소 (10만큼 데미지)
                break                                                   #우선 for문 먼저 나옴
            bullet.state = 'hit'  # 충돌한 총알 상태를 변경
            continue  # 해당 총알은 더 이상 처리하지 않도록 다음 총알로 넘어감
        
        # 적 총알 위치 확인    
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"적 총알 제거: {bullet.position}")
        else:
            enemy_bullets_to_keep.append(bullet)
    enemy_bullets = enemy_bullets_to_keep  # 유효한 총알만 유지
    
    # -------------------------------------- --------------------------------------------- 출력 부분
        
    cropped_background = scroller.get_cropped_image()   # 현재 스크롤 상태에 맞게 이미지를 가져옴
    display.paste(cropped_background, (0, 0))           # 배경 출력
    
    for enemy in enemys_list:
        if enemy.state != 'die':
            draw_bar.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0)) # 적 그리기

    display.paste(player.show_player_motion, (player.character_x, player.character_y), player.show_player_motion)  # 플레이어 출력
    player.player_health_bar(draw_bar)
    
    for bullet in bullets:          # 플레이어 총알
        if bullet.state != 'hit':
            bullet.draw(display)  # 총알 이미지 출력
    
    
    
    
    
    
    joystick.disp.image(display)

    # 프레임 딜레이
    time.sleep(0.01)  # 짧은 시간 딜레이    
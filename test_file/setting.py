from resource_img import *
import time

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

class BackgroundScroller:
    def __init__(self, image, display_width, display_height):
        self.image = image
        self.display_width = display_width
        self.display_height = display_height
        self.scroll_position = 0  # 현재 스크롤 위치
        self.image_width = image.width
        self.maxplayerRange = 3

    def rightScroll(self, step):
        """배경 이미지를 step만큼 이동"""
        if self.scroll_position >= (self.image_width - self.display_width - self.maxplayerRange): #오른쪽 끝에 도달했을 경우
            step = 0 #이 이상으로는 움직이지 않게 끔
        
        # print(self.scroll_position)                 #테스트 출력
        # print(self.image_width - self.display_width - self.maxplayerRange)
        self.scroll_position += step
    
    def leftScroll(self, step):
        if self.scroll_position <= self.maxplayerRange: # 왼쪽 끝에 도달했을 경우
            step = 0
        
        print(self.scroll_position)                     # 테스트 출력
        self.scroll_position -= step
        

    def get_cropped_image(self): # 현재 스크롤된 위치에 맞게 자른 이미지를 반환함
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
        self.position = np.array([self.character_x, self.character_y])       # 캐릭터 좌상단 좌표

        # 캐릭터의 중심 좌표 계산 (좌상단 기준으로 크기 반영)
        self.center = self.position + (self.character_size // 2)  # 중심 좌표 계산
        
        #캐릭터 몇번째 프레임에 있는지 
        self.frame_index = 0
        
        #실제로 플레이어 모션을 보여줄 이미지
        self.show_player_motion = player_wait       # 기본으로 보이는건 대기 이미지
        self.player_move_frames = player_move       # 움직이기
        self.player_dead_frames = player_dead       # 사망
        
        # 캐릭터 이동 관련 커맨드
        self.command = {'move': False, 'up_pressed': False , 'down_pressed': False, 
                        'left_pressed': False, 'right_pressed': False}
        
        self.health = 100            # 내 체력
        self.max_health = 100        # 치료를 염두해둔 최대 체력
        self.last_damage_time = 0    # 마지막으로 데미지 받은 시간
        self.invincibility_time = 2  # 데미지 입지 않는 무적 타임 (2초)
        
        self.killed_enemy = 0        # 적 처치 횟수
        
        self.last_key_pressed = 'right'    # 마지막으로 누른 키, 첫 시작은 플레이어가 오른쪽을 바라보고 있음, None로 초기화하면 시작해서 총쏘자마자 에러 발생
        self.previous_button_state = True  # 버튼이 눌리지 않은 상태로 시작
        
        self.background_state = 'morning'  # 이 프로퍼티는 스테이지가 바뀌면서 수정되어야됨!!!!
        
        # y 이동 범위 지정
        self.y_bottom_limit = 142
        self.y_limit_morning = 72
        self.y_limit_sunset = 97
        self.y_limit_midnight = 77
        

    def move(self, command = None):
        if command['move'] == False:
            if self.last_key_pressed == 'left': #왼쪽 키를 마지막으로 누르면 대기 이미지도 반전
                self.show_player_motion = player_wait.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                self.show_player_motion = player_wait
        else:
            if command['up_pressed']:       # 위로 이동
                if stage.stage_level == 1:              # 각 스테이지 별로 y높이를 다르게 조정(바다 이미지 때문에)
                    if self.character_y >= self.y_limit_morning:
                        self.character_y -= 5
                elif stage.stage_level == 2:
                    if self.character_y >= self.y_limit_sunset:
                        self.character_y -= 5
                elif stage.stage_level == 3:
                    if self.character_y >= self.y_limit_midnight:
                        self.character_y -= 5
                        

            if command['down_pressed']:     # 아래 이동
                if self.character_y <= self.y_bottom_limit:         # 디스플레이 아래로 이탈하는 것을 방지하기 위해 리밋을 걸어놓음
                    self.character_y += 5
                
                
            if command['left_pressed']:     # 왼쪽 이동
                self.show_player_motion = self.player_move_frames[self.frame_index].transpose(Image.FLIP_LEFT_RIGHT) # 이미지 반전
                self.frame_index = (self.frame_index + 1) % len(self.player_move_frames)        # 이건 나중에 파일 참조 할 것
                if self.character_x >= 10:
                    self.character_x -= 5
                else:
                    scroller.leftScroll(step = 5)
            
                self.last_key_pressed = 'left'
                
                
            if command['right_pressed']:    # 오른쪽 이동
                self.show_player_motion = self.player_move_frames[self.frame_index]
                self.frame_index = (self.frame_index + 1) % len(self.player_move_frames)
                if self.character_x <= 150:
                    self.character_x += 5
                else:
                    scroller.rightScroll(step = 5)
                
                self.last_key_pressed = 'right'
                
            print("play x, y", self.character_x, self.character_y)
            
            # 플레이어 좌표 최신화
            self.position = np.array([self.character_x, self.character_y])
            self.center = self.position + (self.character_size // 2)
            
    
    
    def damage(self, hit_damage):                   # 플레이어가 데미지 입는 부분
        current_time = time.time()
        
        # 무적 시간 동안은 데미지를 입지 않음
        if current_time - self.last_damage_time < self.invincibility_time:
            return False  # 데미지 무시
        
        self.health -= hit_damage
        self.last_damage_time = current_time
        
        if self.health <= 0:
            print('플레이어 사망')
            return True
        
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
        
    def player_die(self):
        self.state = 'dead'  # 플레이어 상태를 죽음으로 변경
        if self.last_key_pressed == 'left':
            self.show_player_motion = self.player_dead_frames[self.frame_index].transpose(Image.FLIP_LEFT_RIGHT) # 이미지 반전
            self.frame_index = (self.frame_index + 1) % len(self.player_move_frames)        # 이건 나중에 파일 참조 할 것
        elif self.last_key_pressed == 'right':
            self.show_player_motion = self.player_dead_frames[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.player_move_frames)
            

class Enemy:
    def __init__(self, move, attack, hurt, dead, spawn_position, attack_power, speed, health, boss):
        self.move_img = move
        self.attack_img = attack
        self.hurt_img = hurt
        self.dead_img = dead
         
        self.attack = attack_power     # 적의 공격력
        self.speed = speed             # 적의 이동 속도
        self.health = health           # 적의 체력
        self.last_attack_time = 0      # 마지막 공격 시간 기록
        self.state = 'alive'           # 생존 여부
        self.boss_check = boss         # 보스 여부
        
        self.approach = False
        
        self.frame_index = 0           # 프레임 위치
        self.show_motion = self.move_img[0]     # 움직이는 첫 번째 이미지 출력
        
        self.x, self.y = spawn_position        
        self.x_size, self.y_size = self.move_img[0].size
        
        self.center = np.array([self.x + self.x_size // 2, self.y + self.y_size // 2])      # 적의 중심 값
        # 적의 사각형 위치 (x1, y1, x2, y2) 형태
        self.position = np.array([self.x, self.y, self.x + self.x_size, self.y + self.y_size])
        
        
    def update_center(self):
        """현재 중심 좌표 업데이트"""
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        
    
    def move_towards(self, player_position, min_distance):
        """
        플레이어를 향해 이동하면서 최소 거리를 유지하는 함수
        player_position: [x, y] 형식의 numpy 배열로 제공
        min_distance: 플레이어와 적 간 최소 거리
        """
        player_x, player_y = player_position  # 플레이어 x, y좌표 분리
        enemy_x, enemy_y = self.center        # 적의 현재 x, y 좌표
        
        # x 방향으로 이동
        if player_x > enemy_x:      # 플레이어가 오른쪽에 있으면
            move_x = self.speed
            
            self.show_motion = self.move_img[self.frame_index]
            self.frame_index = (self.frame_index + 1) % len(self.move_img)      # 움직이는 이미지 표시
            self.show_motion
        elif player_x < enemy_x:    # 플레이어가 왼쪽에 있으면
            move_x = -self.speed
            
            self.show_motion = self.move_img[self.frame_index].transpose(Image.FLIP_LEFT_RIGHT) # 이미지 반전
            self.frame_index = (self.frame_index + 1) % len(self.move_img)
        else:
            move_x = 0              # 플레이어와 x 좌표가 같으면 이동하지 않음
        
        # y 방향으로 이동
        if player_y > enemy_y:      # 플레이어가 아래에 있으면
            move_y = self.speed
        elif player_y < enemy_y:    # 플레이어가 위에 있으면
            move_y = -self.speed
        else:
            move_y = 0              # 플레이어와 y 좌표가 같으면 이동하지 않음
            
        distance =  np.linalg.norm(np.array([player_x - enemy_x, player_y - enemy_y]))
            
        if distance > min_distance:
            self.position[0] += move_x  # 적의 x 좌표 이동
            self.position[2] += move_x  # 적의 x2 좌표 이동 (오른쪽 끝)
            self.position[1] += move_y  # 적의 y 좌표 이동
            self.position[3] += move_y  # 적의 y2 좌표 이동 (아래쪽 끝)
        
        # 중심 좌표 갱신
        #self.position = np.array([self.x, self.y, self.x + self.x_size, self.y + self.y_size]) # 업데이트
        self.update_center()
        
        if distance <= min_distance:                    #적이 다가 왔다면
            self.approach = True
        else:
            self.approach = False
            
    
        
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
    
    def attack_player(self, current_time):
        self.show_motion = self.attack_img[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.move_img)      # 공격 이미지 표시
        
        if current_time - self.last_attack_time > 2:    # 2초가 지난 후에 공격
            player.damage(self.attack)                  # 플레이어에게 데미지 주기
            self.last_shot_time = current_time          # 마지막 공격 시간 갱신
            print(f"적이 플레이어를 공격! {self.attack} 데미지 입음")
    
'''-------------------------------------------------- 캐릭터 세팅 --------------------------------------------------'''

class Bullet:
    def __init__(self, last_key_pressed):
        self.speed = 10
        self.damage = 10
        self.state = None
        self.image = player_bullet[0]       # 별도의 파일에서 Image.open해서 로드함
        
        self.x_size, self.y_size = self.image.size
        
        offset_x = 55  # 플레이어 총구의 X축 위치 조정
        offset_y = 58  # 플레이어 총구의 Y축 위치 조정

        # 플레이어 위치와 오프셋을 기준으로 총알 위치 설정
        self.x = player.character_x + offset_x
        self.y = player.character_y + offset_y
        
        self.position = [self.x, self.y, self.x + self.x_size, self.y + self.y_size]
        
        self.direction = {'left' : False, 'right' : False}      # 좌우 확인

        if last_key_pressed == 'right':
            self.direction['right'] = True
        if last_key_pressed == 'left':
            self.direction['left'] = True
    
        
    def move(self):
        if self.direction['left']:
            self.x -= self.speed
            
        if self.direction['right']:
            self.x += self.speed
        
        self.position = [self.x, self.y, self.x + self.x_size, self.y + self.y_size] #위치 업데이트
        print(self.position, enemy.position)
          
           
    def collision_check(self, enemys):              # 적에게 맞았는지 확인
        print(type(enemys))
        
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                self.image = player_bullet[1]       # 이미지는 표시 되나 너무 빨라서 적용이 안되는 듯함
                enemy.state = 'die'
                self.state = 'hit'
    
    def draw(self, draw_surface): #현재 총알 이미지를 화면에 출력, (x, y) 좌표는 이미지의 좌상단을 기준으로 출력
        if player.last_key_pressed == 'right':
            draw_surface.paste(self.image, (self.x, self.y), self.image)  # 총알 이미지 출력
        else:
            draw_surface.paste(self.image.transpose(Image.FLIP_LEFT_RIGHT), (self.x, self.y), self.image.transpose(Image.FLIP_LEFT_RIGHT))
    
    def overlap(self, ego_position, other_position):
        """
        두 이미지가 겹치는지 확인하는 함수
        ego_position: [x, y, width, height] (총알)
        other_position: [x, y, width, height] (적)
        
        return:
            True: 겹침, False: 겹치지 않음
        """
        # print(f"총알 위치: {ego_position}, 적 위치: {other_position}")
             
        # 총알과 적이 겹치는지 확인
        return not (
            ego_position[2] < other_position[0] or  # image1의 오른쪽이 image2의 왼쪽보다 왼쪽
            ego_position[0] > other_position[2] or  # image1의 왼쪽이 image2의 오른쪽보다 오른쪽
            ego_position[3] < other_position[1] or  # image1의 아래쪽이 image2의 위쪽보다 위
            ego_position[1] > other_position[3]     # image1의 위쪽이 image2의 아래쪽보다 아래
        )
        
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

class Stage_set:
    def __init__(self, stage_level):
        self.stage_level = stage_level
        self.background = None
        self.enemy_type = None
        self.boss = None
        self.goal_enemy_kill = None
        self.spawn_enemy_num = None
        self.stage_setting()
    
    def stage_setting(self):
        if self.stage_level == 1:
            self.background = morning_background
            self.enemy_type = 'monsterLV1'
            self.boss = 'bossLV1'
            self.goal_enemy_kill = 20
            self.spawn_enemy_num = 3
        elif self.stage_level == 2:
            self.background = sunset_background
            self.enemy_type = 'monsterLV2'
            self.boss = 'bossLV2'
            self.goal_enemy_kill = 30
            self.spawn_enemy_num = 4
        elif self.stage_level == 3:
            self.background = midnight_background
            self.enemy_type = 'monsterLV3'
            self.boss = 'bossLV3'
            self.goal_enemy_kill = 40
            self.spawn_enemy_num = 5

'''-------------------------------------------------- 스테이지 세팅 --------------------------------------------------'''

# --------------------------------------------------------------------------- 게임 시작 전 설정 사항
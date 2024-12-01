'''
from setting import Joystick, Character, BackgroundScroller
from resource_img import morning_background, sunset_background, midnight_background
from PIL import Image
import time

# 조이스틱, 캐릭터 초기화
joystick = Joystick()
my_circle = Character(joystick.width, joystick.height)

# 배경 클래스 초기화
scroller = BackgroundScroller(morning_background, joystick.width, joystick.height)

# 디스플레이 초기화
combined_image = Image.new("RGB", (joystick.width, joystick.height))  # 디스플레이 이미지

# 캐릭터 초기 위치
character_x = joystick.width // 2 - my_circle.character_source.size[0] // 2
character_y = joystick.height // 2 - my_circle.character_source.size[1] // 2

# 캐릭터와 벽의 최소 거리 (버퍼)
buffer_x = 50
buffer_y = 30

# 메인 루프
while True:
    # 조이스틱 입력 처리
    if not joystick.button_U.value:  # 위쪽 이동
        if character_y > buffer_y:  # 캐릭터가 상단 버퍼를 벗어나지 않도록 이동
            character_y -= 5
    if not joystick.button_D.value:  # 아래쪽 이동
        if character_y < joystick.height - my_circle.character_source.size[1] - buffer_y:
            character_y += 5
    if not joystick.button_L.value:  # 왼쪽 이동
        if character_x > buffer_x:  # 캐릭터가 왼쪽 버퍼를 벗어나지 않도록 이동
            character_x -= 5
        else:
            scroller.leftScroll(step=5)  # 배경 이동
    if not joystick.button_R.value:  # 오른쪽 이동
        if character_x < joystick.width - my_circle.character_source.size[0] - buffer_x:
            character_x += 5
        else:
            scroller.rightScroll(step=5)  # 배경 이동

    # 배경 업데이트
    cropped_background = scroller.get_cropped_image()
    combined_image.paste(cropped_background, (0, 0))  # 배경 갱신

    # 캐릭터 업데이트
    combined_image.paste(my_circle.character_source, (character_x, character_y), mask=my_circle.character_source)

    # 디스플레이 출력
    joystick.disp.image(combined_image)

    # 프레임 딜레이
    time.sleep(0.03)
'''

import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import numpy as np

#from resource_img

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
        
class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        
        self.image_move = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_gif.gif')
        
        image_width, image_height = self.image_move.size
        
        self.position = np.array([width/2 - image_width/2, height/2 - image_height/2, 
                                  width/2 + image_width/2, height/2 + image_height/2])
        
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"
        self.health = 100 # 내 체력, 초기 체력은 100
        self.max_health = 100 # 치료를 염두해둔 최대 체력
        self.last_damage_time = 0  # 마지막으로 데미지를 받은 시간
        self.invincibility_time = 2  # 데미지 입지 않는 무적 타임 (2초)
        
    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
    
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
    
    def heal(self, heal_point):
        if(self.health <= self.max_health):
            self.health += heal_point
        else:
            self.health = self.max_health
                       
class Enemy:
    def __init__(self, spawn_position):
        self.appearance = 'circle'
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 25, spawn_position[1] - 25, spawn_position[0] + 25, spawn_position[1] + 25])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#00FF00"
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

class Bullet:
    def __init__(self, position, last_key_pressed):
        self.appearance = 'rectangle'
        self.speed = 10
        self.damage = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.state = None
        self.outline = "blue"


        if last_key_pressed == 'up':
            self.direction['up'] = True
        if last_key_pressed == 'down':
            self.direction['down'] = True
        if last_key_pressed == 'right':
            self.direction['right'] = True
        if last_key_pressed == 'left':
            self.direction['left'] = True

        
    def move(self):
        if self.direction['up']:
            self.position[1] -= self.speed
            self.position[3] -= self.speed

        if self.direction['down']:
            self.position[1] += self.speed
            self.position[3] += self.speed

        if self.direction['left']:
            self.position[0] -= self.speed
            self.position[2] -= self.speed
            
        if self.direction['right']:
            self.position[0] += self.speed
            self.position[2] += self.speed
            
    def collision_check(self, enemys):
        for enemy in enemys:
            collision = self.overlap(self.position, enemy.position)
            
            if collision:
                enemy.state = 'die'
                self.state = 'hit'

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
    
    def is_out_of_bounds(self, width, height):
        """
        총알이 화면 경계를 벗어났는지 확인하는 함수
        """
        x1, y1, x2, y2 = self.position
        return x2 < 0 or x1 > width or y2 < 0 or y1 > height

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


font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # 폰트 설정
font = ImageFont.truetype(font_path, 17)                            # 폰트 크기

joystick = Joystick()
my_image = Image.new("RGB", (joystick.width, joystick.height)) #도화지!
my_draw = ImageDraw.Draw(my_image) #그리는 도구!

character = Character(joystick.width, joystick.height)


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

def draw_health_bar(draw, position, width, height, health, max_health):     # 체력 바 생성
    """
    체력 바를 그리는 함수
    draw: ImageDraw 객체
    position: 체력 바의 중심 위치 (x, y)
    width, height: 체력 바 크기
    health: 현재 체력
    max_health: 최대 체력
    """
    x, y = position
    bar_length = width
    bar_height = height

    # 체력 비율에 따라 바의 길이 계산
    health_ratio = health / max_health
    filled_length = int(bar_length * health_ratio)

    # 체력 바 배경
    draw.rectangle(
        [x - bar_length // 2, y - bar_height // 2, x + bar_length // 2, y + bar_height // 2],
        fill=(128, 128, 128),  # 회색 배경
    )

    # 체력 바
    draw.rectangle(
        [x - bar_length // 2, y - bar_height // 2, x - bar_length // 2 + filled_length, y + bar_height // 2],
        fill=(0, 255, 0),  # 초록색 체력 바
    )
    
# 총알 맞았는지 확인하는 함수
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


# 잔상이 남지 않는 코드 & 대각선 이동 가능
my_circle = Character(joystick.width, joystick.height)
my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))
enemy_1 = Enemy((50, 50))
enemy_2 = Enemy((200, 200))
enemy_3 = Enemy((150, 50))

enemys_list = [enemy_1, enemy_2, enemy_3]   # 초기 적에 대한 리스트
enemy_bullets = []  # 적 총알 리스트
bullets = []        # 내 총알 리스트


last_key_pressed = None  # 마지막으로 누른 키
previous_button_state = True  # 버튼이 눌리지 않은 상태로 시작

'''
while True:
    command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
    if not joystick.button_U.value:  # up pressed
        command['up_pressed'] = True
        command['move'] = True
        last_key_pressed = "up"  # 마지막 키 기록

    if not joystick.button_D.value:  # down pressed
        command['down_pressed'] = True
        command['move'] = True
        last_key_pressed = "down"  # 마지막 키 기록

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        last_key_pressed = "left"  # 마지막 키 기록

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        last_key_pressed = "right"  # 마지막 키 기록

    current_button_state = joystick.button_A.value  # 현재 버튼 상태
    
    if not joystick.button_A.value: # A pressed
        if not current_button_state and previous_button_state:  # 버튼이 눌림 (이전엔 안 눌렸지만 지금 눌림)
            print(f"총알 발사! 방향: {last_key_pressed}")
            bullet = Bullet(my_circle.center, last_key_pressed)
            bullets.append(bullet)

    # 버튼 상태 갱신
    previous_button_state = current_button_state
            
    #print("마지막으로 누른 키", last_key_pressed)

    my_circle.move(command)
    
    #사용자 총알 위치 확인
    bullets_to_keep = []
    for bullet in bullets:
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"총알이 화면 밖으로 나갔습니다: {bullet.position}")
        elif bullet.state == 'hit':
            print(f"총알 충돌로 제거: {bullet.position}")
        else:
            bullet.collision_check(enemys_list)
            bullet.move()
            bullets_to_keep.append(bullet)  # 유효한 총알만 유지
    bullets = bullets_to_keep  # 유효한 총알로 리스트 업데이트
    
    #적이 총에 맞았다면 즉시 제거 됨
    remaining_enemies = []
    for enemy in enemys_list:
        if enemy.state == 'die':
            print(f"적 제거: {enemy.position}")
        else:
            remaining_enemies.append(enemy)  # 유효한 적만 유지
    enemys_list = remaining_enemies  # 유효한 적으로 리스트 업데이트
    
    
    # 적이 모두 제거되었을 경우 새로운 적 3개 생성
    if len(enemys_list) == 0:
        print("적이 모두 제거되었습니다. 새로운 적을 생성합니다!")
        enemys_list.extend(spawn_random_enemies(3, joystick.width, joystick.height))  # 적 추가
        
    
    # 적이 플레이어를 향해 이동하고 일정 시간마다 총알 발사
    current_time = time.time()
    for enemy in enemys_list:
        if enemy.state == 'alive':
            enemy.move_towards(my_circle.center, min_distance = 80)  # 플레이어를 향해 이동, 일정 거리 떨어져서 옴
            if current_time > enemy.last_shot_time + 1:  # 2초마다 발사
                enemy_bullet = enemy.shoot(my_circle.center)  # 플레이어 위치 전달
                enemy_bullets.append(enemy_bullet)
                enemy.last_shot_time = current_time  # 발사 시간 갱신
    
    # 적 총알 이동 및 화면 경계 처리       
    enemy_bullets_to_keep = []
    for bullet in enemy_bullets:
        bullet.move()
        
        # 플레이어와 충돌 확인
        if check_collision(bullet.position, my_circle.position):
            print("플레이어가 적의 총알에 맞았습니다!")
            if my_circle.damage(10):  # 체력 감소 (10만큼 데미지)
                break                                                   #우선 for문 먼저 나옴
            bullet.state = 'hit'  # 충돌한 총알 상태를 변경
            continue  # 해당 총알은 더 이상 처리하지 않도록 다음 총알로 넘어감
        
        # 적 총알 위치 확인    
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"적 총알 제거: {bullet.position}")
        else:
            enemy_bullets_to_keep.append(bullet)
    enemy_bullets = enemy_bullets_to_keep  # 유효한 총알만 유지
    
    
    # 텍스트 정보 생성
    num_bullets = len(bullets) + len(enemy_bullets)  # 총알 개수
    num_enemies = len(enemys_list)  # 적 개수
    status_text = f"Bullets: {num_bullets}\nEnemies: {num_enemies}"  # 텍스트 내용
    
    
    # ------------------------------------------------------------------------------------------------------------------------------------------ 출력 부분
    
    
    #그리는 순서가 중요합니다. 배경을 먼저 깔고 위에 그림을 그리고 싶었는데 그림을 그려놓고 배경으로 덮는 결과로 될 수 있습니다.
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (255, 255, 255, 100))                                 # 배경
    my_draw.ellipse(tuple(my_circle.position), outline = my_circle.outline, fill = (0, 0, 0))
    
    for enemy in enemys_list:
        if enemy.state != 'die':
            my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0)) # 적 그리기

    for bullet in bullets:
        if bullet.state != 'hit':
            my_draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255)) # 플레이어 총알 그리기
            
    for bullet in enemy_bullets:
        my_draw.rectangle(tuple(bullet.position), outline=bullet.outline, fill=(255, 0, 0))  # 적 총알 그리기
    
    
    # 체력 바 그리기
    health_bar_position = (int(my_circle.center[0]), int(my_circle.position[1]) - 15)  # 플레이어 상단 위치
    draw_health_bar(my_draw, health_bar_position, width=80, height=5, health=my_circle.health, max_health=my_circle.max_health)
            
    # 텍스트 출력 (왼쪽 아래)
    text_x = 10
    text_y = joystick.height - 40  # 화면 아래로 40px 위
    my_draw.text((text_x, text_y), status_text, font=font, fill="#000000")  # 검은색 텍스트

    #좌표는 동그라미의 왼쪽 위, 오른쪽 아래 점 (x1, y1, x2, y2)
    joystick.disp.image(my_image)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------ 검사 부분
    
    # 체력 0 이하로 루프를 빠져나온 경우
    if my_circle.health <= 0:
        break                                                           # <-여기서 while문에서 빠지게 돰
    
'''


while True: 
    command = {'move': False, 'up_pressed': False , 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}
    
    if not joystick.button_U.value:  # up pressed
        command['up_pressed'] = True
        command['move'] = True
        last_key_pressed = "up"  # 마지막 키 기록

    if not joystick.button_D.value:  # down pressed
        command['down_pressed'] = True
        command['move'] = True
        last_key_pressed = "down"  # 마지막 키 기록

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        last_key_pressed = "left"  # 마지막 키 기록

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        last_key_pressed = "right"  # 마지막 키 기록
        
    current_button_state = joystick.button_A.value  # 현재 버튼 상태
    
    if not joystick.button_A.value: # A pressed
        if not current_button_state and previous_button_state:  # 버튼이 눌림 (이전엔 안 눌렸지만 지금 눌림)
            print(f"총알 발사! 방향: {last_key_pressed}")
            bullet = Bullet(character.center, last_key_pressed)
            bullets.append(bullet)

    # 버튼 상태 갱신
    previous_button_state = current_button_state
        
    character.move(command)
    
     #사용자 총알 위치 확인
    bullets_to_keep = []
    for bullet in bullets:
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"총알이 화면 밖으로 나갔습니다: {bullet.position}")
        elif bullet.state == 'hit':
            print(f"총알 충돌로 제거: {bullet.position}")
        else:
            bullet.collision_check(enemys_list)
            bullet.move()
            bullets_to_keep.append(bullet)  # 유효한 총알만 유지
    bullets = bullets_to_keep  # 유효한 총알로 리스트 업데이트
    
    #적이 총에 맞았다면 즉시 제거 됨
    remaining_enemies = []
    for enemy in enemys_list:
        if enemy.state == 'die':
            print(f"적 제거: {enemy.position}")
        else:
            remaining_enemies.append(enemy)  # 유효한 적만 유지
    enemys_list = remaining_enemies  # 유효한 적으로 리스트 업데이트
    
    
    # 적이 모두 제거되었을 경우 새로운 적 3개 생성
    if len(enemys_list) == 0:
        print("적이 모두 제거되었습니다. 새로운 적을 생성합니다!")
        enemys_list.extend(spawn_random_enemies(3, joystick.width, joystick.height))  # 적 추가
        
    
    # 적이 플레이어를 향해 이동하고 일정 시간마다 총알 발사
    current_time = time.time()
    for enemy in enemys_list:
        if enemy.state == 'alive':
            enemy.move_towards(character.center, min_distance = 80)  # 플레이어를 향해 이동, 일정 거리 떨어져서 옴
            if current_time > enemy.last_shot_time + 1:  # 2초마다 발사
                enemy_bullet = enemy.shoot(character.center)  # 플레이어 위치 전달
                enemy_bullets.append(enemy_bullet)
                enemy.last_shot_time = current_time  # 발사 시간 갱신
    
    # 적 총알 이동 및 화면 경계 처리       
    enemy_bullets_to_keep = []
    for bullet in enemy_bullets:
        bullet.move()
        
        # 플레이어와 충돌 확인
        if check_collision(bullet.position, character.position):
            print("플레이어가 적의 총알에 맞았습니다!")
            if character.damage(10):  # 체력 감소 (10만큼 데미지)
                break                                                   #우선 for문 먼저 나옴
            bullet.state = 'hit'  # 충돌한 총알 상태를 변경
            continue  # 해당 총알은 더 이상 처리하지 않도록 다음 총알로 넘어감
        
        # 적 총알 위치 확인    
        if bullet.is_out_of_bounds(joystick.width, joystick.height):
            print(f"적 총알 제거: {bullet.position}")
        else:
            enemy_bullets_to_keep.append(bullet)
    enemy_bullets = enemy_bullets_to_keep  # 유효한 총알만 유지
    
    
    # 텍스트 정보 생성
    num_bullets = len(bullets) + len(enemy_bullets)  # 총알 개수
    num_enemies = len(enemys_list)  # 적 개수
    status_text = f"Bullets: {num_bullets}\nEnemies: {num_enemies}"  # 텍스트 내용
    
    x1, y1, x2, y2 = character.position

   
    
    
    # --------------------------------------------------------------------
    

    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill = (0, 255, 255, 100)) # 배경
    my_image.paste(character.image_move, (int(x1), int(y1)))                              # 플레이어
    
    for enemy in enemys_list:
        if enemy.state != 'die':
            my_draw.ellipse(tuple(enemy.position), outline = enemy.outline, fill = (255, 0, 0)) # 적 그리기

    for bullet in bullets:
        if bullet.state != 'hit':
            my_draw.rectangle(tuple(bullet.position), outline = bullet.outline, fill = (0, 0, 255)) # 플레이어 총알 그리기
            
    for bullet in enemy_bullets:
        my_draw.rectangle(tuple(bullet.position), outline=bullet.outline, fill=(255, 0, 0))  # 적 총알 그리기
    
    
    # 체력 바 그리기
    health_bar_position = (int(character.center[0]), int(character.position[1]) - 15)  # 플레이어 상단 위치
    draw_health_bar(my_draw, health_bar_position, width=80, height=5, health=character.health, max_health=character.max_health)
            
    # 텍스트 출력 (왼쪽 아래)
    text_x = 10
    text_y = joystick.height - 40  # 화면 아래로 40px 위
    my_draw.text((text_x, text_y), status_text, font=font, fill="#000000")  # 검은색 텍스트

    
    joystick.disp.image(my_image)


print("게임 종료")
from setting import *
from resource_img import *
import time, random


#조이스틱, 캐릭터 초기화
joystick = Joystick()
player = Player(width = joystick.width, 
                height = joystick.height, 
                character_size_x = 96, 
                character_size_y = 96) #캐릭터 사이즈 96 x 96


display = Image.new("RGB", (joystick.width, joystick.height))           # 디스플레이 초기화

draw_bar = ImageDraw.Draw(display)                                      # 체력 바 및 경고창을 그리기 위한 draw

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"      # 폰트 설정
font = ImageFont.truetype(font_path, 25)                                # 폰트 크기, 게임 클리어에서 쓰임
sub_font = ImageFont.truetype(font_path, 17)                            # 폰트 크기, 게임 오버 됬을 때 쓰임


goalState = False                               # 스테이지가 끝났음을 확인하기 위한 변수
gameover = False                                # 

def player_bullet_fire(player):                 # 플레이어 총알 발사
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
        bullet = Bullet(player.last_key_pressed, player.character_x, player.character_y)
        bullets.append(bullet)

def spawn_random_enemies(num_enemies):          # 적 랜덤으로 생성, num_enemies 생성할 적의 리스트를 받음
    if stage.enemy_type == 'monsterLV1':
        enemy_config = {
            'move': monsterLV1_move,
            'attack': monsterLV1_attack,
            'hurt': monsterLV1_hurt,
            'dead': monsterLV1_dead,
            'attack_power': 20,
            'speed': 1,
            'health': 50
        }
    elif stage.enemy_type == 'monsterLV2':
        enemy_config = {
            'move': monsterLV2_move,
            'attack': monsterLV2_attack,
            'hurt': monsterLV2_hurt,
            'dead': monsterLV2_dead,
            'attack_power': 10,
            'speed': 2,
            'health': 100
        }
    elif stage.enemy_type == 'monsterLV3':
        enemy_config = {
            'move': monsterLV3_move,
            'attack': monsterLV3_attack,
            'hurt': monsterLV3_hurt,
            'dead': monsterLV3_dead,
            'attack_power': 20,
            'speed': 1,
            'health': 150
        }
        
    
    new_enemies = []
    for _ in range(num_enemies):
        random_x = random.choice([random.randint(0, 0), random.randint(joystick.width - 40, joystick.width)]) 
        random_y = random.randint(player.y_limit_midnight + 50, player.y_bottom_limit)

        # Enemy 클래스 인스턴스 생성, 여기서 생성되는 몹들은 보스가 아니기에 boss는 False로 반환
        new_enemy = Enemy(
            move = enemy_config['move'],
            attack = enemy_config['attack'],
            hurt = enemy_config['hurt'],
            dead = enemy_config['dead'],
            spawn_position = (random_x, random_y),
            attack_power = enemy_config['attack_power'],
            speed = enemy_config['speed'],
            health = enemy_config['health'],
            boss = False
        )
        new_enemies.append(new_enemy)
    return new_enemies

def spawn_boss():                               # 보스 생성하기
    if stage.boss == 'bossLV1':
        print("LV1")
        enemy_config = {
            'move': bossLV1_move,
            'attack': bossLV1_attack,
            'hurt': bossLV1_hurt,
            'dead': bossLV1_dead,
            'attack_power': 10,
            'speed': 1,
            'health': 50
        }
    elif stage.boss == 'bossLV2':
        print("LV2")
        enemy_config = {
            'move': bossLV2_move,
            'attack': bossLV2_attack,
            'hurt': bossLV2_hurt,
            'dead': bossLV2_dead,
            'attack_power': 20,
            'speed': 2,
            'health': 100
        }
    elif stage.boss == 'bossLV3':
        print("LV3")
        enemy_config = {
            'move': bossLV3_move,
            'attack': bossLV3_attack,
            'hurt': bossLV3_hurt,
            'dead': bossLV3_dead,
            'attack_power': 10,
            'speed': 2,
            'health': 150
        }

    random_x = random.randint(joystick.width - 50, joystick.width)  # 보스 위치를 화면의 오른쪽 끝 근처로 설정
    random_y = random.randint(player.y_limit_midnight + 50, player.y_bottom_limit)

    # 보스의 속성 설정 (보스는 다른 몹과 다름으로 boss = True를 반환함)
    make_boss = Enemy(
            move = enemy_config['move'],
            attack = enemy_config['attack'],
            hurt = enemy_config['hurt'],
            dead = enemy_config['dead'],
            spawn_position = (random_x, random_y),
            attack_power = enemy_config['attack_power'],
            speed = enemy_config['speed'],
            health = enemy_config['health'],
            boss = True
        )
    enemys_list.append(make_boss)  # 보스를 적 목록에 추가

def is_boss_check(enemys_list):                 # 적 리스트를 순회하면서 보스가 있는지 확인
    for enemy in enemys_list:
        if enemy.boss_check:  # 보스 여부 확인
            return True  # 보스가 존재하면 True 반환
    return False  # 보스가 없다면 False 반환

def game(set_level):                            # 게임 실행 함수
    global bullets, enemys_list, goalState, stage, gameover                              # 글로벌로 선언하여 다른 함수들도 참조 가능하도록
    


    if goalState == True:
        print("goal state", goalState)
        return False
    
    stage = Stage_set(stage_level = set_level)  # 스테이지 정하기 --------------------------------------------------------------------------------
    scroller = BackgroundScroller(stage.background, joystick.width, joystick.height)    # 배경 클래스 초기화

    player.player_state_reset()
    
    enemys_list = []    # 적 리스트
    bullets = []        # 내 총알 리스트
    
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

        if not joystick.button_R.value:  # right pressed
            command['right_pressed'] = True
            command['move'] = True
        
        # ------------------------------------------------------------------------ 플레이어 총알 발사
        global current_button_state                     # 현재 버튼 상태
        current_button_state = joystick.button_A.value
        if not joystick.button_A.value and player.previous_button_state: # A pressed
            player_bullet_fire(player)        # 발사 모션

        # 버튼 상태 갱신
        player.previous_button_state = current_button_state
        
        # ------------------------------------------------------------------------ 플레이어 및 적 이동 확인
        player.move(scroller, stage, command) #플레이어 이동 갱신
        
        # ----------------------------------------------------------------------- 총알들의 유효성 및 피격 여부
        
        # 사용자 총알 위치 확인
        bullets_to_keep = []
        for bullet in bullets:
            if bullet.is_out_of_bounds(joystick.width, joystick.height):
                print(f"총알이 화면 밖으로 나갔습니다: {bullet.x} {bullet.y}")
            elif bullet.state == 'hit':
                print(f"총알 충돌로 제거: {bullet.x} {bullet.y}")
            else:
                bullet.move(enemy)
                bullet.collision_check(enemys_list)
                bullets_to_keep.append(bullet)  # 유효한 총알만 유지
        bullets = bullets_to_keep               # 유효한 총알로 리스트 업데이트
        
        
        #적이 총에 맞았다면 즉시 제거 됨
        remaining_enemies = []
        for enemy in enemys_list:
            # print("코드테스트")            
            if enemy.boss_check:  # 적 캐릭터가 보스일 경우
                if enemy.health > 0:  # 보스가 살아있다면
                    enemy.health -= bullet.damage  # 총알 데미지만큼 체력 감소
                else:
                    if enemy.state != 'die':  # 보스가 죽었을 때만 상태 변경
                        enemy.state = 'die'   # 보스 죽음 처리
                        print(f"보스가 쓰러졌습니다! 위치: {enemy.position}")
            else:
                if enemy.state == 'die':
                    player.killed_enemy += 1              # 적 사살횟수 증가
                    print(f"적 제거: {enemy.position} / {player.killed_enemy}")
                else:
                    remaining_enemies.append(enemy)       # 유효한 적만 유지

        enemys_list = remaining_enemies          # 유효한 적으로 리스트 업데이트
        
        
        # 적이 모두 제거되었을 경우 새로운 적 3개 생성
        if len(enemys_list) == 0 and player.killed_enemy <= stage.goal_enemy_kill: # 목표치에 도달하기 전까지 생성       
            print("새로운 적을 생성합니다!")
            enemys_list.extend(spawn_random_enemies(stage.spawn_enemy_num))  # 적 추가 생성, 스테이지별로 생성 횟수 다름    
        
        
        # 적이 플레이어를 향해 이동하고 일정 시간마다 공격
        current_time = time.time()
        for enemy in enemys_list:
            if enemy.state == 'alive':
                enemy.move_towards(player.center, min_distance = 35)  # 플레이어를 향해 이동, 일정 거리 떨어져서 옴
                if enemy.approach:
                    enemy.attack_player(current_time, player)         # 지정한 거리 이내로 다가오면 공격하기

        # -------------------------------------- --------------------------------------------- 출력 부분
            
        cropped_background = scroller.get_cropped_image()   # 현재 스크롤 상태에 맞게 이미지를 가져옴
        display.paste(cropped_background, (0, 0))           # 배경 출력
        
        for enemy in enemys_list:
            if enemy.state != 'die':
                display.paste(enemy.show_motion, (enemy.position[0], enemy.position[1]), enemy.show_motion)   
                
        if player.health <= 0:                      # 플레이어 체력이 0이하면 
            for _ in range(len(player_dead)):
                player.player_die()
            draw_bar.text((40, 180), "Game Over!", font=font, fill=(255, 0, 0))
            
            draw_bar.text((60, 210), "B : Restart", font=sub_font, fill=(0, 255, 0))
            goalState = True

        display.paste(player.show_player_motion, (player.character_x, player.character_y), player.show_player_motion)  # 플레이어 출력
        player.player_health_bar(draw_bar)
        
        for bullet in bullets:                  # 플레이어 총알
            if bullet.state != 'hit':
                bullet.draw(display, player)    # 총알 이미지 출력
                
        if len(enemys_list) == 0 and player.killed_enemy >= stage.goal_enemy_kill:
            draw_bar.text((30, 150), f"{stage.stage_level} Level Clear! ", font=font, fill=(0, 0, 255))
            if stage.stage_level == 3:
                draw_bar.text((60, 210), "B : Restart", font=sub_font, fill=(0, 255, 0))
            goalState = True

        joystick.disp.image(display)
        
        if goalState:
            joystick.disp.image(display)
            time.sleep(2)
            break
        
        # 프레임 딜레이
        time.sleep(0.01)  # 짧은 시간 딜레이

    print("플레이어 상태 확인", player.state)

    if player.state == 'dead':
        print(f"stage {stage.stage_level} : 게임 실패")
        gameover = True
        return
    else:
        print(f"stage {stage.stage_level} : 게임 클리어")
        return True


set_level = 1                                   # 처음 스테이지 레벨


while True:                                     # 게임 무한 반복함
    
    goalState = False
    game(set_level)
    set_level += 1
    
    if gameover or set_level == 4:
        while True:
            #print("조이스틱 입력")
            if not joystick.button_B.value:
                set_level = 1
                gameover = False
                break

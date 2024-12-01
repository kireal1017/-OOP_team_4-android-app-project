from collections import namedtuple
from PIL import Image

absolute_path = '/home/j9077/working_directory/' #혹시 모를 절대경로, 이유는 모르겠으나 상대경로를 쓰면 에러가 발생함


morning_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_midnight.png')
start_logo = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/start_logo_120x100.png')

player_sprites = namedtuple('player', ['wait', 'move', 'attack', 'hit', 'die', 'jump']) #namedtuple로 일일히 변수를 만들기 보단 구조체로 묶음
# 플레이어
player = player_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Run.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Shot.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Dead.png'),
    jump = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/Jump.png')
)

monster_sprites = namedtuple('monster', ['wait', 'move', 'attack', 'hit', 'die'])

# enemy Lv1 거북이
turtle = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/Walk.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/Death.png'),
)

# enemy lv2 전기 뱀장어 그냥 electricMob이라 할래
electric_mob = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV2/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV2/Walk.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV2/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV2/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV2/Death.png'),
)

# enemy Lv3 심해 아귀, 얘도 귀찮으니깐 deepFish라 함
deep_fish = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/Walk.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/Death.png'),
)

# boss Lv1 어부 
fisherman = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV1/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV1/Walk.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV1/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV1/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV1/Death.png'),
)

# boss Lv2 용궁의 전사, 쓰기 귀찮으니 그냥 전사라 함
warrier = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Walk2.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Death.png'),
)

# boss Lv3 고대 해군
ancient_navy = monster_sprites(
    wait = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Idle.png'),
    move = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Walk.png'),
    attack = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Attack.png'),
    hit = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Hurt.png'),
    die = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Death.png'),
)


bullet_sprites = namedtuple('bullet', ['player', 'fisherman', 'warrier'])

bullet = bullet_sprites(
    player = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/player/player_bullet1.png'),
    fisherman = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV2/Projectile.png'),
    warrier = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/character/enemy_boss/bossLV3/Arrow1.png')
)
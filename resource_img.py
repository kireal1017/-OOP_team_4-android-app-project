from collections import namedtuple
from PIL import Image

absolute_path = '/home/j9077/working_directory/' #혹시 모를 절대경로



morning_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_midnight.png')
start_logo = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/start_logo_120x100.png')

CharacterSprites = namedtuple('CharacterSprites', ['wait', 'move', 'attack', 'hit', 'die']) #namedtuple로 일일히 변수를 만들기 보단 구조체로 묶음

'''

# 플레이어
player = CharacterSprites(
    wait = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/character/player/Idle.png'),
    move = Image.open('/path/to/player_move.png'),
    attack = Image.open('/path/to/player_attack.png'),
    hit = Image.open('/path/to/player_hit.png'),
    die = Image.open('/path/to/player_die.png'),
)

# enemy Lv1 거북이
turtle = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

# enemy lv2 전기 뱀장어 그냥 electricMob이라 할래
electric_mob = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

# enemy Lv3 심해 아귀, 얘도 귀찮으니깐 deepFish라 함
deep_fish = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

# boss Lv1 어부 
fisherman = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

# boss Lv2 용궁의 전사, 쓰기 귀찮으니 그냥 전사라 함
warrier = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

# boss Lv3 고대 해군
ancient_navy = CharacterSprites(
    wait = Image.open('/path/to/turtle_wait.png'),
    move = Image.open('/path/to/turtle_move.png'),
    attack = Image.open('/path/to/turtle_attack.png'),
    hit = Image.open('/path/to/turtle_hit.png'),
    die = Image.open('/path/to/turtle_die.png'),
)

'''
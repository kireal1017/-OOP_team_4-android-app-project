from collections import namedtuple
from PIL import Image

absolute_path = '/home/j9077/working_directory/' #혹시 모를 절대경로, 이유는 모르겠으나 상대경로를 쓰면 에러가 발생함

morning_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/background/background_midnight.png')
start_logo = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/start_logo_120x100.png')

player_path = 'esw_raspberryPi_game_project/image_source/character/player/'

player_wait = Image.open(absolute_path + player_path + 'playerWait.png').convert("RGBA")


player_move = [
    Image.open(absolute_path + player_path + 'player1.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player2.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player3.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player4.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player5.png').convert("RGBA"),
]

player_shoot = [
    player_wait,
    Image.open(absolute_path + player_path + 'player_shoot1.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_shoot2.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_shoot3.png').convert("RGBA"),
    player_wait
]

player_bullet = [
    Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/bullet_asset/player_bullet1.png').convert("RGBA"),
    Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/bullet_asset/player_bullet2.png').convert("RGBA")
]


player_hurt = [
    Image.open(absolute_path + player_path + 'player_hunt1.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_hunt2.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_hunt3.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_hunt4.png').convert("RGBA")
]

player_dead = [
    Image.open(absolute_path + player_path + 'player_dead1.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_dead2.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_dead3.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_dead4.png').convert("RGBA"),
    Image.open(absolute_path + player_path + 'player_dead5.png').convert("RGBA")
]


monsterLV1_path = 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV1/'

monsterLV1_move = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk6.png').convert("RGBA")
]

monsterLV1_attack = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack6.png').convert("RGBA")
] 

monsterLV1_hurt = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Hurt1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Hurt2.png').convert("RGBA")
]

monsterLV1_dead = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death6.png').convert("RGBA")
]


monsterLV1_path = 'esw_ra1pberryPi_game_project/image_source/character/enemy/monsterLV2/'

monsterLV2_move = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Walk6.png').convert("RGBA")
]

monsterLV2_attack = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Attack6.png').convert("RGBA")
] 

monsterLV2_hurt = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Hurt1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Hurt2.png').convert("RGBA")
]

monsterLV2_dead = [
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV1_path + 'moster1_Death6.png').convert("RGBA")
]

monsterLV3_path = 'esw_raspberryPi_game_project/image_source/character/enemy/monsterLV3/'

monsterLV3_move = [
    Image.open(absolute_path + monsterLV3_path + 'moster3_Walk1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Walk2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Walk3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Walk4.png').convert("RGBA")
]

monsterLV3_attack = [
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Attack6.png').convert("RGBA")
]

monsterLV3_hurt = [
    Image.open(absolute_path + monsterLV3_path + 'moster3_Hurt1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Hurt2.png').convert("RGBA")   
]

monsterLV3_dead = [
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death1.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death2.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death3.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death4.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death5.png').convert("RGBA"),
    Image.open(absolute_path + monsterLV3_path + 'moster3_Death6.png').convert("RGBA")
]


enemy_test = Image.open(absolute_path + 'esw_raspberryPi_game_project/image_source/test_gif.gif').convert("RGBA")
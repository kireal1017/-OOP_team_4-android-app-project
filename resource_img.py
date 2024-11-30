from PIL import Image

morning_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_midnight.png')

start_logo = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/start_logo_120x100.png')

player_proto = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/test_70.png')  #대기
player_move_proto = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/character/player/character_move_right_2.png') #이동


print(player_proto)
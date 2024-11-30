from PIL import Image
import os

print(os.getcwd)

morning_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_evening.png')
sunset_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_sunset.png')
midnight_background = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/background/background_midnight.png')

start_logo = Image.open('/home/j9077/working_directory/esw_raspberryPi_game_project/image_source/start_logo_120x100.png')

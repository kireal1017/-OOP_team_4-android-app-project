import subprocess

from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
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

# 게임 오버 상태 체크 변수
game_over = False

joystick = Joystick()

# 실행할 파일 목록
files = ['/home/j9077/working_directory/esw_raspberryPi_game_project/stage_1.py', 
        '/home/j9077/working_directory/esw_raspberryPi_game_project/stage_2.py', 
        '/home/j9077/working_directory/esw_raspberryPi_game_project/stage_3.py']

def run_game(files):
    global game_over  # game_over 상태 확인
    # 게임 루프
    for file in files:
        print("game", game_over)
        if game_over:   # 게임 오버 상태일 경우, 이후 파일들은 실행되지 않음
            print("게임 오버 나머지 파일은 실행되지 않음")
            break       # 게임 오버가 되면 더 이상 파일을 실행하지 않고 루프 종료

        print(f"현재 실행 중인 파일 : {file}")
        result = subprocess.run(['python', file]) # 파일 실행

        if "GAME_OVER" in result.stdout:  # 파일에서 출력된 'GAME_OVER' 확인
            print("게임 오버 상태 확인")
            game_over = True  # 게임 오버 상태로 변경
            break  # 게임 오버가 되면 파일 실행을 중단


        # 게임 실행 중 게임 오버 상태가 되면
        if result.returncode != 0:      # 오류가 발생한 경우 게임 오버 처리
            print("오류 확인")
            game_over = True            # 게임 오버 상태로 변경        
            while True:                                                             # 게임 오버되었을 때 B 버튼을 눌러서 재실행 가능함
                if not joystick.button_B.value:
                    print("게임 재시작")
                    game_over = False   # 게임 오버 상태 초기화
                    run_game(files)     # 게임을 다시 시작하는 함수 호출
                    break               # 게임 루프를 다시 시작하게 하기 위해 현재 루프를 종료
    

run_game(files) # 최초 게임 실행
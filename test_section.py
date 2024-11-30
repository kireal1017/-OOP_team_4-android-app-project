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
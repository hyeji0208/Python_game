from ursina import *
import random

app = Ursina()

# 엔딩화면
ending_screen = Entity(
    model='quad',
    texture='graphic/s최종.png',
    scale=(14.6, 8.2)
)

# 엔딩bgm
end_bgm = Audio('bgm/엔딩.mp3', volume=1, pitch=1, loop=True, autoplay=True, auto_destroy=True)

# 다시하기 버튼
retry_button = Button(
    model='quad',
    texture='graphic/retrybutton.png',
    scale=(0.22, 0.07),
    position=(-0.7, -0.42),
    color=color.white,
    highlight_color=color.gray,
    pressed_color=color.white
)

app.run()
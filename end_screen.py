from ursina import *

# 윈도우 생성
app = Ursina()

# 엔딩 화면
end_screen = Entity(
    model='quad',
    texture='graphic/main.png',
    scale=(14.6, 8.2)
)
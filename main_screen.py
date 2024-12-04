from ursina import *

# 윈도우 생성
app = Ursina()

#메인 배경화면

main_screen = Entity(
    model='quad',
    texture='graphic/main.png',              
    scale=(14.6, 8.2)               
)

# bgm
main_bgm = Audio(sound_file_name='bgm/게임 메인.mp3', volume=1, pitch=1, loop=True, autoplay=True, auto_destroy=True)

# 시작버튼
start_button = Button(
    model='quad',
    texture = 'graphic/startbutton.png',
    scale=(0.416, 0.13),
    position=(0.34, -0.334),
    color= color.white,
    highlight_color = color.gray,
    pressed_color = color.white
    )

# 설명버튼
explain_button = Button(
    model='quad',
    texture = 'graphic/explainbutton.png',
    scale=(0.416, 0.13),
    position=(-0.33, -0.334),
    color= color.white,
    highlight_color = color.gray,
    pressed_color = color.white
    )

# 게임설명창
explain_screen = Entity(
    model='quad',
    texture='graphic/explain.png',              
    scale=(14.6, 8.2),
    position=(3, 6),
    enabled=False             
)

def explain():
    main_screen.texture = 'graphic/explain.png'
    explain_button.disable()
    start_button.disable()
    back_button.enable()
    start1_button.enable()
  
# 되돌아가기 버튼
back_button = Button(
    model='quad',
    texture = 'graphic/back.png',
    scale=(0.22, 0.09),
    position=(-0.7, -0.39),
    color= color.white,
    highlight_color = color.gray,
    pressed_color = color.white,
    enabled = False
    )

# 설명창 시작 버튼
start1_button = Button(
    model='quad',
    texture = 'graphic/start1.png',
    scale=(0.22, 0.09),
    position=(0.7, -0.39),
    color= color.white,
    highlight_color = color.gray,
    pressed_color = color.white,
    enabled = False
    )

# 메인화면 되돌아가기
def main():
    main_screen.texture = 'graphic/main.png'
    explain_button.enable()
    start_button.enable()
    back_button.disable()
    start1_button.disable()

explain_button.on_click = explain
back_button.on_click = main

# start_button.on_click = start_game

app.run()
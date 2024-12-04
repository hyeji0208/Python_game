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

# button
start_button = Button(
    model='quad',
    texture = 'graphic/startbutton.png',
    scale=(0.416, 0.13),
    position=(0.34, -0.334),
    color= color.white,
    highlight_color = color.white,
    pressed_color = color.white
    )


# start_button.on_click = start_game

app.run()
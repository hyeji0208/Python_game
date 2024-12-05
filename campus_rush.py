from ursina import *
import random


# 윈도우 생성
app = Ursina()

# ---------------------------
# 메인 화면 설정
# ---------------------------

main_screen = Entity(
    model='quad',
    texture='graphic/main.png',
    scale=(14.6, 8.2)
)

# BGM
main_bgm = Audio('bgm/게임 메인.mp3', volume=1, pitch=1, loop=True, autoplay=True, auto_destroy=True)

# 시작 버튼
start_button = Button(
    model='quad',
    texture='graphic/startbutton.png',
    scale=(0.416, 0.13),
    position=(0.34, -0.334),
    color=color.white,
    highlight_color=color.gray,
    pressed_color=color.white
)

# 설명 버튼
explain_button = Button(
    model='quad',
    texture='graphic/explainbutton.png',
    scale=(0.416, 0.13),
    position=(-0.33, -0.334),
    color=color.white,
    highlight_color=color.gray,
    pressed_color=color.white
)

# 게임 설명창
explain_screen = Entity(
    model='quad',
    texture='graphic/explain.png',
    scale=(14.6, 8.2),
    position=(3, 6),
    enabled=False
)

# 설명 함수
def explain():
    main_screen.texture = 'graphic/explain.png'
    explain_button.disable()
    start_button.disable()
    back_button.enable()
    start1_button.enable()

# 되돌아가기 버튼
back_button = Button(
    model='quad',
    texture='graphic/back.png',
    scale=(0.22, 0.09),
    position=(-0.7, -0.39),
    color=color.white,
    highlight_color=color.gray,
    pressed_color=color.white,
    enabled=False
)

# 설명창에서 게임 시작 버튼
start1_button = Button(
    model='quad',
    texture='graphic/start1.png',
    scale=(0.22, 0.09),
    position=(0.7, -0.39),
    color=color.white,
    highlight_color=color.gray,
    pressed_color=color.white,
    enabled=False
)

# 메인 화면으로 돌아가기
def main():
    main_screen.texture = 'graphic/main.png'
    explain_button.enable()
    start_button.enable()
    back_button.disable()
    start1_button.disable()

back_button.on_click = main
explain_button.on_click = explain

# ---------------------------
# 게임 화면 설정
# ---------------------------

# 맵 한정하기
pos = [-2, 0, 2]

# 점수 표시
global score
score = 0
elapsed_time = 0
score_text = Text(f"Score: {score}", position=(-0.77, 0.43), scale=2, color=color.black, enabled = False)

# 게임 배경화면
background = Entity(
    model='quad',
    texture='graphic/game.png',
    scale=(40, 25, 1),              
    position=(0, -2.5, 50),         
)   

# bgm
game_bgm = Audio(sound_file_name='bgm/게임 시작.mp3', volume=0, loop=True, autoplay=True, auto_destroy=True) #게임중 bgm

# 플레이어 걷는 애니메이션
# 플레이어 텍스쳐
player_textures = ['graphic/player1.png', 'graphic/player2.png']
player_textures2 = ['graphic/player3.png', 'graphic/player4.png']
current_texture_index = 0

# 플레이어 생성
player = Entity(
    model='quad',
    texture=player_textures[current_texture_index],
    scale=(2, 2, 2),
    position=(0, 0,0),
    collider = 'sphere',
    enabled=False
)

# 무적상태
global invincible
invincible = False 

# 텍스처 변경 함수
def switch_texture():
    global current_texture_index, invincible
    if invincible == True:
        current_texture_index = (current_texture_index + 1) % len(player_textures2) 
        player.texture = player_textures2[current_texture_index]
    else:
        current_texture_index = (current_texture_index + 1) % len(player_textures) 
        player.texture = player_textures[current_texture_index]
    invoke(switch_texture, delay=0.5)

# 애니메이션 시작
switch_texture()

# 체력 생성
global health
max_health = 3
health = max_health
hearts = []

for i in range(max_health):
    heart = Entity(
    model='quad',
    texture='graphic/health.png',
    position=(2.1 + i * 0.4, 2.97),
    scale=(0.47, 0.47),
    enabled=False
    )
    hearts.append(heart)

# 체력감소함수
def reduce_health():
    global health, invincible
    if invincible != True: # 무적 상태가 아닐 경우 체력 감소
        health -= 1
        if health >= 0:
            hearts[health].enabled = False

# 아이템 효과 함수
# 체력 아이템 (체력증가)
def plus_health():
    global health
    if health < 3:
        hearts[health].enabled = True
        health += 1

# 휴학신청서 아이템 (무적)
def rest():
    global invincible
    invincible = True
    invoke (rest_off, delay=5)

def rest_off():
    global invincible
    invincible = False

# 장애물 종류 정의
block_types = [
{'name': 'task','model': 'quad', 'texture': 'graphic/book.png', 'scale': (1, 1, 1)},  # 과제
{'name': 'labtop', 'model': 'quad', 'texture': 'graphic/labtop.png', 'scale': (1, 1, 1)},  # 노트북
{'name': 'team1', 'model': 'quad', 'texture': 'graphic/team1.png', 'scale': (1, 2, 1)},   # 팀원
{'name': 'team2', 'model': 'quad', 'texture': 'graphic/team2.png', 'scale': (1, 2, 1)}   # 팀원
]

# 장애물 리스트 생성
blocks = []

def spawn_block():

    if score <= 100:
        block_type = block_types[0]

    elif score > 100 and score <= 250:
        block_type = (block_types[random.randrange(0,2)])

    elif score > 250:
        block_type = (block_types[random.randrange(0,4)])

    block = Entity(
    model=block_type['model'],
    texture=block_type['texture'],
    scale=block_type['scale'],
    name=block_type['name'],
    position=(random.choice(pos), 0, 20),
    collider='quad'
)
    blocks.append(block)
    invoke(spawn_block, delay=2)

# 게임 난이도
def level (block):
    if score <=100 :
        block.z -= 0.3

    elif score > 100 and score <= 250:
        block.z -= 0.4

    elif score > 250 and score <= 450:
        block.z -= 0.5
    
    elif score > 450 and score <= 700:
        block.z -= 0.6

    elif score > 700 and score <= 999:
        block.z -= 0.7

    elif score > 999:
        block.z -= 1

# 아이템 종류
item_types = [
{'name': 'heart1', 'model': 'quad', 'texture': 'graphic/heart1.png', 'scale': (1, 1, 1)},  # 체력
{'name': 'heart2', 'model': 'quad', 'texture': 'graphic/heart2.png', 'scale': (1, 1, 1)},  
{'name': 'paper', 'model': 'quad', 'texture': 'graphic/rest.png', 'scale': (1, 1, 1)}  # 휴학신청서
]

# 아이템 리스트 생성
items = []
def spawn_item():
    if score <= 250:
        item_type = item_types[random.randrange(0,2)]
        delay = 5

    elif score >250:
        item_type = (item_types[random.randrange(0,3)])
        if item_types[random.randrange(0,2)]:
            delay = 5
        elif item_types[2]:
            delay = 10

    item = Entity(
        model=item_type['model'],
        texture=item_type['texture'],
        scale=item_type['scale'],
        name=item_type['name'],
        position=(random.choice(pos), 0, 20),
        collider='quad'
    )
    items.append(item)
    invoke(spawn_item, delay = delay)

# 캐릭터 좌우 이동, 스페이스 점프
def input(key):
    if key == 'space' and player.y == 0:
        player.animate_y(1.5, duration=0.25, curve=curve.out_quad)
        invoke(player.animate_y, 0, duration=0.25, delay=0.25, curve=curve.in_quad)
    elif key == 'd' and player.x < max(pos):
        player.x += 2
    elif key == 'a' and player.x > min(pos):
        player.x -= 2

# 장애물, 아이템 이동
def update():
    for block in blocks[:]:
        level(block)
        if block.z < -4:  # 화면 밖으로 나가면 삭제
            blocks.remove(block)
            destroy(block)

        elif player.intersects(block).hit: # 장애물과 충돌감지
            Audio(sound_file_name='bgm/충돌.mp3', volume=0.5, loop=False) #충돌 소리
            reduce_health()
            blocks.remove(block)
            destroy(block)

    for item in items[:]:
        item.z -= 0.3
        if item.z < -4 :
            items.remove(item)
            destroy(item)

        elif player.intersects(item).hit:
            Audio(sound_file_name='bgm/아이템.mp3', volume=1, loop=False) #아이템 먹는 소리
            match item.name:
                case 'heart1':
                    plus_health()
                case 'heart2':
                    plus_health()
                case 'paper':
                    rest()
            items.remove(item)
            destroy(item)

# 시간 기반 점수 증가
    global score, elapsed_time
    elapsed_time += time.dt

# 0.1초마다 점수 증가
    if elapsed_time >= 0.1:
        score += 1
        elapsed_time = 0  # 타이머 리셋
        score_text.text = f"score: {score}"


# 게임 시작
def start_game():
    # 메인 화면 숨기고 게임 화면 활성화
    main_screen.disable()
    main_bgm.volume = 0
    game_bgm.volume = 0.5
    background.enabled = True
    player.enabled = True
    explain_button.disable()
    start_button.disable()
    start1_button.disable()
    back_button.disable()
    
    # 점수 표시
    global score
    score = 0
    score_text.enabled = True

    # 카메라 생성
    camera.position = (0, 2, -10)
    camera.rotation = (4, 0, 0)

    # 체력 생성
    for i in range(3):
        hearts[i].enabled = True

    # 장애물, 아이템 생성
    spawn_block()
    spawn_item()

start_button.on_click = start_game
start1_button.on_click = start_game

app.run()



"""
점수구간
F 0 ~ 100 (100 차이) - 장애물 : 과제, 아이템 : 체력 (5초)
D 101 ~ 250 (150 차이) - 장애물 : 과제+노트북, 아이템 : 체력 (5초)
C+ 251 ~ 450 (200 차이) - 장애물 : 과제+노트북+팀, 아이템 : 무적(10초) + 체력
B+ 451 ~ 700 (250 차이) - 장애물 : 속도증가, 아이템 : 무적(10초) + 체력
A 701 ~ 999  (300 차이) - 장애물 : 속도증가, 아이템 : 무적(10초) + 체력
A+ 1000점 이상 : 장애물 : 속도증가, 아이템 : 10초

S 히든 2000
"""
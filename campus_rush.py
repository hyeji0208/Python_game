from ursina import *
import random

# 윈도우 생성
app = Ursina()

# 맵 한정하기
pos = [-2, 0, 2]

# 점수 표시
score = 0
elapsed_time = 0
score_text = Text(f"Score: {score}", position=(-0.7, 0.45), scale=2, color=color.white)

# 플레이어 생성
player = Entity(model='cube', color=color.white, scale_y=1.5, position=(0, 0, 2), collider='box')

# 체력 생성
global health
max_health = 3
health = max_health

hearts = []
for i in range(max_health):
    heart = Entity(
        model='quad',
        texture='graphic/health.png',
        position=(2 + i * 0.35, 3.2),
        scale=(0.47, 0.47)
    )
    hearts.append(heart)

# 체력감소함수
invincible = False # 무적 상태

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
    
    elif score >250 and score <= 999:
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

# 카메라 생성
camera.position = (0, 2, -10)
camera.rotation = (3, 0, 0)

# 캐릭터 좌우 이동, 스페이스 점프
def input(key):
    if key == 'space' and player.y == 0:
        player.animate_y(2, duration=0.25, curve=curve.out_quad)
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
            reduce_health()
            blocks.remove(block)
            destroy(block)

    for item in items[:]:
        item.z -= 0.3
        if item.z < -4 :
            items.remove(item)
            destroy(item)

        elif player.intersects(item).hit:
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
spawn_block()
spawn_item()
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
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
        texture='heart.png',
        position=(2 + i * 0.35, 3.2),
        scale=(0.35, 0.35)
    )
    hearts.append(heart)

# 체력감소함수
invincible = False # 무적 상태

def reduce_health():
    global invincible
    if invincible != True: # 무적 상태가 아닐 경우 체력 감소
        health -= 1
        if health >= 0:
            hearts[health].enabled = False

#체력증가함수
def plus_health():
    health += 1
    if health < 3:
        hearts[health].enabled = True


# 장애물 종류 정의
block_types = [
    {'name': 'task','model': 'cube', 'color': color.yellow, 'scale': (0.5, 0.5, 0.5)},  # 과제
    {'name': 'labtop', 'model': 'cube', 'color': color.gray, 'scale': (0.5, 0.5, 0.5)},  # 노트북
    {'name': 'team', 'model': 'cube', 'color': color.green, 'scale': (0.5, 1, 0.5)}   # 팀원
]

# 장애물 리스트 생성
blocks = []

def spawn_block():
    block_type = random.choice(block_types)
    block = Entity(
        model=block_type['model'],
        color=block_type['color'],
        scale=block_type['scale'],
        name=block_type['name'],
        position=(random.choice(pos), 0, 20),
        collider='cube'
    )
    blocks.append(block)
    invoke(spawn_block, delay=2)

# 아이템 종류
item_types = [
    {'name': 'heart', 'model': 'sphere', 'color': color.red, 'scale': (0.5, 0.5, 0.5)},  # 체력
    {'name': 'paper', 'model': 'sphere', 'color': color.blue, 'scale': (0.5, 0.5, 0.5)}  # 휴학신청서
]

# 아이템 리스트 생성
items = []
def spawn_item():
    item_type = random.choice(item_types)
    item = Entity(
        model=item_type['model'],
        color=item_type['color'],
        scale=item_type['scale'],
        name=item_type['name'],
        position=(random.choice(pos), 0, 20),
        collider='sphere'
    )
    items.append(item)
    invoke(spawn_item, delay=5)

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
        block.z -= 0.3
        if block.z < -4:  # 화면 밖으로 나가면 삭제
            blocks.remove(block)
            destroy(block)

        elif player.intersects(block).hit: # 장애물과 충돌감지
            reduce_health()
            blocks.remove(block)
            destroy(block)

    for item in items[:]:
        item.z -= 0.3
        if item.z < -4 : # 아이템 충돌
            items.remove(item)
            destroy(item)

        elif player.intersects(item).hit:
            items.remove(item)
            destroy(item)

            match item.name:
                case 'heart':
                    plus_health()

# 시간 기반 점수 증가
    global score, elapsed_time
    elapsed_time += time.dt

    # 1초마다 점수 증가
    if elapsed_time >= 1:
        score += 1
        elapsed_time = 0  # 타이머 리셋
        score_text.text = f"score: {score}"


# 게임 시작
spawn_block()
spawn_item()
app.run()
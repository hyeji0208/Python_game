from ursina import *
import random

# 윈도우 생성
app = Ursina()

# 맵 한정하기
pos = [-2, 0, 2]

# 플레이어 생성
player = Entity(model='cube', color=color.white, scale_y=1.5, position=(0, 0, 2))

# 장애물 종류 정의
block_types = [
    {'model': 'cube', 'color': color.yellow, 'scale': (0.5, 0.5, 0.5)},  # 종이
    {'model': 'cube', 'color': color.gray, 'scale': (0.5, 0.5, 0.5)},  # 노트북
    {'model': 'cube', 'color': color.green, 'scale': (0.5, 1, 0.5)}   # 팀원
]

# 장애물 리스트 생성
blocks = []
def spawn_block():
    block_type = random.choice(block_types)
    block = Entity(
        model=block_type['model'],
        color=block_type['color'],
        scale=block_type['scale'],
        position=(random.choice(pos), 0, 20)
    )
    blocks.append(block)
    invoke(spawn_block, delay=2)

# 아이템 종류
item_types = [
    {'model': 'sphere', 'color': color.red, 'scale': (0.5, 0.5, 0.5)},  # 체력
    {'model': 'sphere', 'color': color.blue, 'scale': (0.5, 0.5, 0.5)}  # 휴학
]

# 아이템 리스트 생성
items = []
def spawn_item():
    item_type = random.choice(item_types)
    item = Entity(
        model=item_type['model'],
        color=item_type['color'],
        scale=item_type['scale'],
        position=(random.choice(pos), 0, 20)
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

    for item in items[:]:
        item.z -= 0.3
        if item.z < -4:
            items.remove(item)
            destroy(item)

# 게임 시작
spawn_block()
spawn_item()
app.run()

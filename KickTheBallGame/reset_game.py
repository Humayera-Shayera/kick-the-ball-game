import random
from game_state import (
    player_pos, player_rot, player_fall_ang, ball_pos, ball_vel, has_ball,
    life, score, game_over, enemies, ENEMY_COUNT, pickup_cooldown
)

def reset_game():
    player_pos[:] = [0.0, -300.0, 0.0]
    player_rot = 0.0
    player_fall_ang = 0.0

    ball_pos[:] = [0.0, 0.0, 0.0]
    ball_vel[:] = [0.0, 0.0, 0.0]
    has_ball = False
    pickup_cooldown = 0

    life = 5
    score = 0
    game_over = False

    enemies.clear()
    for _ in range(ENEMY_COUNT):
        x = random.uniform(-600 + 50, 600 - 50)
        y = random.uniform(50, 600 - 50)
        enemies.append({"pos": [x, y, 0.0]})

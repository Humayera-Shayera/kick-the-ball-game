from OpenGL.GLUT import *
import math
import time
from game_state import state

# Movement step
MOVE_STEP = 10
ROTATE_STEP = 5


def handle_keys(key, x, y):
    if state['show_menu']:
        if key == b'1':
            state['difficulty'] = 'Easy'
        elif key == b'2':
            state['difficulty'] = 'Medium'
        elif key == b'3':
            state['difficulty'] = 'Hard'
        elif key == b's':
            state['show_menu'] = False
            state['game_started'] = True
            state['timer_start'] = time.time()
        elif key == b'q':
            exit()
    elif state['game_over']:
        if key == b'r':
            from config import reset_game
            reset_game()
    else:
        if key == b'w':
            state['player_pos'][1] += MOVE_STEP
        elif key == b's':
            state['player_pos'][1] -= MOVE_STEP
        elif key == b'a':
            state['player_angle'] += ROTATE_STEP
        elif key == b'd':
            state['player_angle'] -= ROTATE_STEP


def handle_mouse(button, state_click, x, y):
    if button == GLUT_LEFT_BUTTON and state_click == GLUT_DOWN:
        kick_ball()


def kick_ball():
    rad = math.radians(state['player_angle'])
    state['ball_velocity'] = [
        math.cos(rad) * 4 * state['ball_speed'],
        math.sin(rad) * 4 * state['ball_speed']
    ]
    state['ball_kicked'] = True
    state['goal_timer_start'] = time.time()


def update_player_and_ball():
    if not state['game_started'] or state['show_menu'] or state['game_over']:
        return

    # Update ball position
    state['ball_pos'][0] += state['ball_velocity'][0]
    state['ball_pos'][1] += state['ball_velocity'][1]
    state['ball_velocity'][0] *= 0.97
    state['ball_velocity'][1] *= 0.97

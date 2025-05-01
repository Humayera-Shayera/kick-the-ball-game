from OpenGL.GL import *
from OpenGL.GLUT import *
from config import game_state, reset_game

def handle_restart_key(key):
    if key == b'r' and game_state['game_over']:
        game_state['score'] = 0
        game_state['missed'] = 0
        game_state['game_over'] = False
        game_state['last_goal_time'] = 0
        game_state['ball_kicked'] = False
        reset_game()

def check_game_over():
    if game_state['missed'] >= 5:
        game_state['game_over'] = True

def draw_game_over():
    if game_state['game_over']:
        glColor3f(1, 0, 0)
        glRasterPos2f(400, 400)
        for ch in b"GAME OVER! Press 'R' to Restart":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ch)

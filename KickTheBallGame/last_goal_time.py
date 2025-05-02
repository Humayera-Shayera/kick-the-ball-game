from OpenGL.GL import *
from OpenGL.GLUT import *
from config import game_state

def update_last_goal_time():
    from time import time
    game_state['last_goal_time'] = round(time() - game_state['goal_timer_start'], 1)

def draw_last_goal_time():
    if game_state['last_goal_time']:
        glColor3f(1, 1, 0)
        glRasterPos2f(10, 710)
        msg = f"Last Goal Time: {game_state['last_goal_time']}s"
        for ch in msg.encode():
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ch)

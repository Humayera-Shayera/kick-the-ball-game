from OpenGL.GL import *
from OpenGL.GLUT import *
from config import game_state

def draw_goal_feedback():
    if game_state['ball_kicked']:
        glColor3f(0, 1, 0)
        feedback = "GOAL!" if game_state['goal_scored'] else "MISSED!"
        glRasterPos2f(450, 200)
        for ch in feedback.encode():
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ch)

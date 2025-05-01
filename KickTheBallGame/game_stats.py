from OpenGL.GL import *
from OpenGL.GLUT import *
import time
from game_state import get_score, get_missed, get_last_goal_time, is_game_over


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glColor3f(*color)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_game_stats():
    score = get_score()
    missed = get_missed()
    last_time = get_last_goal_time()
    game_over = is_game_over()

    draw_text(10, 770, f"Score: {score}")
    draw_text(10, 740, f"Kicks Missed: {missed}")
    if last_time:
        draw_text(10, 710, f"Last Goal Time: {last_time}s")
    if game_over:
        draw_text(400, 400, "GAME OVER! Press 'R' to Restart", color=(1, 0, 0))

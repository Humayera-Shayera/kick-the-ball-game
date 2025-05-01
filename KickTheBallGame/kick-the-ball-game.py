from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

from config import init_game, restart_game
from draw_components import draw_all_components
from player_and_kick import handle_keys, handle_mouse, update_player_and_ball
from stats import draw_stats, draw_key_reminders, draw_goal_feedback
from goal_and_feedback import check_goal_or_miss, check_collision

# Window settings
width, height = 1000, 800

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_all_components()
    draw_stats()
    draw_key_reminders()
    draw_goal_feedback()

    glutSwapBuffers()

def idle():
    update_player_and_ball()
    check_goal_or_miss()
    check_collision()
    glutPostRedisplay()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(120, w / h, 1.0, 2000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def keyboard(key, x, y):
    if key == b'r':
        restart_game()
    else:
        handle_keys(key, x, y)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Kick The Ball Game")

    init_game()

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(handle_mouse)

    glutMainLoop()

if __name__ == "__main__":
    main()

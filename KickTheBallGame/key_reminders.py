from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_key_reminders():
    glColor3f(1, 1, 1)
    reminders = [
        "WASD - Move", 
        "Left Click - Kick", 
        "R - Restart", 
        "1/2/3 - Difficulty"
    ]
    for i, text in enumerate(reminders):
        glRasterPos2f(10, 660 - i * 20)
        for ch in text.encode():
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ch)

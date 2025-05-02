trail = []

def update_trail():
    trail.append(game_state["player_pos"][:2])
    if len(trail) > 10:
        trail.pop(0)
def draw_trail():
    glColor3f(0, 1, 1)
    glBegin(GL_LINE_STRIP)
    for pos in trail:
        glVertex3f(pos[0], pos[1], 1)
    glEnd()

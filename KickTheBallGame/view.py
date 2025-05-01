def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(fovY,1000/800,0.1,2000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    if camera_mode=="first":
        ex = player_pos[0] + 50*math.cos(math.radians(player_rot))
        ey = player_pos[1] + 50*math.sin(math.radians(player_rot))
        lx = player_pos[0] +150*math.cos(math.radians(player_rot))
        ly = player_pos[1] +150*math.sin(math.radians(player_rot))
        gluLookAt(ex,ey,100, lx,ly,0, 0,0,1)
    else:
        gluLookAt(*camera_pos, 0,0,0, 0,0,1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glViewport(0,0,1000,800)
    setupCamera()
    draw_grid()
    draw_walls()
    draw_player()
    draw_goal_posts()
    draw_net()
    for e in enemies: draw_enemy(e["pos"], e["scale"])
    for b in bullets: draw_bullet(b["pos"])
    draw_text(10,770, f"Life: {life}  Score: {score}  Missed: {bullets_missed}")
    if game_over:
        draw_text(400,400, "GAME OVER - Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)
    glutSwapBuffers()
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, random, time


player_pos      = [0.0, -300.0, 0.0]
player_rot      = 0.0
player_fall_ang = 0.0
life       = 5
score      = 0
game_over  = False
ball_pos        = [0.0, 0.0, 0.0]
ball_vel        = [0.0, 0.0, 0.0]
has_ball        = False
BALL_RADIUS     = 15.0
KICK_SPEED      = 15.0
pickup_cooldown = 0
GRID_LENGTH = 600
GOAL_WIDTH  = 400
GOAL_LINE   = GRID_LENGTH
goal_flag   = False
goal_time   = 0.0
enemies     = []
ENEMY_COUNT = 5
ENEMY_SPEED = 0.005
camera_mode   = "third"
camera_pos    = (0.0, 500.0, 500.0)
fovY          = 120.0
CELL_SIZE     = 100
PLAYER_RADIUS = 30

def init_enemies():
    global enemies
    enemies = []
    for _ in range(ENEMY_COUNT):
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(  50,               GRID_LENGTH - 50)
        enemies.append({"pos": [x, y, 0.0]})
init_enemies()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glRasterPos2f(x,y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    for j in range(-GRID_LENGTH, GRID_LENGTH, CELL_SIZE):
        color = (0.0,0.6,0.0) if ((j//CELL_SIZE)%2==0) else (0.0,0.4,0.0)
        glColor3f(*color)
        for i in range(-GRID_LENGTH, GRID_LENGTH, CELL_SIZE):
            glBegin(GL_QUADS)
            glVertex3f(i,   j,   0)
            glVertex3f(i+CELL_SIZE, j,   0)
            glVertex3f(i+CELL_SIZE, j+CELL_SIZE, 0)
            glVertex3f(i, j+CELL_SIZE, 0)
            glEnd()
    # center lines
    glColor3f(1,1,1)
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(-GRID_LENGTH,0,0)
    glVertex3f( GRID_LENGTH,0,0)
    glEnd()
    glBegin(GL_LINE_LOOP)
    for i in range(64):
        ang = 2*math.pi*i/64
        glVertex3f(100*math.cos(ang), 100*math.sin(ang), 0.1)
    glEnd()

def draw_walls():
    glColor3f(0,1,1)
    h = CELL_SIZE
    box_w = GOAL_WIDTH
    for y in (-GRID_LENGTH, GRID_LENGTH):
        glBegin(GL_QUADS)
        glVertex3f(-GRID_LENGTH, y,   0)
        glVertex3f(-GRID_LENGTH, y,   h)
        glVertex3f(-box_w/2,    y,   h)
        glVertex3f(-box_w/2,    y,   0)
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f( box_w/2,    y,   0)
        glVertex3f( box_w/2,    y,   h)
        glVertex3f( GRID_LENGTH, y,  h)
        glVertex3f( GRID_LENGTH, y,  0)
        glEnd()
    for x in (-GRID_LENGTH, GRID_LENGTH):
        glBegin(GL_QUADS)
        glVertex3f(x, -GRID_LENGTH, 0)
        glVertex3f(x, -GRID_LENGTH, h)
        glVertex3f(x,  GRID_LENGTH, h)
        glVertex3f(x,  GRID_LENGTH, 0)
        glEnd()

def draw_goal_posts():
    glColor3f(1,1,1)
    post_thick, post_height = 10, 200
    cross_th = 10
    box_w = GOAL_WIDTH
    for y in (-GRID_LENGTH, GRID_LENGTH):
        for x_off in (-box_w/2, box_w/2):
            glPushMatrix()
            glTranslatef(x_off, y, post_height/2)
            glScalef(post_thick, post_thick, post_height)
            glutSolidCube(1)
            glPopMatrix()
        glPushMatrix()
        glTranslatef(0, y, post_height)
        glScalef(box_w, cross_th, post_thick)
        glutSolidCube(1)
        glPopMatrix()

def draw_net():
    glColor4f(1,1,1,0.7)
    box_w, post_h = GOAL_WIDTH, 200
    glLineWidth(1)
    for i in range(-int(box_w/2)+10, int(box_w/2), 20):
        for sign in (1, -1):
            glBegin(GL_LINE_STRIP)
            glVertex3f(i, sign*GRID_LENGTH, post_h)
            glVertex3f(i, sign*GRID_LENGTH, 0)
            glEnd()
    for j in range(10, post_h, 20):
        for sign in (1, -1):
            glBegin(GL_LINES)
            glVertex3f(-box_w/2, sign*GRID_LENGTH, j)
            glVertex3f( box_w/2, sign*GRID_LENGTH, j)
            glEnd()

def draw_player_model():
    quad = gluNewQuadric()
    glColor3f(0,0,0)
    for off in (-12, 12):
        glPushMatrix()
        glTranslatef(off, 0, 0)
        gluCylinder(quad, 5, 2, 50, 12, 1)
        glPopMatrix()
    body = 40
    glColor3f(0.5,0.5,0.5)
    glPushMatrix()
    glTranslatef(0, 0, 50+body/2)
    glutSolidCube(body)
    glPopMatrix()
    glColor3f(0,0,0)
    arm_z = 50 + body*0.75
    for off in (-body/2, body/2):
        glPushMatrix()
        glTranslatef(off, 0, arm_z)
        glRotatef(90,1,0,0)
        gluCylinder(quad, 4,4,30,12,1)
        glPopMatrix()
    glColor3f(0,1,1)
    glPushMatrix()
    glTranslatef(0, 0, 50+body+20)
    glutSolidSphere(20,20,20)
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_rot+90, 0,0,1)
    if game_over and player_fall_ang>0:
        glRotatef(player_fall_ang, 1,0,0)
    draw_player_model()
    glPopMatrix()

def draw_enemy_model():
    quad = gluNewQuadric()
    glColor3f(0,0,0)
    for off in (-12,12):
        glPushMatrix()
        glTranslatef(off, 0, 0)
        gluCylinder(quad, 5,2,50,12,1)
        glPopMatrix()
    body = 40
    glPushMatrix()
    glTranslatef(0, 0, 50+body/2)
    glutSolidCube(body)
    glPopMatrix()
    arm_z = 50 + body*0.75
    for off in (-body/2, body/2):
        glPushMatrix()
        glTranslatef(off, 0, arm_z)
        glRotatef(90,1,0,0)
        gluCylinder(quad,4,4,30,12,1)
        glPopMatrix()
    glColor3f(0,1,1)
    glPushMatrix()
    glTranslatef(0, 0, 50+body+20)
    glutSolidSphere(20,20,20)
    glPopMatrix()

def draw_enemy(e):
    glPushMatrix()
    glTranslatef(*e['pos'])
    glRotatef(180,0,0,1)
    draw_enemy_model()
    glPopMatrix()

def draw_ball():
    glPushMatrix()
    glTranslatef(*ball_pos)
    glColor3f(1,1,0)
    glutSolidSphere(BALL_RADIUS,20,20)
    glPopMatrix()

def update_game():
    global enemies, life, game_over, player_fall_ang
    global pickup_cooldown, has_ball, ball_pos, ball_vel
    global goal_flag, goal_time, score

    if game_over:
        if player_fall_ang < 90:
            player_fall_ang += 2
        return

    if goal_flag:
        if time.time() - goal_time >= 5.0:
            ball_pos[:] = [0.0,0.0,0.0]
            ball_vel[:] = [0.0,0.0,0.0]
            has_ball = False
            goal_flag = False
            player_pos[1] = -300.0
            init_enemies()
        else:
            return

    if pickup_cooldown > 0:
        pickup_cooldown -= 1

    for e in enemies:
        dx, dy = ball_pos[0]-e['pos'][0], ball_pos[1]-e['pos'][1]
        d = math.hypot(dx,dy) or 1
        e['pos'][0] += dx/d * ENEMY_SPEED
        e['pos'][1] += dy/d * ENEMY_SPEED
        if math.hypot(e['pos'][0]-ball_pos[0], e['pos'][1]-ball_pos[1]) < BALL_RADIUS+20:
            game_over = True
            return

        if math.hypot(player_pos[0]-e['pos'][0], player_pos[1]-e['pos'][1]) < 35:
            life -= 1
            if life <= 0:
                game_over = True
            e['pos'] = [
                random.uniform(-GRID_LENGTH, GRID_LENGTH),
                random.uniform( 50, GRID_LENGTH), 0.0
            ]

    if has_ball:
        ball_pos[0] = player_pos[0] + (PLAYER_RADIUS + BALL_RADIUS/2)*math.cos(math.radians(player_rot))
        ball_pos[1] = player_pos[1] + (PLAYER_RADIUS + BALL_RADIUS/2)*math.sin(math.radians(player_rot))
    elif pickup_cooldown == 0:
        if math.hypot(player_pos[0]-ball_pos[0], player_pos[1]-ball_pos[1]) < PLAYER_RADIUS+BALL_RADIUS+10:
            has_ball = True
            ball_vel[:] = [0.0,0.0,0.0]

    if not has_ball:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        half_goal = GOAL_WIDTH/2 - BALL_RADIUS

        if ball_pos[1] > GOAL_LINE - BALL_RADIUS and abs(ball_pos[0]) < half_goal:
            score += 1
            goal_flag = True
            goal_time = time.time()
            ball_vel[:] = [0.0,0.0,0.0]
            return
        if ball_pos[1] < -GOAL_LINE + BALL_RADIUS and abs(ball_pos[0]) < half_goal:
            score -= 1
            goal_flag = True
            goal_time = time.time()
            ball_vel[:] = [0.0,0.0,0.0]
            return

        max_c = GRID_LENGTH - BALL_RADIUS
        if ball_pos[0] >  max_c:
            ball_pos[0], ball_vel[0] = max_c, -ball_vel[0]
        elif ball_pos[0] < -max_c:
            ball_pos[0], ball_vel[0] = -max_c, -ball_vel[0]
        if ball_pos[1] >  max_c and abs(ball_pos[0]) > half_goal:
            ball_pos[1], ball_vel[1] = max_c, -ball_vel[1]
        if ball_pos[1] < -max_c and abs(ball_pos[0]) > half_goal:
            ball_pos[1], ball_vel[1] = -max_c, -ball_vel[1]

        ball_vel[0] *= 0.98
        ball_vel[1] *= 0.98
        if abs(ball_vel[0]) < 0.01: ball_vel[0] = 0.0
        if abs(ball_vel[1]) < 0.01: ball_vel[1] = 0.0

def keyboardListener(key, x, y):
    global player_pos, player_rot, life, game_over, player_fall_ang, score
    global ball_pos, has_ball
    if game_over and key == b'r':
        player_pos[:] = [0.0,-300.0,0.0]
        player_rot = 0.0
        life, score = 5, 0
        game_over, player_fall_ang = False, 0.0
        ball_pos[:] = [0.0,0.0,0.0]
        ball_vel[:] = [0.0,0.0,0.0]
        has_ball = False
        init_enemies()
        return
    if game_over:
        return
    k = key.decode().lower()
    if k == 'w':
        player_pos[0] += 10*math.cos(math.radians(player_rot))
        player_pos[1] += 10*math.sin(math.radians(player_rot))
    elif k == 's':
        player_pos[0] -= 10*math.cos(math.radians(player_rot))
        player_pos[1] -= 10*math.sin(math.radians(player_rot))
    elif k == 'a':
        player_rot += 5
    elif k == 'd':
        player_rot -= 5
    lim = GRID_LENGTH - PLAYER_RADIUS
    player_pos[0] = max(-lim, min(lim, player_pos[0]))
    player_pos[1] = max(-lim, min(lim, player_pos[1]))

def mouseListener(button, state, x, y):
    global has_ball, ball_vel, camera_mode, pickup_cooldown
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        if has_ball:
            ball_vel[:] = [
                KICK_SPEED*math.cos(math.radians(player_rot)),
                KICK_SPEED*math.sin(math.radians(player_rot)), 0.0
            ]
            has_ball = False
            pickup_cooldown = 20
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 'first' if camera_mode=='third' else 'third'

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_UP:    cy += 10
    elif key == GLUT_KEY_DOWN: cy -= 10
    elif key == GLUT_KEY_LEFT: cx -= 10
    elif key == GLUT_KEY_RIGHT:cx += 10
    camera_pos = (cx, cy, cz)

def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(fovY, 1000/800, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    if camera_mode == 'first':
        ex = player_pos[0] + 50*math.cos(math.radians(player_rot))
        ey = player_pos[1] + 50*math.sin(math.radians(player_rot))
        lx = player_pos[0] +150*math.cos(math.radians(player_rot))
        ly = player_pos[1] +150*math.sin(math.radians(player_rot))
        gluLookAt(ex, ey, 100, lx, ly, 0, 0,0,1)
    else:
        gluLookAt(*camera_pos, 0,0,0, 0,0,1)

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid()
    draw_walls()
    draw_list = []
    def queue_draw(fn, pos):
        dx = pos[0] - camera_pos[0]
        dy = pos[1] - camera_pos[1]
        dz = pos[2] - camera_pos[2]
        dist2 = dx*dx + dy*dy + dz*dz
        draw_list.append((dist2, fn))

    queue_draw(draw_player, player_pos)
    queue_draw(draw_goal_posts, [0, GRID_LENGTH, 100])
    queue_draw(draw_net,        [0, GRID_LENGTH, 100])
    for e in enemies:
        queue_draw(lambda e=e: draw_enemy(e), e['pos'])
    queue_draw(draw_ball, ball_pos)
    for _, fn in sorted(draw_list, key=lambda x: -x[0]):
        fn()
    draw_text(10,770, f"Life: {life}  Score: {score}")
    draw_text(10,750, f"Cooldown: {pickup_cooldown}  has_ball={has_ball}")
    if game_over:
        draw_text(400,400, "GAME OVER - Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()

def idle():
    update_game()
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,800)
    glutCreateWindow(b"Bullet Frenzy Soccer")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()

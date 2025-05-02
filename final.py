from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, random, time

game_difficulty = 'Medium'

difficulty_settings = {
    'Easy':   {'opponent_speed': 0.01, 'super_duration': 10},
    'Medium': {'opponent_speed': 0.05, 'super_duration': 5},
    'Hard':   {'opponent_speed': 0.1, 'super_duration': 3},
}

def set_difficulty(key):
    global game_difficulty
    if key == b'1':
        game_difficulty = 'Easy'
    elif key == b'2':
        game_difficulty = 'Medium'
    elif key == b'3':
        game_difficulty = 'Hard'

def get_opponent_speed():
    return difficulty_settings[game_difficulty]['opponent_speed']

player_pos      = [0.0, -300.0, 0.0]
player_rot      = 0.0
player_fall_ang = 0.0
combo_count = 0
last_goal_time = 0
combo_active = False
goal_missed = False

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

camera_mode   = "third"
camera_pos    = (0.0, 500.0, 500.0)
fovY          = 120.0
CELL_SIZE     = 100
PLAYER_RADIUS = 30
trail = []

game_state = {
    'ball_kicked': False,
    'goal_scored': False,
    'stamina': 100.0,
    'max_stamina': 100.0
}

cheat_mode = False
cheat_message_time = 0

superman_strength = False
superman_start_time = 0

turbo_mode = False
normal_speed = 10
turbo_speed = normal_speed
turbo_increment = 0.1
max_turbo_speed = 20.0

invisible = False
invisible_start_time = 0
invisibility_duration = 10

charging_towards_goal = False

def update_stamina(is_moving):
    if is_moving:
        game_state["stamina"] = max(0, game_state["stamina"] - 0.5)
    else:
        game_state["stamina"] = min(game_state["max_stamina"], game_state["stamina"] + 0.3)

def draw_goal_feedback():
    if game_state['ball_kicked']:
        glColor3f(0, 1, 0)
        feedback = "GOAL!" if game_state['goal_scored'] else "MISSED!"
        glRasterPos2f(-150, -300)
        for ch in feedback.encode():
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ch)

def update_trail():
    trail.append(player_pos[:2])
    if len(trail) > 55:
        trail.pop(0)

def draw_trail():
    glColor3f(94, 64, 51)
    glBegin(GL_LINE_STRIP)
    for pos in trail:
        glVertex3f(pos[0], pos[1], 1)
    glEnd()

def init_enemies():
    global enemies
    enemies = []
    for _ in range(ENEMY_COUNT):
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(  50,               GRID_LENGTH - 50)
        enemies.append({"pos": [x, y, 0.0], "falling": False})

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
        gluCylinder(quad,4,4,30,12,1)
        glPopMatrix()
    glColor3f(0,1,1)
    glPushMatrix()
    glTranslatef(0, 0, 50+body+20)
    glutSolidSphere(20,20,20)
    glPopMatrix()

def draw_player():
    global invisible
    if invisible:
        if time.time() - invisible_start_time > invisibility_duration:
            invisible = False
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_rot+90, 0,0,1)
    if game_over and player_fall_ang>0:
        glRotatef(player_fall_ang, 1,0,0)
    if invisible:
        glColor4f(0, 0, 0, 0)
    else:
        draw_player_model()
    glPopMatrix()

def draw_enemy_model():
    quad = gluNewQuadric()
    glColor3f(0,0,0)
    for off in (-12,12):
        glPushMatrix()
        glTranslatef(off, 0, 0)
        gluCylinder(quad,5,2,50,12,1)
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
    if not e["falling"]:
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

def update_invisibility():
    global invisible, invisible_start_time, invisibility_duration
    if invisible:
        elapsed_time = time.time() - invisible_start_time
        if elapsed_time > invisibility_duration:
            invisible = False

def draw_invisibility_countdown():
    if invisible:
        remaining_time = int(invisibility_duration - (time.time() - invisible_start_time))
        draw_text(400, 650, f"Invisibility: {remaining_time}s", GLUT_BITMAP_TIMES_ROMAN_24)

def charge_towards_goal():
    global player_pos, player_rot, ball_pos, enemies
    goal_direction = math.radians(player_rot)
    player_pos[0] += 10 * math.cos(goal_direction)
    player_pos[1] += 10 * math.sin(goal_direction)

    for enemy in enemies:
        dx, dy = enemy["pos"][0] - player_pos[0], enemy["pos"][1] - player_pos[1]
        if abs(dx) < 30 and abs(dy) < 30: 
            enemy["falling"] = True
            enemy["pos"][2] = -50  
    if abs(player_pos[1] - GOAL_LINE) < 20 and abs(ball_pos[0] - player_pos[0]) < PLAYER_RADIUS + BALL_RADIUS:
        ball_vel[0] = 15 * math.cos(math.radians(player_rot))
        ball_vel[1] = 15 * math.sin(math.radians(player_rot))
        has_ball = False
        pickup_cooldown = 20

def update_game():
    global enemies, life, game_over, player_fall_ang
    global pickup_cooldown, has_ball, ball_pos, ball_vel
    global goal_flag, goal_time, score, combo_count, combo_active, goal_missed, charging_towards_goal

    if game_over:
        if player_fall_ang < 90:
            player_fall_ang += 2
        return

    update_invisibility()

    if goal_flag:
        if time.time() - goal_time >= 5.0:
            ball_pos[:] = [0.0, 0.0, 0.0]
            ball_vel[:] = [0.0, 0.0, 0.0]
            has_ball = False
            goal_flag = False
            player_pos[1] = -300.0
            init_enemies()

            if combo_active and not goal_missed:
                combo_count += 1
            else:
                combo_active = True
                combo_count = 1

            goal_missed = False
            game_state['ball_kicked'] = False
            game_state['goal_scored'] = False

            return
        else:
            return

    if not has_ball and combo_active:
        combo_active = False
        combo_count = 0
        goal_missed = True

    update_trail()

    if pickup_cooldown > 0:
        pickup_cooldown -= 1

    if charging_towards_goal:
        charge_towards_goal()
        if abs(player_pos[1] - GOAL_LINE) < 20:  # Check if player has reached the goal line
            charging_towards_goal = False  # Stop charging after reaching goal
            ball_vel[0] = 15 * math.cos(math.radians(player_rot))
            ball_vel[1] = 15 * math.sin(math.radians(player_rot))
            has_ball = False
            pickup_cooldown = 20
        return

    speed = get_opponent_speed()
    for e in enemies:
        if invisible:
            continue

        dx, dy = ball_pos[0]-e['pos'][0], ball_pos[1]-e['pos'][1]
        d = math.hypot(dx,dy) or 1
        e['pos'][0] += dx/d * speed
        e['pos'][1] += dy/d * speed

        if math.hypot(e['pos'][0]-ball_pos[0], e['pos'][1]-ball_pos[1]) < BALL_RADIUS+20:
            if cheat_mode:
                e['falling'] = True
                e['pos'][2] = -50
            elif superman_strength:
                continue
            elif not invisible:
                game_over = True

        if math.hypot(player_pos[0]-e['pos'][0], player_pos[1]-e['pos'][1]) < 35:
            if not superman_strength:
                life -= 1
            if life <= 0:
                game_over = True
            e['pos'] = [
                random.uniform(-GRID_LENGTH,GRID_LENGTH),
                random.uniform( 50, GRID_LENGTH),
                0.0
            ]

    if has_ball:
        ball_pos[0] = player_pos[0] + (PLAYER_RADIUS+BALL_RADIUS/2)*math.cos(math.radians(player_rot))
        ball_pos[1] = player_pos[1] + (PLAYER_RADIUS+BALL_RADIUS/2)*math.sin(math.radians(player_rot))
    elif pickup_cooldown == 0:
        if math.hypot(player_pos[0]-ball_pos[0], player_pos[1]-ball_pos[1]) < PLAYER_RADIUS+BALL_RADIUS+10:
            has_ball = True
            ball_vel[:] = [0.0,0.0,0.0]

    if not has_ball:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]

        half_goal = GOAL_WIDTH/2 - BALL_RADIUS
        if ball_pos[1] > GOAL_LINE-BALL_RADIUS and abs(ball_pos[0])<half_goal:
            score += 1
            goal_flag = True
            goal_time = time.time()
            ball_vel[:] = [0.0,0.0,0.0]
            game_state['ball_kicked'] = True
            game_state['goal_scored'] = True
            return
        if ball_pos[1] < -GOAL_LINE+BALL_RADIUS and abs(ball_pos[0])<half_goal:
            score -= 1
            goal_flag = True
            goal_time = time.time()
            ball_vel[:] = [0.0,0.0,0.0]
            game_state['ball_kicked'] = True
            game_state['goal_scored'] = False
            return

        max_c = GRID_LENGTH - BALL_RADIUS
        if ball_pos[0]> max_c:
            ball_pos[0], ball_vel[0] = max_c, -ball_vel[0]
        elif ball_pos[0]<-max_c:
            ball_pos[0], ball_vel[0] = -max_c,-ball_vel[0]
        if ball_pos[1]> max_c and abs(ball_pos[0])>half_goal:
            ball_pos[1], ball_vel[1] = max_c, -ball_vel[1]
        if ball_pos[1]<-max_c and abs(ball_pos[0])>half_goal:
            ball_pos[1], ball_vel[1] = -max_c,-ball_vel[1]

        ball_vel[0] *= 0.98; ball_vel[1] *= 0.98
        if abs(ball_vel[0])<0.01: ball_vel[0] = 0.0
        if abs(ball_vel[1])<0.01: ball_vel[1] = 0.0

def keyboardListener(key, x, y):
    global player_pos, player_rot, charging_towards_goal, life, game_over, player_fall_ang, score
    global ball_pos, has_ball, combo_count, combo_active, cheat_mode, cheat_message_time, superman_strength, superman_start_time, turbo_mode, turbo_speed, turbo_increment, invisible, invisible_start_time

    if key == b'1':
        set_difficulty(key)
        return

    if game_over and key == b'r':
        print("Restarting the game...")
        player_pos[:] = [0.0,-300.0,0.0]
        player_rot = 0.0
        life, score = 5, 0
        game_over, player_fall_ang = False, 0.0
        ball_pos[:] = [0.0,0.0,0.0]
        ball_vel[:] = [0.0,0.0,0.0]
        has_ball = False
        combo_count, combo_active = 0, False
        init_enemies()
        game_state['ball_kicked'] = False
        game_state['goal_scored'] = False
        print("Game has been reset.")
        return

    if game_over:
        return

    k = key.decode().lower()
    if k == 'w':
        player_pos[0] += turbo_speed * math.cos(math.radians(player_rot))
        player_pos[1] += turbo_speed * math.sin(math.radians(player_rot))
        update_stamina(True)  # Player is moving
    elif k == 's':
        player_pos[0] -= turbo_speed * math.cos(math.radians(player_rot))
        player_pos[1] -= turbo_speed * math.sin(math.radians(player_rot))
        update_stamina(True)  # Player is moving
    elif k == 'a':
        player_rot += 5
        update_stamina(False)  # Player is not moving
    elif k == 'd':
        player_rot -= 5
        update_stamina(False)  # Player is not moving
    elif k == 'c':
        cheat_mode = not cheat_mode
        cheat_message_time = time.time()  
        print(f"Cheat mode {'activated' if cheat_mode else 'deactivated'}.")
    elif k == 'p': 
        superman_strength = True
        superman_start_time = time.time()
        print("Superman strength activated!")
    elif k == 't': 
        if turbo_mode:
            turbo_mode = False
            turbo_speed = normal_speed  
            print("Turbo mode deactivated.")
        else:
            turbo_mode = True
            turbo_speed = normal_speed  
            print("Turbo mode activated.")
    elif k == 'i': 
        invisible = True
        invisible_start_time = time.time()
        print("Player is now invisible for 10 seconds.")

    elif k == 'b':
        charging_towards_goal = True  # Start charging towards the goal

    lim = GRID_LENGTH - PLAYER_RADIUS
    player_pos[0] = max(-lim, min(lim, player_pos[0]))
    player_pos[1] = max(-lim, min(lim, player_pos[1]))

def mouseListener(button, state, x, y):
    global has_ball, ball_vel, camera_mode, pickup_cooldown, cheat_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        if has_ball:
            kick_speed = KICK_SPEED * 5 if cheat_mode else KICK_SPEED
            ball_vel[:] = [
                kick_speed * math.cos(math.radians(player_rot)),
                kick_speed * math.sin(math.radians(player_rot)), 0.0
            ]
            has_ball = False
            pickup_cooldown = 20
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 'first' if camera_mode == 'third' else 'third'

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_UP:    cy += 10
    elif key == GLUT_KEY_DOWN: cy -= 10
    elif key == GLUT_KEY_LEFT: cx -= 10
    elif key == GLUT_KEY_RIGHT: cx += 10
    camera_pos = (cx, cy, cz)

def setupCamera():
    glMatrixMode(GL_PROJECTION); glLoadIdentity()
    gluPerspective(fovY, 1000/800, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    if camera_mode == 'first':
        ex = player_pos[0] + 50*math.cos(math.radians(player_rot))
        ey = player_pos[1] + 50*math.sin(math.radians(player_rot))
        lx = player_pos[0] + 150*math.cos(math.radians(player_rot))
        ly = player_pos[1] + 150*math.sin(math.radians(player_rot))
        gluLookAt(ex, ey, 100, lx, ly, 0, 0,0,1)
    else:
        gluLookAt(*camera_pos, 0,0,0, 0,0,1)

def showScreen():
    global superman_strength, superman_start_time, cheat_mode, cheat_message_time

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

    queue_draw(draw_trail, player_pos)
    queue_draw(draw_player, player_pos)
    queue_draw(draw_goal_posts, [0, GRID_LENGTH, 100])
    queue_draw(draw_net, [0, GRID_LENGTH, 100])

    for e in enemies:
        queue_draw(lambda e=e: draw_enemy(e), e['pos'])

    queue_draw(draw_ball, ball_pos)
    for _, fn in sorted(draw_list, key=lambda x: -x[0]):
        fn()

    draw_text(10, 770, f"Life: {life}  Score: {score}")
    draw_text(10, 750, f"CD: {pickup_cooldown}  Ball: {has_ball}")
    draw_text(10, 730, f"Difficulty: {game_difficulty} (1-Easy 2-Med 3-Hard)")

    if goal_flag:
        draw_text(10, 710, f"Last Goal Time: {goal_time:.2f} seconds")

    draw_text(10, 690, f"Combo: {combo_count}")

    draw_goal_feedback()

    if game_over:
        draw_text(400, 400, "GAME OVER - Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)

    if superman_strength:
        remaining_time = max(0, 30 - (time.time() - superman_start_time))
        if remaining_time > 0:
            draw_text(400, 500, f"Superman Strength: {remaining_time:.2f}s", GLUT_BITMAP_TIMES_ROMAN_24)
        else:
            superman_strength = False

    if cheat_mode and time.time() - cheat_message_time <= 2:
        draw_text(400, 550, "Cheat code C activated!", GLUT_BITMAP_TIMES_ROMAN_24)

    if turbo_mode:
        draw_text(400, 600, "Turbo Mode: Active", GLUT_BITMAP_TIMES_ROMAN_24)

    if invisible:
        draw_invisibility_countdown()

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

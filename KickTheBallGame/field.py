def draw_grid():
    for j in range(-GRID_LENGTH, GRID_LENGTH, CELL_SIZE):
        color = (0.0, 0.6, 0.0) if ((j // CELL_SIZE) % 2 == 0) else (0.0, 0.4, 0.0)
        glColor3f(*color)
        for i in range(-GRID_LENGTH, GRID_LENGTH, CELL_SIZE):
            glBegin(GL_QUADS)
            glVertex3f(i, j, 0)
            glVertex3f(i + CELL_SIZE, j, 0)
            glVertex3f(i + CELL_SIZE, j + CELL_SIZE, 0)
            glVertex3f(i, j + CELL_SIZE, 0)
            glEnd()

    #markings
    glColor3f(1, 1, 1)
    glLineWidth(2.0)
    half_field = GRID_LENGTH

    # Center line
    glBegin(GL_LINES)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glEnd()

    # Center circle
    glBegin(GL_LINE_LOOP)
    radius = 100
    for i in range(64):
        angle = 2 * math.pi * i / 64
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, 0.1)
    glEnd()

    # Center spot
    glPointSize(6)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0.2)
    glEnd()

    # Penalty boxes
    box_width = 400
    box_depth = 200

    # Bottom penalty box
    glBegin(GL_LINE_LOOP)
    glVertex3f(-box_width/2, -GRID_LENGTH, 0.1)
    glVertex3f(-box_width/2, -GRID_LENGTH + box_depth, 0.1)
    glVertex3f(box_width/2, -GRID_LENGTH + box_depth, 0.1)
    glVertex3f(box_width/2, -GRID_LENGTH, 0.1)
    glEnd()

    # Top penalty box
    glBegin(GL_LINE_LOOP)
    glVertex3f(-box_width/2, GRID_LENGTH, 0.1)
    glVertex3f(-box_width/2, GRID_LENGTH - box_depth, 0.1)
    glVertex3f(box_width/2, GRID_LENGTH - box_depth, 0.1)
    glVertex3f(box_width/2, GRID_LENGTH, 0.1)
    glEnd()


def draw_walls():
    glColor3f(0,1,1)
    h = CELL_SIZE
    box_width = 400 
    for y in (-GRID_LENGTH, GRID_LENGTH):
        # Left segment
        glBegin(GL_QUADS)
        glVertex3f(-GRID_LENGTH, y, 0)
        glVertex3f(-GRID_LENGTH, y, h)
        glVertex3f(-box_width/2, y, h)
        glVertex3f(-box_width/2, y, 0)
        glEnd()
        # Right segment
        glBegin(GL_QUADS)
        glVertex3f(box_width/2, y, 0)
        glVertex3f(box_width/2, y, h)
        glVertex3f(GRID_LENGTH, y, h)
        glVertex3f(GRID_LENGTH, y, 0)
        glEnd()
    # Side walls
    for x in (-GRID_LENGTH, GRID_LENGTH):
        glBegin(GL_QUADS)
        glVertex3f(x, -GRID_LENGTH, 0); glVertex3f(x, -GRID_LENGTH, h)
        glVertex3f(x, GRID_LENGTH, h);  glVertex3f(x, GRID_LENGTH, 0)
        glEnd()

def draw_goal_posts():
    glColor3f(1, 1, 1)
    post_thick = 10
    post_height = 200
    crossbar_thick = 10
    box_w = 400

    for y in (-GRID_LENGTH, GRID_LENGTH):
        # Left post
        glPushMatrix()
        glTranslatef(-box_w/2, y, post_height/2)
        glScalef(post_thick, post_thick, post_height)
        glutSolidCube(1)
        glPopMatrix()

        # Right post
        glPushMatrix()
        glTranslatef( box_w/2, y, post_height/2)
        glScalef(post_thick, post_thick, post_height)
        glutSolidCube(1)
        glPopMatrix()

        # Crossbar
        glPushMatrix()
        glTranslatef(0, y, post_height)
        glScalef(box_w, crossbar_thick, post_thick)
        glutSolidCube(1)
        glPopMatrix()


def draw_net():
    glColor4f(1,1,1,0.7)
    box_w = 400
    post_height = 200
    glLineWidth(1.0)
    for i in range(-int(box_w/2)+10, int(box_w/2), 20):
        glBegin(GL_LINE_STRIP)
        glVertex3f(i, GRID_LENGTH, post_height)
        glVertex3f(i, GRID_LENGTH, 0)
        glEnd()
        glBegin(GL_LINE_STRIP)
        glVertex3f(i, -GRID_LENGTH, post_height)
        glVertex3f(i, -GRID_LENGTH, 0)
        glEnd()
    for j in range(10, post_height, 20):
        glBegin(GL_LINES)
        glVertex3f(-box_w/2, GRID_LENGTH, j)
        glVertex3f(box_w/2, GRID_LENGTH, j)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(-box_w/2, -GRID_LENGTH, j)
        glVertex3f(box_w/2, -GRID_LENGTH, j)
        glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_rot+90, 0,0,1)
    if game_over and player_fall_ang>0:
        glRotatef(player_fall_ang,1,0,0)

    quad = gluNewQuadric()
    # legs
    glColor3f(0,0,0)
    for x_off in (-12,12):
        glPushMatrix()
        glTranslatef(x_off,0,0)
        gluCylinder(quad,5,2,50,12,1)
        glPopMatrix()
    # body
    body_s = 40
    glColor3f(0.5,0.5,0.5)
    glPushMatrix()
    glTranslatef(0,0,50+body_s/2)
    glutSolidCube(body_s)
    glPopMatrix()
    # side-arms
    glColor3f(0,0,0)
    arm_r, arm_len = 4, 30
    arm_z = 50 + body_s*0.75
    for x_off in (-body_s/2, body_s/2):
        glPushMatrix()
        glTranslatef(x_off,0,arm_z)
        glRotatef(90,1,0,0)
        gluCylinder(quad,arm_r,arm_r,arm_len,12,1)
        glPopMatrix()
    # head
    glColor3f(0,1,1)
    glPushMatrix()
    glTranslatef(0,0,50+body_s+20)
    glutSolidSphere(20,20,20)
    glPopMatrix()
    glPopMatrix()
def init_enemies():
    global enemies
    enemies = []
    for _ in range(ENEMY_COUNT):
        x = random.randint(-GRID_LENGTH, GRID_LENGTH)
        y = random.randint(-GRID_LENGTH, GRID_LENGTH)
        enemies.append({"pos":[x, y, 0], "scale":1.0, "dir":0.01})
        
def draw_enemy(pos, scale):
    glPushMatrix()
    glTranslatef(*pos)
    glColor3f(1,0,0)
    glutSolidSphere(30*scale,20,20)
    glTranslatef(0,0,30*scale+20*scale)
    blink = (int(time.time()*2)%2)==0
    glColor3f(0,1,0) if blink else glColor3f(0,0,0)
    glutSolidSphere(20*scale,20,20)
    glPopMatrix()
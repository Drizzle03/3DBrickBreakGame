game_state = "start_screen"

#구의 x, y, z 좌표 설정
sp_x = 0
sp_y = 0
sp_z = 0

# 구의 x 속도, y속도, z의 속도 설정
sp_dx = 4
sp_dy = 6
sp_dz = 4

# 박스의 너비, 높이, 깊이
box_width = 700
box_height = 500
box_depth = 400

# 박스의 반 너비, 높이, 깊이
half_box_width = box_width / 2
half_box_height = box_height / 2
half_box_depth = box_depth / 2
z_offset = 10

brick_start_point_x = -half_box_width / 2
brick_start_point_y = -half_box_height /2 
brick_start_point_z = -half_box_depth

brick_num = 10  # x축과 z축 방향으로 배치될 벽돌의 개수
brick_row = 2


brick_margin = 5  # 벽돌 사이의 간격
brick_total_width = box_width - (brick_margin * (brick_num + 1))
brick_total_depth = box_depth - (brick_margin * (brick_num + 1))

brick_width = brick_total_width // brick_num
brick_depth = brick_total_depth // brick_num

# brick_width = box_width // brick_num
brick_height = (box_height/3) // (brick_row * 2)
# brick_depth = box_depth // brick_num

padX, padY, padZ = 0, 0, 0
ctrlPressed, shiftPressed = False, False
aPressed,wPressed, sPressed, dPressed = False, False, False,  False


bricks = [[[ True for _ in range(brick_num) ] for _ in range(brick_num)] for _ in range(brick_row)]

x = 0
y = 0
cam_x = 0

def setup():
    global sp_x, sp_y, sp_z
    global sp_dx, sp_dy, sp_dz
    global bricks, scaleFactor, x,y
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed,wPressed, sPressed, dPressed
    
    noiseDetail(15, 0.5)
    sp_x = 0
    sp_y = 0
    sp_z = 0
    size(1920, 980, P3D)
    

def draw():
    global game_state

    if game_state == "start_screen":
        draw_start_screen()
    elif game_state == "game":
        global sp_x, sp_y, sp_z
        global sp_dx, sp_dy, sp_dz
        global bricks
        global scaleFactor, x,y
        global padX, padY, padZ
        
        background(0)
        translate(width / 2+ x, height / 2+y, 0);
        
        rotateY(radians(x))
        rotateX(radians(y))
    
    
        #아웃 박스 그리기
        stroke(255)
        strokeWeight(4)
        noFill()
        box(box_width, box_height, box_depth)
        
        draw_brick_rows() #벽돌 그리기
        # pos_print() #벽돌 좌표 표시하기
        
        update_pad()
        # 공 움직임 설정
        pushMatrix()
        #화면 너비에 절반 + 현재 공 x 좌표, 화면 높이 절반 + 공 y 좌표, 너비 10 + 공 z 좌표
        translate(sp_x, sp_y, 10 + sp_z)
        directionalLight(255, 255, 255, -1, -1, -1)
        lights()
        # 공 색상 설정 (초록색)
        fill(0, 255, 0)
        noStroke()
        # print(width / 2 + sp_x, height / 2 + sp_y, 10 + sp_z)
        
        sphere(20)
        popMatrix()
        
        
        #racket 생성
        pushMatrix()
        translate(padX, padY, padZ)
        fill(187, 210, 235)
        box(box_width/2.5, box_height/30, box_depth/2.5)
        popMatrix()
    
        # 사각형 충돌 감지
        if sp_x < -half_box_width + 20 or sp_x > half_box_width - 20:
            sp_dx *= -1
        if sp_y < -half_box_height + 20 or sp_y > half_box_height - 20:
            sp_dy *= -1
        if sp_z < -half_box_depth + 20 or sp_z > half_box_depth - 20:
            sp_dz *= -1
    
        check_collision_with_racket()
        # 움직임 설정
        sp_x += sp_dx
        sp_y += sp_dy
        sp_z += sp_dz
        
        break_y = -275 + (brick_height * brick_row)  #-155
        row_pos = (sp_y + 275) // brick_height
        dep_pos = (sp_z + 200) // brick_depth
        col_pos = (sp_x + 200) // brick_width
        
        #벽돌 충돌 감지
        for i, b1 in enumerate(bricks):
            for j, b2 in enumerate(b1):
                for k, brick in enumerate(b2):
                    if brick:
                        brick_x = -half_box_width + (brick_width / 2) + brick_width * k + brick_margin * (k + 1)
                        brick_y = -half_box_height + (brick_height / 2) + brick_height * i + brick_margin * (i + 1)
                        brick_z = -half_box_depth + brick_depth * j + brick_margin * (j + 1)
                        
                        if (
                            brick_x - brick_width / 2 <= sp_x <= brick_x + brick_width / 2
                            and brick_y - brick_height / 2 <= sp_y <= brick_y + brick_height / 2
                            and brick_z - brick_depth / 2 <= sp_z <= brick_z + brick_depth / 2
                        ):
                            bricks[i][j][k] = False
                            sp_dy *= -1


def draw_start_screen():
    background(0)
    textSize(50)
    fill(255)
    textAlign(CENTER, CENTER)
    text("Brick Break Game", width / 2, height / 2 - 100)
    textSize(30)
    text("Click on the screen to get started", width / 2, height / 2)


    
def pos_print():
    textSize(32)
    fill(255)
    text("("+str(-200)+" "+str(-275)+" "+str(-200)+")", -200, -275, -200)
    text("("+str(-200)+" "+str(-275)+" "+str(200)+")", -200, -275, 200)
    text("("+str(200)+" "+str(275)+" "+str(200)+")", 200, 275, 200)
    text("("+str(-200)+" "+str(275)+" "+str(-200)+")", -200, 275, -200)
    text("("+str(200)+" "+str(-275)+" "+str(-200)+")", 200, -275, -200)
    text("("+str(200)+" "+str(275)+" "+str(-200)+")", 200, 275, -200)
    text("("+str(200)+" "+str(-275)+" "+str(200)+")", 200, -275, 200)
    text("("+str(-200)+" "+str(275)+" "+str(200)+")", -200, 275, 200)


def draw_brick_rows():
    global bricks

    for i, b1 in enumerate(bricks):
        for j, b2 in enumerate(b1):
            for k, brick in enumerate(b2):
                if brick:
                    pushMatrix()
                    translate(
                        max(min(-half_box_width + (brick_width / 2) + brick_width * k + brick_margin * (k + 1), half_box_width - (brick_width / 2)), -half_box_width + (brick_width / 2)),
                        max(min(-half_box_height + (brick_height / 2) + brick_height * i + brick_margin * (i + 1), half_box_height - (brick_height / 2)), -half_box_height + (brick_height / 2)),
                        max(min(-half_box_depth + brick_depth * j + brick_margin * (j + 1), half_box_depth - (brick_depth / 2)), -half_box_depth + (brick_depth / 2)),
                    )
                    # 펄린 노이즈 값을 사용하여 랜덤 색상을 생성합니다.
                    n = noise(i * 0.7, j * 0.7, k * 0.7)

                    r = map(n, 0, 1, 100, 100)
                    g = map(n, 0, 1, 50, 100)
                    b = map(n, 0, 1, 200, 255)

                    # 생성한 랜덤 색상을 사용하여 벽돌을 채웁니다.
                    fill(r, g, b)

                    box(brick_width, brick_height, brick_depth)
                    popMatrix()

    
def mousePressed():
    global game_state

    if game_state == "start_screen":
        game_state = "game"
        
def keyPressed():
    global x, y
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed,wPressed, sPressed, dPressed
    
    #회전 각도 초기화
    if key == 'r' or key == 'R':
        x, y = 0, 0

    #padMove
    
    if key == 'w' or key == 'W': wPressed = True
    if key == 'a' or key == 'A': aPressed = True
    if key == 's' or key == 'S': sPressed = True
    if key == 'd' or key == 'D': dPressed = True
        
    if keyCode == SHIFT: shiftPressed = True
    if keyCode == CONTROL: ctrlPressed = True

def keyReleased():
    global ctrlPressed, shiftPressed
    global aPressed, wPressed, sPressed, dPressed
    
    if key == 'w' or key == 'W': wPressed = False
    if key == 'a' or key == 'A': aPressed = False
    if key == 's' or key == 'S': sPressed = False
    if key == 'd' or key == 'D': dPressed = False
    
    if keyCode == SHIFT: shiftPressed = False
    if keyCode == CONTROL: ctrlPressed = False
    
def update_pad():
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed, wPressed, sPressed, dPressed
    
    if wPressed:
        newZ = padZ - 20
        if newZ >= -half_box_depth + box_depth / 5:
            padZ = newZ

    if sPressed:
        newZ = padZ + 20
        if newZ <= half_box_depth - box_depth / 5:
            padZ = newZ

    if aPressed:
        newX = padX - 20
        if newX >= -half_box_width + box_width / 5:
            padX = newX

    if dPressed:
        newX = padX + 20
        if newX <= half_box_width - box_width / 5:
            padX = newX

    if shiftPressed:
        newY = padY - 10
        if newY >= -half_box_height + box_height / 60:
            padY = newY

    if ctrlPressed:
        newY = padY + 10
        if newY <= half_box_height - box_height / 60:
            padY = newY

        
def mouseDragged():
    global x, y
    x -= (mouseX - pmouseX) * 0.03
    y -= (mouseY - pmouseY) * 0.03
    
def check_collision_with_racket():
    global padX, padY, padZdddd
    global sp_x, sp_y, sp_z
    global sp_dx, sp_dy, sp_dz

    # 라켓의 경계값 계산
    racket_half_width = box_width / 5
    racket_half_height = box_height / 60
    racket_half_depth = box_depth / 5

    # 공의 좌표가 라켓 내부에 있는지 확인
    if (
        padX - racket_half_width <= sp_x <= padX + racket_half_width
        and padY - racket_half_height <= sp_y <= padY + racket_half_height
        and padZ - racket_half_depth <= sp_z <= padZ + racket_half_depth
    ):
        # 공이 라켓에 닿았다면, 반사 각도를 조정하고 공의 속도를 변경
        sp_dx *= -1
        sp_dy *= -1
        sp_dz *= -1

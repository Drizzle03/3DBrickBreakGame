# 게임 시작 상태
game_state = "start" #( start - 초기화면 / game - 게임 화면 / end_clear, end_over - 게임 종료 화면)

# 게임 라이프 설정
life_num = 10
life = life_num

# 구 x, y, z 좌표 설정
sp_x = 0
sp_y = 0
sp_z = 0

# 구 x 속도, y속도, z의 속도 설정
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

brick_num = 1  # x축과 z축 방향으로 배치될 벽돌의 개수
brick_row = 2 # 벽돌 줄 개수


brick_margin = 5  # 벽돌 사이의 간격
brick_total_width = box_width - (brick_margin * (brick_num + 1))
brick_total_depth = box_depth - (brick_margin * (brick_num + 1))
# 700 - (5*(6 + 1)) -> 벽돌들의 순수 총 너비 박스의 너비 - (박스 여백 (벽돌의 개수+1))


brick_width = brick_total_width // brick_num #위에서 벽돌들의 순수 총 너비를 계산한걸 단순 나누기
brick_height = (box_height/3) // (brick_row * 2) # 박스의 1/3 위치에 위치, 해당 위치에서 추가적으로 벽돌 행의 수 * 2 만큼 위치를 확보할 수 있는 벽돌 높이 설정
brick_depth = brick_total_depth // brick_num #위에서 벽돌들의 순수 총 깊이를 계산한걸 단순 나누기


padX, padY, padZ = 0, 0, 0
ctrlPressed, shiftPressed = False, False
aPressed,wPressed, sPressed, dPressed = False, False, False,  False

#벽돌 배열 추가
bricks = [[[ True for _ in range(brick_num) ] for _ in range(brick_num)] for _ in range(brick_row)]

x = 0
y = 0

print(half_box_width, brick_width, brick_margin)
print(half_box_height, brick_height, brick_margin)
print(half_box_depth, brick_depth, brick_margin)

print(half_box_width + (brick_width / 2) + brick_width * 0 + brick_margin * (0+1))

def setup():
    global sp_x, sp_y, sp_z
    global sp_dx, sp_dy, sp_dz
    global bricks, scaleFactor, x,y
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed,wPressed, sPressed, dPressed
    global life
    
    sp_x = 0
    sp_y = 0
    sp_z = 0
    size(1920, 980, P3D)
    

def draw():
    global game_state
    # 게임 시작 창 띄울지 결정
    if game_state == "start":
        draw_start_screen()
    
    #게임 클리어
    elif game_state == "end_clear":
        draw_end_clear_screen()
        
    #게임 오버
    elif game_state == "end_over":
        draw_end_over_screen()
    
    # 게임 시작 시
    elif game_state == "game":
        global sp_x, sp_y, sp_z
        global sp_dx, sp_dy, sp_dz
        global bricks
        global scaleFactor, x,y
        global padX, padY, padZ
        global life
        checkgameClear()
        
        background(0)
        # 마우스 클릭에 따라 화면 전환 설정, 위치, 회전 각도 설정
        translate(width / 2+ x, height / 2+y, 0);
        rotateY(radians(x))
        rotateX(radians(y))
    
        #아웃 박스 그리기
        stroke(255)
        strokeWeight(4)
        noFill()
        box(box_width, box_height, box_depth)
        
        # 벽돌 그리기
        draw_brick_rows()
        pos_print() #벽돌 끝점 좌표 표시

        # 공 움직임 설정
        pushMatrix()
        #화면 너비에 절반 + 현재 공 x 좌표, 화면 높이 절반 + 공 y 좌표, 너비 10 + 공 z 좌표
        translate(sp_x, sp_y-20, 10 + sp_z)
        
        #공에 입체감을 주기 위해 빛 설정
        directionalLight(255, 255, 255, -1, -1, -1)
        lights()
        
        # 공 색상 설정 및 생성 (초록색)
        fill(0, 255, 0)
        noStroke()
        sphere(20)
        popMatrix()
        
        
        # 라켓 방향키 조작 적용
        update_pad()
        
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
    
        # 라켓 충돌 감지
        check_collision_with_racket()
        
        
        # 움직임 설정
        sp_x += sp_dx
        sp_y += sp_dy
        sp_z += sp_dz
        

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



# 게임 시작 화면 설정 함수
def draw_start_screen():
    background(0)
    textSize(50)
    fill(255)
    textAlign(CENTER, CENTER)
    text("Brick Break Game", width / 2, height / 2 - 100)
    textSize(30)
    text("Click on the screen to get started", width / 2, height / 2)
    
# 게임 클리어 종료화면 설정
def draw_end_clear_screen():
    background(0)
    textSize(50)
    fill(255)
    textAlign(CENTER, CENTER)
    text("Game Clear!!", width / 2, height / 2 - 100)
    textSize(50)
    text("To restart the game, click this screen.", width / 2, height / 2)
    
    
# 게임 클리어 종료화면 설정
def draw_end_over_screen():
    background(0)
    textSize(50)
    fill(255)
    textAlign(CENTER, CENTER)
    text("Brick Break Game", width / 2, height / 2 - 100)
    textSize(30)
    text("To restart the game, click this screen.", width / 2, height / 2)


# 벽돌 끝 점 출력 함수 (개발 보조용 함수)
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


# 벽돌 그리기 함수
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
                    
                    
                    n = noise(i * 0.2, j * 0.4, k * 0.7)
                    r = map(n, 0, 1, 0, 255)
                    g = map(n, 0, 1, 0, 255)
                    b = map(n, 0, 1, 0, 255)
                    
                    fill(r, g, b)

                    box(brick_width, brick_height, brick_depth)
                    popMatrix()


# 마우스 클릭 설정 - 첫 화면 게임 시작    
def mousePressed():
    global game_state
    global bricks

    if game_state == "start":
        game_state = "game"
        
    elif game_state == "end_clear":
        bricks = [[[ True for _ in range(brick_num) ] for _ in range(brick_num)] for _ in range(brick_row)]
        game_state = "game"
        
        
# 라켓 방향키 조작 설정
def keyPressed():
    global x, y
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed,wPressed, sPressed, dPressed
    
    #회전 각도 초기화 키
    if key == 'r' or key == 'R':
        x, y = 0, 0

    #패드 이동 설정 키가 눌려있을 때 눌림 변수 True로 변경
    #x,z 축 이동 설정
    if key == 'w' or key == 'W': wPressed = True
    if key == 'a' or key == 'A': aPressed = True
    if key == 's' or key == 'S': sPressed = True
    if key == 'd' or key == 'D': dPressed = True
    
    #y축 이동 설정
    if keyCode == SHIFT: shiftPressed = True
    if keyCode == CONTROL: ctrlPressed = True

# 키가 눌렸다 놓아질 때 False로 변경함
def keyReleased():
    global ctrlPressed, shiftPressed
    global aPressed, wPressed, sPressed, dPressed
    
    #x,z축 이동 설정
    if key == 'w' or key == 'W': wPressed = False
    if key == 'a' or key == 'A': aPressed = False
    if key == 's' or key == 'S': sPressed = False
    if key == 'd' or key == 'D': dPressed = False
    
    #y축 이동 설정
    if keyCode == SHIFT: shiftPressed = False
    if keyCode == CONTROL: ctrlPressed = False
    
    
# 패드 이동 설정
def update_pad():
    global padX, padY, padZ
    global ctrlPressed, shiftPressed
    global aPressed, wPressed, sPressed, dPressed
    
    # 키가 눌렸을 때, 
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
    if (padX - racket_half_width <= sp_x <= padX + racket_half_width
        and padY - racket_half_height <= sp_y <= padY + racket_half_height
        and padZ - racket_half_depth <= sp_z <= padZ + racket_half_depth):
        # 공이 라켓에 닿았다면, 반사 각도를 조정하고 공의 속도를 변경
        sp_dx *= -1
        sp_dy *= -1
        sp_dz *= -1
        
        
# 게임 클리어 확인 함수 개선
def checkgameClear():
    check = True
    global bricks #가독성 차원의 전역변수 선언
    global game_state #게임 상태창
    
    for i, b1 in enumerate(bricks):
        for j, b2 in enumerate(b1):
            for k, b3 in enumerate(b2):
                if bricks[i][j][k] == True:
                    check = False
                    break
            if not check:
                break
        if not check:
            break
        
    if check:
        game_state = "end_clear"
        
    

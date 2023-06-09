import pygame
import random
import sys
import sqlite3

#매개 변수로 받은 객체 좌표위치에 그리기
def paintEntity(entity, x, y) :
   screen.blit(entity, (int(x), int(y)))


#게임 실행
def playGame() :
    global screen
    noteObjects = [] #[존재 여부 True/False] [이미지 및 x좌표(출현 x위치) 0 ~ 3] [y좌표]
    for i in range(30) :
        noteObjects.append([False, 0, 0])
    noteDropCycle = 500 #노트가 내려오는 주기. 숫자 작을수록 자주 내려옴
    noteCycle = 0 #noteSpeed 틱마다 노트를 내려보냄
    selectNoteIndex = 0 #다음 출발 시킬 노트 인덱스
    pushing = [False] * 4 #좌상하우 각 방향키가 눌리는 중인지 여부
    evaluationDisplay = [0, 0] #[엑설런트, 굳 등 표시 카운터] [표시 할 단어 miss, good, grate, excellent 순서]
    score = 0
    heart = 3
    screenmode = 0 #화면 모드(0 = 메인 화면, 1 = 게임중, 2 = 점수 조회, 3 = 게임 패배 후 결과화면, 4 = 랭킹 리스트 초기화)
    playerName = ""
    ranking = [] #랭킹 리스트
    finalScore = None


    # 게임 실행 중 무한 반복
    while True :
        (pygame.time.Clock()).tick(1000)  #노트 속도 조절
        screen.blit(background, (0, 0))
        font = pygame.font.Font("./font/NanumGothic.ttf", 30)

## ************************* 메인 화면 ************************* ##
        if(screenmode == 0) :
            for e in pygame.event.get() :
                if e.type in [pygame.QUIT]  :
                    pygame.quit()
                    sys.exit()
                elif e.type in [pygame.KEYDOWN] : #키 눌렀을 때
                    if e.key == pygame.K_UP : #윗쪽 방향키는 게임 초기화 및 게임 시작
                        noteObjects = [] #[존재 여부 True/False] [이미지 및 x좌표(출현 x위치) 0 ~ 3] [y좌표]
                        for i in range(30) :
                            noteObjects.append([False, 0, 0])
                        noteDropCycle = 500
                        noteCycle = 0
                        selectNoteIndex = 0
                        pushing = [False] * 4
                        evaluationDisplay = [0, 0]
                        score = 0
                        heart = 3
                        playerName = ""
                        finalScore = None
                        screenmode = 1
                    if e.key == pygame.K_DOWN : #아랫쪽 방향키는 점수 조회
                        screenmode = 4
                    if e.key == pygame.K_ESCAPE :
                        screenmode = 5

            textMain = font.render("타이밍 맞추기 게임", True, (255, 0, 255)) #게임 시작 버튼
            screen.blit(textMain, (130, 150))
            paintEntity(pygame.image.load(nonPushImages[1]), 100, 400)
            textGameStart = font.render("GameStart", True, (255, 255, 255)) #게임 시작 버튼
            screen.blit(textGameStart, (200, 420))
            paintEntity(pygame.image.load(nonPushImages[2]), 100, 500)
            textScoreInquiry = font.render("랭킹 보드", True, (255, 255, 255)) #점수 조회 버튼
            screen.blit(textScoreInquiry, (200, 520))
                        
## ************************* 게임 화면 ************************* ##
        elif(screenmode == 1) :
            # 키보드나 마우스 이벤트가 들어오는지 체크한다.
            for e in pygame.event.get() :
                if e.type in [pygame.QUIT]  :
                    pygame.quit()
                    sys.exit()

                if e.type in [pygame.KEYDOWN] : #키 눌렀을 때
                    if e.key == pygame.K_LEFT :
                        for y in range(len(noteObjects)) :
                            if((noteObjects[y][0] == True) and (noteObjects[y][1] == 0) and (noteObjects[y][2] >= 590) and (noteObjects[y][2] <= 610)):
                                score += 3
                                evaluationDisplay = [100, 3]
                                noteObjects[y] = [False, 0, 0]
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 0) and (noteObjects[y][2] >= 580) and (noteObjects[y][2] <= 620)):
                                score += 2
                                evaluationDisplay = [100, 2]
                                noteObjects[y] = [False, 0, 0]
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 0) and (noteObjects[y][2] >= 570) and (noteObjects[y][2] <= 630)):
                                score += 1
                                evaluationDisplay = [100, 1]
                                noteObjects[y] = [False, 0, 0]
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 0) and (noteObjects[y][2] >= 560) and (noteObjects[y][2] <= 640)):
                                score += 0
                                evaluationDisplay = [100, 0]
                                noteObjects[y] = [False, 0, 0]
                                heart -= 1
                        pushing[0] = True
                    elif e.key == pygame.K_UP :
                        for y in range(len(noteObjects)) :
                            if((noteObjects[y][0] == True) and (noteObjects[y][1] == 1) and (noteObjects[y][2] >= 590) and (noteObjects[y][2] <= 610)):
                                score += 3
                                evaluationDisplay = [100, 3]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 1) and (noteObjects[y][2] >= 580) and (noteObjects[y][2] <= 620)):
                                score += 2
                                evaluationDisplay = [100, 2]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 1) and (noteObjects[y][2] >= 570) and (noteObjects[y][2] <= 630)):
                                score += 1
                                evaluationDisplay = [100, 1]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 1) and (noteObjects[y][2] >= 560) and (noteObjects[y][2] <= 640)):
                                score += 0
                                evaluationDisplay = [100, 0]
                                noteObjects[y][0] = False
                                heart -= 1
                        pushing[1] = True
                    elif e.key == pygame.K_DOWN :
                        for y in range(len(noteObjects)) :
                            if((noteObjects[y][0] == True) and (noteObjects[y][1] == 2) and (noteObjects[y][2] >= 590) and (noteObjects[y][2] <= 610)):
                                score += 3
                                evaluationDisplay = [100, 3]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 2) and (noteObjects[y][2] >= 580) and (noteObjects[y][2] <= 620)):
                                score += 2
                                evaluationDisplay = [100, 2]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 2) and (noteObjects[y][2] >= 570) and (noteObjects[y][2] <= 630)):
                                score += 1
                                evaluationDisplay = [100, 1]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 2) and (noteObjects[y][2] >= 560) and (noteObjects[y][2] <= 640)):
                                score += 0
                                evaluationDisplay = [100, 0]
                                noteObjects[y][0] = False
                                heart -= 1
                        pushing[2] = True
                    elif e.key == pygame.K_RIGHT :
                        for y in range(len(noteObjects)) :
                            if((noteObjects[y][0] == True) and (noteObjects[y][1] == 3) and (noteObjects[y][2] >= 590) and (noteObjects[y][2] <= 610)):
                                score += 3
                                evaluationDisplay = [100, 3]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 3) and (noteObjects[y][2] >= 580) and (noteObjects[y][2] <= 620)):
                                score += 2
                                evaluationDisplay = [100, 2]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 3) and (noteObjects[y][2] >= 580) and (noteObjects[y][2] <= 620)):
                                score += 1
                                evaluationDisplay = [100, 1]
                                noteObjects[y][0] = False
                            elif((noteObjects[y][0] == True) and (noteObjects[y][1] == 3) and (noteObjects[y][2] >= 560) and (noteObjects[y][2] <= 640)):
                                score += 0
                                evaluationDisplay = [100, 0]
                                noteObjects[y][0] = False
                                heart -= 1
                        pushing[3] = True

                if e.type in [pygame.KEYUP] : #키 뗐을때
                    if e.key == pygame.K_LEFT :
                        pushing[0] = False
                    if e.key == pygame.K_UP :
                        pushing[1] = False
                    if e.key == pygame.K_DOWN :
                        pushing[2] = False
                    if e.key == pygame.K_RIGHT :
                        pushing[3] = False


            noteCycle += 1
            if noteCycle >= noteDropCycle: #noteDropCycle틱마다 노트를 내려보냄
                noteObjects[selectNoteIndex] = [True, random.randrange(4), -20]
                selectNoteIndex += 1
                if selectNoteIndex >= len(noteObjects) :
                    selectNoteIndex = 0
                if noteDropCycle > 100 :
                    noteDropCycle -= 5 #점점 빨라지게
                noteCycle = 0

            for i in range(len(pushing)) : #키 누름 여부에 따라 방향키 모양 표시
                if pushing[i] == False :
                    paintEntity(pygame.image.load(nonPushImages[i]), noteFixX[i] + 10, 620)
                else :
                    paintEntity(pygame.image.load(pushImages[i]), noteFixX[i] + 10, 620)
                

            for i in range(len(noteObjects)) : #noteObjects[i][0]이 1이면 실행중인 노트
                if noteObjects[i][0] == True :
                    paintEntity(pygame.image.load(noteImages[noteObjects[i][1]]), noteFixX[noteObjects[i][1]], noteObjects[i][2])
                    noteObjects[i][2] += 1
                    if noteObjects[i][2] == 699 :
                        heart -= 1
                        evaluationDisplay = [100, 0]
                        noteObjects[i] = [False, 0, 0]

            if(evaluationDisplay[0] > 0) :
                paintEntity(pygame.image.load(evaluationImages[evaluationDisplay[1]]), 101, 450)
                evaluationDisplay[0] -= 1

            textScore = font.render("Score: " + str(score), True, (255, 255, 255)) #점수 표시
            screen.blit(textScore, (200, 50))
            textHeart = font.render("Heart: " + str(heart), True, (255, 0, 0)) #목숨 표시
            screen.blit(textHeart, (200, 100))
            if heart <= 0 :
                finalScore = score
                playerName = ""
                screenmode = 3

## ************************* 점수 화면 ************************* ##
        elif(screenmode == 2):
            for e in pygame.event.get() :
                if e.type in [pygame.QUIT]  :
                    pygame.quit()
                    sys.exit()
                if e.type in [pygame.KEYDOWN] :
                    if e.key == pygame.K_RETURN :
                        screenmode = 0
            textRANKING = font.render("RANKING", True, (255, 0, 255)) #목숨 표시
            screen.blit(textRANKING, (180, 50))
            textPLAYERSCORE = font.render("SCORE     /     PLAYER", True, (0, 255, 255)) #목숨 표시
            screen.blit(textPLAYERSCORE, (110, 100))
            textEXIT = font.render("PRESS ENTER to Exit", True, (0, 0, 255)) #목숨 표시
            screen.blit(textEXIT, (110, 650))

            for i in range(len(ranking)) :
                textSCOREBoard = font.render("%3d" % (ranking[i][1]), True, (255, 255, 255)) #목숨 표시
                screen.blit(textSCOREBoard, (130, (i + 3) * 50))
                textPLAYERBoard = font.render("%6s" % (ranking[i][0]), True, (255, 255, 255)) #목숨 표시
                screen.blit(textPLAYERBoard, (280, (i + 3) * 50))
            

        
## ************************* 결과 화면 ************************* ##
        elif(screenmode == 3) :
            for e in pygame.event.get() :
                if e.type in [pygame.QUIT]  :
                    pygame.quit()
                    sys.exit()
                if e.type in [pygame.KEYDOWN] :
                    if len(playerName) < 5 :
                        if ((e.dict['unicode'] >= 'a') and (e.dict['unicode'] <= 'z')) or ((e.dict['unicode'] >= 'A') and (e.dict['unicode'] <= 'Z')) :
                            playerName += e.dict['unicode'].upper()
                    if e.key == pygame.K_RETURN :
                        mydb = sqlite3.connect("./db/mydb")
                        cursor = mydb.cursor()
                        cursor.execute("SELECT COUNT (*) FROM sqlite_master WHERE type='table' AND name='myTable'")
                        result = cursor.fetchone()
                        if result[0] == 0 :
                            cursor.execute("CREATE TABLE myTable (playerName char(5), score int)")
                        cursor.execute(f"INSERT INTO myTable VALUES('{playerName}', {finalScore})")
                        mydb.commit()
                        mydb.close()
                        screenmode = 4

            
            textGameover = font.render("GAME OVER!!", True, (255, 0, 0))
            screen.blit(textGameover, (150, 200))
            textFinalScore = font.render("Final Score: " + str(finalScore), True, (255, 0, 0))
            screen.blit(textFinalScore, (150, 250))
            textPlayerName = font.render("이름 입력: " + str(playerName), True, (255, 255, 255))
            screen.blit(textPlayerName, (150, 350))
            textNEXT = font.render("PRESS ENTER to Next", True, (0, 0, 255))
            screen.blit(textNEXT, (100, 500))
## ************************* 랭킹 초기화 ************************* ##
        elif(screenmode == 4) :
            mydb = sqlite3.connect("./db/mydb")
            cursor = mydb.cursor()
            cursor.execute("SELECT COUNT (*) FROM sqlite_master WHERE type='table' AND name='myTable'")
            result = cursor.fetchone()
            if result[0] == 0 :
                cursor.execute("CREATE TABLE myTable (playerName char(5), score int)")
            cursor.execute("SELECT * FROM myTable ORDER BY score DESC")
            ranking = []
            for i in range(10):
                row = cursor.fetchone()
                if row == None :
                    break
                else:
                    ranking.append(row)
            mydb.close()
            screenmode = 2
## ************************* 오류 방지 ************************* ##
        elif(screenmode == 5) :
            for e in pygame.event.get() :
                if e.type in [pygame.QUIT]  :
                    pygame.quit()
                    sys.exit()
                if e.type in [pygame.KEYDOWN] :
                    if e.key == pygame.K_RETURN :
                        pygame.quit()
                        sys.exit()
                    if e.key == pygame.K_ESCAPE :
                        screenmode = 0
            textEXIT = font.render("게임을 끝내시겠습니까?", True, (255, 255, 255))
            screen.blit(textEXIT, (100, 200))
            textEndtoExit = font.render("끝내려면 ENTER", True, (255, 0, 0))
            screen.blit(textEndtoExit, (145, 500))
        
        else :
            screenmode = 0


        pygame.display.update()


# 전역변수 선언
swidth, sheight = 500, 700
screen = None
background = pygame.image.load("./images/background.png")
noteImages = ["./images/rednote.png", "./images/yellownote.png", "./images/bluenote.png", "./images/greennote.png"]
nonPushImages = ["./images/defaultleft.png", "./images/defaultup.png", "./images/defaultdown.png", "./images/defaultright.png"]
pushImages = ["./images/pushleft.png", "./images/pushup.png", "./images/pushdown.png", "./images/pushright.png"]
evaluationImages = ["./images/miss.png", "./images/good.png", "./images/great.png", "./images/excellent.png"]
noteFixX = [51, 151, 251, 351]



# 초기 세팅
pygame.init()
screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('타이밍 맞추기 게임')

noteSize = pygame.image.load("./images/rednote.png").get_rect().size


#사용 할 객체에 대한 준비


#게임 프로그램 시작
playGame()
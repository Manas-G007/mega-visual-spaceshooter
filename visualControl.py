import pygame as pyg
import numpy as np
from pygame import mixer
import sys
sys.path.insert(0, './entity')
from player import Player
from enemy import Enemy
from laser import Laser
from button import Button as Btn

# gesture control
import time,cv2
from handtracker import HandTracker

ip_address = "192.168.29.179"
port = "8080"

# Set the URL for DroidCam
url = f"http://{ip_address}:{port}/video"

cap=cv2.VideoCapture(0)
pTime=0
reduceTray=100

# pyg src

pyg.init()

# style
screenSize=800,600
c1=255,255,255

# level
level=[50,100,150,200]

running=True
enemy_win=False
hiScore=0
score=0
scoreCod=10,40
hiScoreCod=10,10
font=pyg.font.Font("freesansbold.ttf",32)

# sound effect
mixer.music.load("./assets/music/bg.mp3")
mixer.music.play(-1)

disp=pyg.display
# screen config
screen=disp.set_mode(screenSize)
disp.set_caption("mega game")
icon=pyg.image.load("./assets/img/icon.png")
disp.set_icon(icon)

# player
playerSize=64
player=Player()
laser=Laser()
btn=Btn()

# enemies
enemies=[]
no_of_enemy=6
for i in range(no_of_enemy):
    enemies.append(Enemy())

# bg
bg=pyg.image.load("./assets/img/bg.png")


def movement(key):
    if key==pyg.K_LEFT:
        player.setDirX(-player.speed)
    if key==pyg.K_RIGHT:
        player.setDirX(player.speed)
    if key==pyg.K_UP:
        player.setDirY(-player.speed)
    if key==pyg.K_DOWN:
        player.setDirY(player.speed)

def defaultX(key):
    if key==pyg.K_LEFT or key==pyg.K_RIGHT:
        player.setDirX(0)

def defaultY(key):
    if key==pyg.K_UP or key==pyg.K_DOWN:
        player.setDirY(0)

def boundaryCondition():
    if player.posX<=0:
        player.posChangeX=0
    if player.posX>=screenSize[0]-playerSize:
        player.posChangeX=0
    if player.posY<=screenSize[1]-200:
        player.posChangeY=0
    if player.posY>=screenSize[1]-playerSize:
        player.posChangeY=0

def renderPlayer():
    screen.blit(player.player,(player.posX,player.posY))

def renderEnemy():
    for enemy in enemies:
        screen.blit(enemy.enemy,(enemy.x,enemy.y))

def renderLaser():
    if laser.state:
        screen.blit(laser.laser,(laser.x,laser.y))

def isHit(id):
    global score,enemies
    distance=np.hypot((laser.x-enemies[id].x),(laser.y-enemies[id].y))

    if laser.state and distance < 30:
            mixerPlayer("./assets/music/hit.wav")
            score+=10
            if score in level:
                for enemy in enemies:
                    enemy.difficult(2.5)
            laser.setState(False)
            enemies[id].x=np.random.randint(0,screenSize[0]-playerSize)
            enemies[id].y=np.random.randint(0,100)

def updateScore():
    scoreText=font.render(f"Score : {score}",True,c1)
    hiScoreText=font.render(f"Hi Score : {hiScore}",True,c1)
    screen.blit(scoreText,scoreCod)
    screen.blit(hiScoreText,hiScoreCod)

def gameOver():
    mixer.music.pause()
    game_over=pyg.font.Font("freesansbold.ttf",50)
    game_over_text=game_over.render("Game Over",True,c1)
    screen.blit(game_over_text,(screenSize[0]/2 - 140,screenSize[1]/2 - 50))

def mixerPlayer(path):
    try:
        mixer.Sound(path).play()
    except pyg.error as error:
        print(error)

def renderBtn():
    pyg.draw.rect(screen,c1,btn.rect)
    screen.blit(btn.text,(btn.x+20,btn.y+10))

def resetGame():
    global enemy_win,enemies,hiScore,score
    hiScore=score if score>hiScore else hiScore
    score=0
    enemy_win=False
    mixer.music.play()
    for _ in range(no_of_enemy):
        enemies.append(Enemy())

def shot(key,x,y,visual=False):
    if visual and not laser.state:
        mixerPlayer('./assets/music/laser.wav')
        laser.setState(True)
        laser.setPos(x,y)
        return
    
    if key==pyg.K_SPACE and not laser.state:
        mixerPlayer('./assets/music/laser.wav')
        laser.setState(True)
        laser.setPos(x,y)

def getDist(a,b):
    x1,y1=a
    x2,y2=b
    return np.hypot((x1-x2),(y1-y2))<80



detect=HandTracker()
while running:
    # visual
    success,img=cap.read()
    img=detect.findHand(img)
    ih,iw,ic=img.shape
    focusPoint=[8,12]
    lmList=detect.getPos(img,focusPoint)

    if lmList:
        a1=lmList[focusPoint[0]][1],lmList[focusPoint[0]][2]
        b1=lmList[focusPoint[0]-3][1],lmList[focusPoint[0]-3][2]
        d1=getDist(a1,b1)
        

        if (a1[0]>reduceTray and a1[0]<iw-reduceTray) and (a1[1]>reduceTray and a1[1]<ih-reduceTray):
            relX=int(np.interp(a1[0],[reduceTray,iw-reduceTray],[800,0]))
            relY=int(np.interp(a1[1],[reduceTray,ih-reduceTray],[400,600]))
            
            a2=lmList[focusPoint[1]][1],lmList[focusPoint[1]][2]
            b2=lmList[focusPoint[1]-3][1],lmList[focusPoint[1]-3][2]
            d2=getDist(a2,b2)
            if not d2 and not d1:
                shot(None,relX,relY,True)
            elif not d1:
                player.setPos(relX,relY)
    #------- 

    # events
    for e in pyg.event.get():
        if e.type==pyg.QUIT:
            running=False
        # if e.type==pyg.KEYDOWN:
            # movement(e.key)
            # shot(e.key,player.posX,player.posY)
            # pass
                

        # if e.type==pyg.KEYUP:
        #     defaultX(e.key)
        #     defaultY(e.key)
        
        if e.type==pyg.MOUSEBUTTONDOWN:
            if btn.rect.collidepoint(pyg.mouse.get_pos()) and enemy_win:
                resetGame()

    
    
    if enemy_win:
        renderBtn()
        gameOver()
    else:
        # live update
        # player.setPos(player.posX+player.posChangeX,
        #             player.posY+player.posChangeY)

        for enemy in enemies:
            enemy.setPosX(-enemy.enemySpeed)
            if enemy.y>screenSize[1]-200:
                enemies.clear()
                enemy_win=True
                break
            if enemy.x<=0:
                enemy.setChangeX(-enemy.enemySpeed)
                enemy.setDown()
            if enemy.x>=screenSize[0]-playerSize:
                enemy.setChangeX(-enemy.enemySpeed)
                enemy.setDown()

        # laser movement
        if laser.state and laser.y>0:
            laser.setPosY(laser.changeY)
        else:
            laser.setState(False)

        for id,enemy in enumerate(enemies):
            isHit(id)
        
        boundaryCondition()

        screen.blit(bg,(0,0))
        renderEnemy()
        renderLaser()
        renderPlayer()
        updateScore()


    # visual
    cTime=time.time()
    fps=int(1/(cTime-pTime))
    pTime=cTime


    cv2.rectangle(img,(reduceTray,reduceTray),(iw-reduceTray,ih-reduceTray),c1,2)
    cv2.putText(img,f"FPS : {fps}",(10,30),2,1,c1)
    cv2.imshow("Tracking",img)
    cv2.waitKey(10)
    # -----

    disp.update()

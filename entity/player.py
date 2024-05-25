import sys
sys.path.insert(0, '../')
import pygame as pyg
import screenConfig as sc

class Player:
    def __init__(self):
        self.player=pyg.image.load("assets/img/spaceship.png")
        self.posX,self.posY=sc.screenSize[0]/2 - sc.playerSize/2,sc.screenSize[1] - sc.playerSize
        self.posChangeX,self.posChangeY=0,0
        self.speed=0.5

    def setPos(self,x,y):
        self.posX,self.posY=x,y
    
    def setDirX(self,val):
        self.posChangeX=val
    
    def setDirY(self,val):
        self.posChangeY=val
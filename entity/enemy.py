import sys
sys.path.insert(0, '../')
import pygame as pyg
import screenConfig as sc
import numpy as np

class Enemy:
    def __init__(self):
        self.enemy=pyg.image.load("assets/img/aline.png")
        self.x=np.random.randint(0,sc.screenSize[0]-sc.playerSize)
        self.y=np.random.randint(0,100)
        self.enemySpeed=0.5
        self.enemyDown=10
        self.changeX=-self.enemySpeed

    def setPosX(self,x):
        self.x+=x
    
    def setDown(self):
        self.y+=self.enemyDown

    def setChangeX(self,val):
        self.enemySpeed=val
    
    def difficult(self,factor):
        self.enemySpeed*=factor
        self.enemyDown*=factor/2
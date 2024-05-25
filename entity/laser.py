import pygame as pyg
import sys
sys.path.insert(0, '../')

class Laser:
    def __init__(self):
        self.laser=pyg.image.load("assets/img/laser.png")
        self.state=False
        self.x=0
        self.y=0
        self.speed=4
        self.changeY=-self.speed
    
    def setState(self,val):
        self.state=val

    def setPos(self,x,y):
        self.x,self.y=x,y

    def setPosY(self,y):
        self.y+=y
import sys
sys.path.insert(0, '../')
import pygame as pyg
import screenConfig as sc

class Button:
    def __init__(self):
        self.width=240
        self.height=60
        self.x=sc.screenSize[0]/2 - self.width/2
        self.y=(sc.screenSize[1]/2 - self.height/2)+50
        self.rect=pyg.Rect(self.x,self.y,self.width,self.height)
        self.text=pyg.font.Font("freesansbold.ttf",38).render("Play Again",True,(0,0,0))
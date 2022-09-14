import tkinter as tk
from tkinter import *
from random import randint
import random
from playsound import playsound
import time

def creat_image():#creat all the image
    global flag_image,dirt,block_image,blockq_image,blockq2_image,cloud,cactus_image,saw_image
    dirt=PhotoImage(file = "./map/dirt.gif")
    block_image=PhotoImage(file = "./map/block.gif")
    blockq_image=PhotoImage(file = "./map/blockq.gif")
    blockq2_image=PhotoImage(file = "./map/blockq2.gif")
    cloud=[]
    cloud.append(PhotoImage(file = "./map/cloud1.gif"))
    cloud.append(PhotoImage(file = "./map/cloud2.gif"))
    cloud.append(PhotoImage(file = "./map/cloud3.gif"))
    cloud.append(PhotoImage(file = "./map/cloud4.gif"))
    cloud.append(PhotoImage(file = "./map/cloud5.gif"))
    cactus_image=PhotoImage(file = "./enemy/cactus.png")
    flag_image=PhotoImage(file = "./map/destination.png")
    saw_image=[]
    for n in range(0,4):
        saw_image.append(PhotoImage(file="./enemy/SAW"+str(n)+".png"))

class cactus():
    def __init__(self,x,y,canvas):
        global cactus_image
        self.x=x
        self.y=y
        self.image=cactus_image
        self.position=[]
        self.canvas=canvas
    def draw(self):
        self.position.append(self.canvas.create_image(self.x,self.y,image=self.image))
    
      
def clouda(canvas):
    global cloud,cp,c1_list,c2_list
    for a in range (0,21):
        again=False
        nc=randint(0,4)
        c1=randint(0,45)
        c1=c1*60
        while c1 in c1_list:
            c1=randint(0,45)
            c1=c1*60
        c1_list.append(c1)   
        c2=randint(1,8)
        c2=c2*20
        cp.append(canvas.create_image(c1,c2,image=cloud[nc]))
        

class block():
    def __init__(self, x, y, canvas):
        global block_image
        self.x = x
        self.y = y
        self.image=block_image
        self.bp=[]#block picture (in the sky)
        self.canvas=canvas
    def draw(self):
        self.bp.append(self.canvas.create_image(self.x,self.y,image=self.image))
class blockq ():
    def __init__(self, x, y ,canvas):
        global blockq_image,blockq2_image
        self.x = x
        self.y = y
        self.image=blockq_image
        self.bqp=[]#question block picture
        self.canvas=canvas
        self.type=0
        self.cactus=None
        self.hit=False
    def draw(self):
        self.bqp.append(self.canvas.create_image(self.x,self.y,image=self.image))
    def collide(self):#question block and pikachu
        if not (self.hit):
            self.image=blockq2_image
            self.draw()
            self.type=randint(1,7)
            if self.type==1:
                playsound("./sound/cactus.wav",block=False)
                self.cactus=cactus(self.x,425,self.canvas)
                self.cactus.draw()
            elif self.type==2:
                playsound("./sound/cactus.wav",block=False)
                self.cactus=cactus(self.x,313,self.canvas)
                self.cactus.draw()
            elif self.type==6:
                playsound("./sound/hit.wav",block=False)
            elif self.type==3:
                playsound("./sound/hit.wav",block=False)
            elif self.type==5:
                playsound("./sound/hit.wav",block=False)
            elif self.type==4 or self.type==7:
                playsound("./sound/question.wav",block=False)
            self.hit=True
            return self.type
        
        
def blocka(canvas):
    global block_list,blockq0_list,blockq1_list
    #the blocks in the sky(can not be at the begining)
    for  a in range(0,7):
        Xb=randint(5,80)
        Xb=Xb*30
        block_list.append(block(Xb,344,canvas))
        nb=randint(1,4)
        for b in range (0,nb):
            question=randint(0,4)
            Xb=Xb+30
            if question==2:
                blockq0_list.append(blockq(Xb,344,canvas))
            else:
                block_list.append(block(Xb,344, canvas))
    for c in range (0,5):
        Xbq=random.choice(block_list)
        blockq1_list.append(blockq(Xbq.x,229, canvas))


def dirta(canvas):
    global Xb_list,Xd_list,dp,dirt
    for a in range (0,7):
        Xd=randint(6,80)
        Xd=Xd*30
        while (Xd in Xd_list) or (Xd-30 in Xd_list) or (Xd+30 in Xd_list) or (Xd-60 in Xd_list)or (Xd+60 in Xd_list):
            Xd=randint(5,80)
            Xd=Xd*30
        Xd_list.append(Xd)
        Xd_list.append(Xd-30)
    for b in range (0,2820,30):
        if b in Xd_list:
            pass
        else:
            dp.append(canvas.create_image(b,485,image=dirt))
            dp.append(canvas.create_image(b,455,image=dirt))
            


def mapa(master,canvas):
    global flag_image,Xd_list,dp, block_list,blockq0_list,blockq1_list,cp,c1_list,c2_list
    Xd_list=[]#no dirt position
    dp=[]#dirt picture
    block_list=[]#list for the position of the block
    blockq1_list=[]
    blockq0_list=[]#list for the position of the question block
    c1_list=[]
    c2_list=[]
    cp=[]  
    creat_image()
    flag=canvas.create_image(2670,415,image=flag_image)
    clouda(canvas)
    blocka(canvas)
    for char in block_list:
        char.draw()
    for char in blockq1_list:
        char.draw()
    for char in blockq0_list:
        char.draw()
    dirta(canvas)
    master.update()
    return Xd_list,block_list,blockq0_list,blockq1_list
    


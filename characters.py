#this file is for characters images

from tkinter import *
import tkinter as tk

def create_image():
    global walk,shoot,ghost,goblin,jump
    
    
    walk=[]
    for n in range (1,9):
        walk.append(PhotoImage(file = "./character/walk"+str(n)+".gif"))
        
   
    shoot=[]
    shoot.append(PhotoImage(file = "./character/shootleft.gif"))
    shoot.append(PhotoImage(file = "./character/shootright.gif"))
    
    ghost=[]
    ghost.append(PhotoImage(file = "./enemy/ghost1.gif"))
    ghost.append(PhotoImage(file = "./enemy/ghost2.gif"))

    goblin=[]
    #11 for each side
    for n in range (0,22):
        goblin.append(PhotoImage(file = "./enemy/goblin"+str(n)+".png"))

    jump=PhotoImage(file = "./character/jump.gif")
    return walk,0,0,shoot,ghost,goblin,jump
    
    

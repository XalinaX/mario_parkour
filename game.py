import tkinter as tk
from tkinter import *
from random import randint
import time
from characters import *
from create_map import *
import threading
from playsound import playsound
from question import*
import winsound


# class for pikachu
#this can jump draw and collidewith enemy
class player(object):
    def __init__(self,x,y,canvas):
        self.isjump=False #determine if pikachu is jump
        self.char=canvas.create_line(0,0,0,0)
        self.left=False#move to left
        self.right=False#move to right
        self.walkCount=0#number of the character image
        self.jumpCount=7
        self.x=x
        self.y=y
        self.standing=True
        self.hitbox=(self.x-18,self.y-19,self.x+17,self.y+14)
        self.character_image=create_image()
        self.Xm=-5#position of canvas
        self.level=0
        self.falling=False
        self.falling_level1=False
        self.falling_level2=False
        self.jump_direction=1
        self.life=3
        
    def draw(self,master,canvas):
        if self.walkCount>3:
            self.walkCount=0
        canvas.delete(self.char)
        if not chu.falling:#if pikachu is falling, don not move it
            if not self.standing:
                if self.left:
                    self.char=canvas.create_image(self.x,self.y,image=self.character_image[0][self.walkCount+4])
                    self.walkCount+=1
                    if self.Xm<-5:
                        if self.x+self.Xm<550:
                            self.Xm+=15
                            canvas.place(x=self.Xm,y=0)
                elif self.right:
                    self.char=canvas.create_image(self.x,self.y,image=self.character_image[0][self.walkCount])
                    self.walkCount+=1
                    if self.Xm>-2000:
                        if self.x+self.Xm>150:
                            self.Xm-=15
                            canvas.place(x=self.Xm,y=0)
            else:
                if self.left:
                    self.char=canvas.create_image(self.x,self.y,image=self.character_image[0][4])
                else:
                    self.char=canvas.create_image(self.x,self.y,image=self.character_image[0][0])
        else:
            self.char=canvas.create_image(self.x,self.y,image=self.character_image[6])
            for a in range (0,10):
                canvas.move(self.char,0,10)
                master.update()
                time.sleep(0.05)
            #tells player how much score and lif they lose
            text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffa500",font="Verdana 24 bold",text="-10")
            text1=game_canvas.create_text(-chu.Xm+150,80,fill="#ff0000",font="Verdana 24 bold",text="-1")
            master.update()
            time.sleep(0.4)
            game_canvas.delete(text)
            game_canvas.delete(text1)
            self.falling=False
            self.x+=45
            self.char=canvas.create_image(self.x,425,image=self.character_image[0][0])
        master.update()
    def hit(self):#hit by enemy
        self.walkCount = 0
    def collide_with_wall_under(self):
        global map_position
        if self.level==0:
            if self.isjump:
                for grid in map_position[1]:
                    if self.y==376:
                        if (self.hitbox[0] < grid.x+14 and self.hitbox[0] > grid.x-14) or (self.hitbox[2] < grid.x+14 and self.hitbox[2] > grid.x-14) or self.x==grid.x:
                            self.jumpCount=-7
                            self.jump_direction=-1
    def collide_with_question_block(self):
        global map_position
        if self.isjump:
            if self.level==0:
                for grid in map_position[2]:
                    if self.y==376:
                        if self.x==grid.x-15 or self.x==grid.x+15 or self.x==grid.x:
                            self.jumpCount=-7
                            self.jump_direction=-1
                            return True,grid
            if self.level==1:
                for grid in map_position[3]:
                    if self.y==264:
                        if self.x==grid.x-15 or self.x==grid.x+15 or self.x==grid.x:
                            self.jumpCount=-7
                            self.jump_direction=-1
                            return True,grid
            
        return False,0
    
    def collide_with_wall_up(self):#jump up to the wall
        global map_position
        if self.level==0:
            for grid in map_position[1]:
                if self.hitbox[3]<grid.y-15:
                    if (self.hitbox[0] < grid.x+14 and self.hitbox[0] > grid.x-14) or (self.hitbox[2] < grid.x+14 and self.hitbox[2] > grid.x-14):
                        self.level=1
                        self.jumpCount=7
                        self.y=313
                        self.isjump=False
                        return True
            for grid in map_position[2]:
                if self.hitbox[3]<grid.y-15:
                    if (self.hitbox[0] < grid.x+15 and self.hitbox[0] > grid.x-15) or (self.hitbox[2] < grid.x+15 and self.hitbox[2] > grid.x-15):
                        self.level=1
                        self.jumpCount=7
                        self.y=313
                        self.isjump=False
                        return True
        elif self.level==1:
            for grid in map_position[3]:
                if self.hitbox[3]<grid.y-15:
                    if (self.hitbox[0] < grid.x+15 and self.hitbox[0] > grid.x-15) or (self.hitbox[2] < grid.x+15 and self.hitbox[2] > grid.x-15):
                        self.level=2
                        self.jumpCount=7
                        self.y=198
                        self.isjump=False
                        return True
        return False
    
    def fall_from_level1_to_0(self):#whenit leave the wall fall down to next level
        global map_position
        if self.level==1:
            for grid in map_position[1]:
                if (self.x == grid.x) or (self.x+15 == grid.x) or (self.x-15== grid.x):
                        return True
            for grid in map_position[2]:
                if (self.x == grid.x) or (self.x+15 == grid.x) or (self.x-15== grid.x):
                        return True
            if  (self.isjump):
                return True
            return False
    def fall_from_level2_to_1(self):
        global map_position
        if self.level==2:
            for grid in map_position[3]:
                if (self.x == grid.x) or (chu.x+15 == grid.x) or (chu.x-15== grid.x):
                        return True          
            if  (self.isjump):
                return True
            return False        

#class for bullet      
class projectile(object):
    def __init__(self,canvas,x,y,facing,start,end):
        self.x=x
        self.y=y
        self.facing=facing
        self.vel=15*facing
        self.picleft=chu.character_image[3][0]
        self.picright=chu.character_image[3][1]
        self.start=start
        self.end=end
        self.shoot=canvas.create_line(0,1,0,1)
        self.vel=20
        
    def draw(self,master,canvas):
        canvas.delete(self.shoot)
        if self.facing==-1:
            self.shoot=canvas.create_image(self.x,self.y,image=self.picleft)
        elif self.facing==1:
            self.shoot=canvas.create_image(self.x,self.y,image=self.picright)
        master.update()

#goblin, which has lots of pictures
class enemy1(object):
    def __init__(self,x,y,canvas,end):
        self.x=x
        self.y=y
        self.walkCount=0
        self.health=2
        self.hitbox=(self.x-13,self.y-26,self.x+13,self.y+26)
        self.visible=True
        self.char=canvas.create_line(0,2,0,2)
        self.pic=chu.character_image[5]
        self.end=end
        self.path=[self.x,self.end]
        self.vel=2
        
    def draw(self,master,canvas):
        self.move()
        canvas.delete(self.char)
        if self.visible:
            if self.walkCount>10:
                self.walkCount=0
            if self.vel>0:
                self.char=canvas.create_image(self.x,self.y,image=self.pic[self.walkCount])
                self.walkCount+=1
            else:
                self.char=canvas.create_image(self.x,self.y,image=self.pic[self.walkCount+11])
                self.walkCount+=1
            self.hitbox=(self.x-13,self.y-26,self.x+13,self.y+26)
    def move(self):
        if self.vel > 0:
            if self.x + self.vel > self.path[1]:
                self.x -= self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel < self.path[0]:
                self.x -= self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self,h):
        if self.health > 0:
            self.health -= h
        else:
            self.visible = False
        if h==3:
            self.visible = False

#ghost, only one picture
class enemy2(object):
    def __init__(self,x,y,canvas,end):
        self.x=x
        self.y=y
        self.health=2
        self.hitbox=(self.x-13,self.y-10,self.x+13,self.y+10)
        self.visible=True
        self.char=canvas.create_line(2,0,2,0)
        self.pic=chu.character_image[4]
        self.end=end
        self.path=[self.x,self.end]
        self.vel=2
        
    def draw(self,master,canvas):
        self.move()
        canvas.delete(self.char)
        if self.visible:
            if self.vel>0:
                self.char=canvas.create_image(self.x,self.y,image=self.pic[0])
            else:
                self.char=canvas.create_image(self.x,self.y,image=self.pic[1])
            self.hitbox=(self.x-13,self.y-10,self.x+13,self.y+10)
    def move(self):
        if self.vel > 0:
            if self.x + self.vel > self.path[1]:
                self.x -= self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel < self.path[0]:
                self.x -= self.vel
            else:
                self.vel = self.vel * -1
    def hit(self,h):
        if self.health > 0:
            self.health -= h
        else:
            self.visible = False
        if h==3:
            self.visible = False

def redrawGameWindow():#redraw the window, I try to draw every thing in one time,because it is faster for program
    global chu,bullets,goblin,ghost,score,score_text,life_text,cactus_list,game_canvas,name_text
    
    chu.hitbox=(chu.x-18,chu.y-19,chu.x+17,chu.y+14)
    game_canvas.delete(name_text)
    game_canvas.delete(score_text)
    game_canvas.delete(life_text)
    score_text=game_canvas.create_text(-chu.Xm+75,50,fill="#8b4513",font=(None,20),text=("score:",str(score)))
    life_text=game_canvas.create_text(-chu.Xm+65,80,fill="#8b4513",font=(None,20),text=("life:",str(chu.life)))
    name_text=game_canvas.create_text(-chu.Xm+650,50,fill="blue",font=(None,18),text=name)
    game_canvas.update()
    if not (chu.collide_with_wall_up()):
        chu.draw(win,game_canvas)
    for goblinc in goblin:
        goblinc.draw(win,game_canvas)
    for ghostc in ghost:
        ghostc.draw(win,game_canvas)
    for bullet in bullets:
        bullet.draw(win,game_canvas)

#main part of the game
        #check key input
        #check collition
def main_game():
    global B2,exit_button,b_continue,chu,bullets,runc,goblin,ghost,score,score_text,map_position,life_text,cactus_list,game_canvas,name,name_text
    #creat the canvas for game
    game_canvas=tk.Canvas(win.master,width=2800,height=500,bg="#00bfff")
    game_canvas.pack()
    game_canvas.place(x=-5,y=0)

    #redraw the button, otherwise it won't appear, it will be under the canvas
    B2.place_forget()
    b_continue.place_forget()
    exit_button.place_forget()
    mu.B3.place_forget()
    exit_button=Button(win.master,command=exit_game,text="EXIT",activebackground="gray",fg="#daa520")
    exit_button.pack()
    exit_button.place(x=660,y=5)
    b_continue=Button(win.master,command=game_over,text="GIVE UP",font="Verdana 11",activebackground="yellow",fg="#b8860b")
    b_continue.pack()
    b_continue.place(x=610,y=460)
    B2=Button(win.master,command=rule,text="?",activebackground="yellow",font=(None,18))
    B2.pack()
    B2.place(x=60,y=460,width=30,height=30)
    mu.B3=Button(win.master,command=mu.sound_off,image=mu.photo_on,activebackground="yellow")
    mu.B3.pack()
    mu.B3.place(x=20,y=460,width=30,height=30)
    
    #map generate
    map_position=None
    map_position=mapa(win,game_canvas)
    #pikachu
    chu=None
    chu=player(60,425,game_canvas)
    #display user name
    name_text=game_canvas.create_text(-chu.Xm+650,50,fill="blue",font=(None,18),text=name)
    #score
    score=0
    score_text=game_canvas.create_text(-chu.Xm+75,50,fill="#8b4513",font=(None,20),text=("score:",str(score)))
    #life
    life_text=game_canvas.create_text(-chu.Xm+65,80,fill="#8b4513",font=(None,20),text=("life:",str(chu.life)))
    
    runc=True
    bullets=[]
    shootloop=0
    
    ghost=[]
    ghost.append(enemy2(2000,430,game_canvas,1600))
    ghost.append(enemy2(950,430,game_canvas,650))
    ghost.append(enemy2(1200,315,game_canvas,500))
    ghost.append(enemy2(2400,315,game_canvas,1800))
    ghost.append(enemy2(1700,200,game_canvas,1200))
    
    goblin=[]
    goblin.append(enemy1(600,415,game_canvas,100))
    goblin.append(enemy1(2600,415,game_canvas,2100))
    goblin.append(enemy1(1500,415,game_canvas,1000))

    cactus_list=[]
    while runc:
        time.sleep(0.04)
        if chu.life>0 and chu.x != 2670: #the basic rule for game
            magic=chu.collide_with_question_block()#check collition with question block
            if magic[0]:
                ca=magic[1].collide()
                if ca==4 or ca==7:
                    question_d(win.master)
                    time.sleep(2)#stop pikachu moving for 2 seconds
                elif ca==3:
                    chu.life-=0.5
                    text1=game_canvas.create_text(-chu.Xm+150,80,fill="#ff0000",font="Verdana 24 bold",text="-0.5")
                    win.update()
                    time.sleep(0.4)
                    game_canvas.delete(text1)
                elif ca==6:
                    chu.life+=1
                    text1=game_canvas.create_text(-chu.Xm+150,80,fill="#ff0000",font="Verdana 24 bold",text="+1")
                    win.update()
                    time.sleep(0.4)
                    game_canvas.delete(text1)
                elif ca==5:
                    score+=10
                    text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffa500",font="Verdana 24 bold",text="+10")
                    win.update()
                    time.sleep(0.4)
                    game_canvas.delete(text)
                
            #check with enemies
            for goblina in goblin:
                if goblina.visible:
                    if chu.hitbox[1]>goblina.hitbox[1] and chu.hitbox[3]<goblina.hitbox[3]+3:
                        if (chu.hitbox[2]>goblina.hitbox[0] and chu.hitbox[2]<goblina.hitbox[2]) or (chu.hitbox[0]>goblina.hitbox[0] and chu.hitbox[0]<goblina.hitbox[2]):
                            playsound("./sound/hit.wav",block=False)
                            chu.hit()
                            goblina.hit(3)
                            text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffa500",font="Verdana 24 bold",text="-5")
                            text1=game_canvas.create_text(-chu.Xm+150,80,fill="#ff0000",font="Verdana 24 bold",text="-0.5")
                            win.update()
                            time.sleep(0.4)
                            game_canvas.delete(text)
                            game_canvas.delete(text1)
                            score-=5
                            chu.life-=0.5
                            
            for ghosta in ghost:
                if ghosta.visible:
                    if (chu.hitbox[1]>ghosta.hitbox[1]-30 and chu.hitbox[3]<ghosta.hitbox[3]+20):
                        if chu.hitbox[2]>ghosta.hitbox[0] and chu.hitbox[2]<ghosta.hitbox[2] or (chu.hitbox[0]>ghosta.hitbox[0] and chu.hitbox[0]<ghosta.hitbox[2]):
                            playsound("./sound/hit.wav",block=False)
                            chu.hit()
                            ghosta.hit(3)
                            text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffa500",font="Verdana 24 bold",text="-5")
                            text1=game_canvas.create_text(-chu.Xm+150,80,fill="#ff0000",font="Verdana 24 bold",text="-0.5")
                            win.update()
                            time.sleep(0.4)
                            game_canvas.delete(text)
                            game_canvas.delete(text1)
                            score-=5
                            chu.life-=0.5
            #make a little space between each bullet
            if shootloop>0:
                shootloop +=1
            if shootloop>3:
                shootloop=0
            # check bullets with enemies
            for bullet in bullets:
                for goblinb in goblin:
                    if goblinb.visible:
                        if bullet.y>goblinb.hitbox[1] and bullet.y<goblinb.hitbox[3]:
                            if bullet.x+20<goblinb.hitbox[2]+20 and bullet.x-20>goblinb.hitbox[0]-20:
                                playsound("./sound/hit.wav",block=False)
                                goblinb.hit(1)
                                text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffd700",font="Verdana 24 bold",text="+5")
                                win.update()
                                time.sleep(0.4)
                                game_canvas.delete(text)
                                score+=5
                                bullets.pop(bullets.index(bullet))
                                game_canvas.delete(bullet.shoot)
                for ghostb in ghost:
                    if ghostb.visible:
                        if bullet.y>ghostb.hitbox[1]-10 and bullet.y+10<ghostb.hitbox[3]:
                                if bullet.x<ghostb.hitbox[2]+20 and bullet.x>ghostb.hitbox[0]-20:
                                    playsound("./sound/hit.wav",block=False)
                                    ghostb.hit(1)
                                    text=game_canvas.create_text(-chu.Xm+170,50,fill="#ffd700",font="Verdana 24 bold",text="+5")
                                    win.update()
                                    time.sleep(0.4)
                                    game_canvas.delete(text)
                                    score+=5
                                    bullets.pop(bullets.index(bullet))
                                    game_canvas.delete(bullet.shoot)
                if bullet.x<bullet.end and bullet.x>bullet.start:
                    bullet.x+=bullet.vel*bullet.facing
                else:
                    bullets.pop(bullets.index(bullet))
                    game_canvas.delete(bullet.shoot)
            chu.collide_with_wall_under()       
            key=win.checkKey()#check which arrow key is pressed
            if key=="space" and shootloop==0:#shoot
                playsound("./sound/bullet.wav",block=False)
                if chu.left:
                    facing=-1
                else:
                    facing=1
                if len(bullets)<5:
                    bullets.append(projectile(game_canvas,chu.x,chu.y,facing,-chu.Xm,-chu.Xm+700))
                shootloop=1

            if key=="Left" and not (chu.falling_level1) and not (chu.falling_level2):
                if chu.x>25:
                    chu.x-=15
                chu.left=True
                chu.right=False
                chu.standing=False
            elif key=="Right" and not (chu.falling_level1) and not (chu.falling_level2):
                if chu.x<2680:
                    chu.x+=15
                chu.left=False
                chu.right=True
                chu.standing=False
            else:
                chu.standing=True
                chu.walkCount=0
            #jumping
            if not (chu.isjump) and not (chu.falling_level1) and not (chu.falling_level2):  #pikachu can only jump once it can't jump while it is in the sky 
                if key=="Up":
                    chu.isjump=True
                    chu.right=False
                    chu.left=False
                    chu.walkCount=0
                    playsound("./sound/jump.wav",block=False)
            elif chu.isjump:
                if chu.jumpCount>-7 or chu.jumpCount==-7:
                    chu.jump_direction=1
                    if chu.jumpCount<0:
                        chu.jump_direction=-1
                    chu.y -= (chu.jumpCount**2)*chu.jump_direction
                    chu.jumpCount -= 1
                else:
                    chu.isjump=False
                    if chu.level==0:
                        chu.y=425
                    elif chu.level==1:
                        chu.y=313
                    elif chu.level==2:
                        chu.y=198
                    chu.jumpCount=7
            #check for different position,falling
            if chu.level==0:
                if chu.x in map_position[0] or (chu.x+15 in map_position[0] and chu.x-15 in map_position[0]):
                    if not chu.isjump:
                        playsound("./sound/fall.wav",block=False)
                        chu.falling=True
                        score-=10
                        chu.life-=1
            elif chu.level==1:
                if not chu.fall_from_level1_to_0():
                    chu.falling_level1=True
                    if chu.y<409:
                       chu.y+=20
                    else:
                        chu.y=425
                        chu.falling_level1=False
                        chu.level=0
            elif chu.level==2:
                if not chu.fall_from_level2_to_1():
                    chu.falling_level2=True
                    if chu.y<289:
                       chu.y+=20
                    else:
                        chu.y=313
                        chu.falling_level2=False
                        chu.level=1
                    
            redrawGameWindow()#redraw the window
        else:
            runc=False
    game_canvas.delete(name_text)
    if chu.x==2670:
        game_win()
    else:
        game_over()
        

#backgriund music
class music(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.photo_on=PhotoImage(file="./else/speaker.gif")
        self.photo_off=PhotoImage(file="./else/no_speaker.gif")
        self.B3=Button(master,command=self.sound_off,image=self.photo_on,activebackground="yellow")
        self.B3.pack()
        self.B3.place(x=20,y=450,width=40,height=40)
        master.update()
    def sound_on(self):
        winsound.PlaySound("./sound/music.wav", winsound.SND_FILENAME|winsound.SND_LOOP|winsound.SND_ASYNC)
        self.B3.config(image=self.photo_on,command=self.sound_off)
    def sound_off(self):
        winsound.PlaySound(None, winsound.SND_FILENAME)
        self.B3.config(image=self.photo_off,command=self.sound_on)
    def run(self):
        winsound.PlaySound("./sound/music.wav", winsound.SND_FILENAME|winsound.SND_LOOP|winsound.SND_ASYNC)
#exit
def exit_game():
    winsound.PlaySound(None,winsound.SND_PURGE)
    win.close()
#introduction
def go_to_intro():
    global textaa,b_continue,intro
    textaa.setText("INTRODUCTION")
    logo.undraw()
    b_continue.config(command=go_to_username)
    introd="""  WELCOME EVERYBODY! This is a parkour game with Pikachu.
It is very easy to play, the only hard thing is solving some math
problems (If you get the chance). By click the continue button, you
will see the user name entry, where you need to creat a name for
yourself, the two buttons on the buttom left corner of the screen is
for control the sound and check the rule. If you want to leave the
game, click the exit button on the top right corner. After you click
the start button, GAME START. More details about the game will be
in the rule.
    >6< ENJOY YOUR TIME! >6<"""
    intro=Text(Point(350,240),introd)
    intro.setSize(16)
    intro.setOutline("#b8860b")
    intro.draw(win)
#enter name
def go_to_username():
    global textaa,b_continue,L1,E1,B2,intro,pic
    #lable username
    intro.undraw()
    textaa.undraw()
    pic=Image(Point(350,100),"./else/pikachus.png")
    pic.draw(win)
    L1 = Label(win.master, text="User Name",bg="yellow")
    L1.config(font=("system",20))
    L1.pack()
    L1.place(x=150,y=250)
    #entry for user name
    E1 = tk.Entry(win.master,width=20,font=(None,18),bd=5,bg="white")
    E1.pack()
    E1.place(x=300,y=250)
    #button for rule
    B2=Button(win.master,command=rule,text="?",activebackground="yellow",font=(None,20))
    B2.pack()
    B2.place(x=80,y=450,width=40,height=40)
    #button for enter the name
    b_continue.config(text="START",command=namea)
    b_continue.place(x=600,y=450)

#record user name
def namea():
    global textab,name
    name=E1.get()
    textab.undraw()
    #check if the user enter the name (can be a space)
    if name!="":
        start()
    else:
        textab=Text(Point(350,325),"Please enter your name( can be spaces )")
        textab.setOutline("orange")
        textab.draw(win)

def rule():
    global B2,T,win3
    win3=GraphWin("RULE",630,450)
    #the rule text
    rulea="""        RULE
--At the beginning of the game, your life will be 3 and score will be 0.
--When you collide with an enemy, you will lose 0.5 life and 5 scores. The
enemy will disappear immediately.
--If you hit an enemy by bullet, you will earn 5 scores. The enemy will
disappear after three nice shoot.
--If you falling from the ground (the space on the ground),
you will lose 1 life and 10 scores.
--When you hit the block with a "?", you might lose or earn life or score.
-If you find a cactus appear,do not worry,that is just a cute picture add
to the map.
-If you find a text box appear, you need to get the right answer as fast
as you can because the box will block part of the map. But, if your answer is
wrong, there will be a new question for you. The enemis still move!
--Each "? block" can only be hit once
--If your life become 0 or less, GAME IS OVER.
--If you run to the end of the map, you WIN the game.
        CONTROL
--use "arrow keys"(<--,-->) to control the direction, "up" means jump
--use "space" to shoot
    """
    T = tk.Text(win3.master, height=20,width=56,bg="#fffaf0")
    T.pack()
    T.place(x=5,y=5)
    T.insert(END, rulea)
    T.config(font=(None,14))
    B2.config(command=rule_off)
#turn off rule window
def rule_off():
    global B2,win3
    win3.close()
    B2.config(command=rule)
#life<0 or give up
def game_over():
    global B2,b_continue,game_canvas,runc,tetf,picf,score,recf
    runc=False
    playsound("./sound/over.wav",block=False)
    time.sleep(0.7)
    game_canvas.place_forget()
    B2.place_forget()
    b_continue.place_forget()
    b_continue=Button(win.master,command=start,text="NEW GAME",font="Verdana 16",activebackground="yellow",fg="#b8860b")
    b_continue.pack()
    b_continue.place(x=540,y=450)
    B2=Button(win.master,command=rule,text="?",activebackground="yellow",font=(None,20))
    B2.pack()
    B2.place(x=80,y=450,width=40,height=40)
    mu.B3.place(x=20,y=450,width=40,height=40)
    ttt="Game Over!\nYour score is: "+str(score)
    recf=Rectangle(Point(150,50),Point(550,500))
    recf.setOutline("white")
    recf.setFill("white")
    recf.draw(win)
    textf=Text(Point(350,100),ttt)
    textf.setSize(20)
    textf.setOutline("#b8860b")
    textf.draw(win)
    picf=Image(Point(350,300),"./else/over.png")
    picf.draw(win)
#arrived at destination    
def game_win():
    global B2,b_continue,game_canvas,runc,textf,picf,score,ttt,recf
    runc=False
    playsound("./sound/win.wav",block=False)
    time.sleep(0.7)
    game_canvas.place_forget()
    B2.place_forget()
    b_continue.place_forget()
    b_continue=Button(win.master,command=start,text="NEW GAME",font="Verdana 16",activebackground="yellow",fg="#b8860b")
    b_continue.pack()
    b_continue.place(x=540,y=450)
    B2=Button(win.master,command=rule,text="?",activebackground="yellow",font=(None,20))
    B2.pack()
    B2.place(x=80,y=450,width=40,height=40)
    mu.B3.place(x=20,y=450,width=40,height=40)
    recf=Rectangle(Point(150,50),Point(550,500))
    recf.setOutline("white")
    recf.setFill("white")
    recf.draw(win)
    ttt="Congratulation!\nYour score is: "+str(score)
    textf=Text(Point(350,100),ttt)
    textf.setSize(20)
    textf.setOutline("#b8860b")
    textf.draw(win)
    picf=Image(Point(350,300),"./else/win.png")
    picf.draw(win)
       
def start():
    global L1,E1,pic,runc,textf,picf
    runc=False
    try:
        textf.undraw()
        picf.undraw()
        recf.undraw()
    except NameError:
        pass
    pic.undraw()
    E1.place_forget()
    L1.place_forget()
    background.undraw()
    main_game()

#first screen    
from graphics import *
win=GraphWin("PIKACHU PARKOUR",700,500)
mu=music(win)
mu.start()
background=Image(Point(350,250),"./else/background.png")
background.draw(win)
exit_button=Button(win.master,command=exit_game,text="EXIT",activebackground="gray",fg="#daa520")
exit_button.pack()
exit_button.place(x=660,y=5)
b_continue=Button(win.master,command=go_to_intro,text="CONTINUE",font="Verdana 16",activebackground="yellow",fg="#b8860b")
b_continue.pack()
b_continue.place(x=540,y=450)
textab=Text(Point(350,300),"")
textab.draw(win)
textaa=Text(Point(350,80),"^--^Pikachu^--^\nby Alina Wu")#display welcome when user enter the game
textaa.setSize(28)
textaa.setOutline(color_rgb(100,149,237))
textaa.draw(win)
logo=Image(Point(350,250),"./else/logo.png")
logo.draw(win)
win.mainloop()
    
            

          
        
    




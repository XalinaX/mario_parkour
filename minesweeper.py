#minesweeper game
from random import randint
from tkinter import*
import tkinter as tk
import threading
import time
from playsound import playsound
import winsound

def creat_image():#create all the image
    global boom1,boom2,flagpic,pikachu,pikachu2,boom3
    boom1=tk.PhotoImage(file="./minesweeper/boom1.gif")  #red boom picture
    boom2=tk.PhotoImage(file="./minesweeper/boom2.gif")  #transparent boom
    flagpic=tk.PhotoImage(file="./minesweeper/flag.gif") #flag image
    pikachu=tk.PhotoImage(file="./minesweeper/pikachu.gif")   #pikachu image
    pikachu2=tk.PhotoImage(file="./minesweeper/pikachu2.gif")
    boom3=tk.PhotoImage(file="./minesweeper/boom3.gif")

def creat_table():#create a table for all the numbers
    global i,boo,row,column
    i=[]
    for a in range(0,row):
        i.append([])
        for b in range(0,column):
            i[a].append(0)
    while boo < boom:#creat booms
        r1=randint(0,row-1)#choose a row
        r2=randint(0,column-1)#choose a column
        if i[r1][r2]!=9:
            i[r1][r2]=9
            boo=boo+1
    #put number in to the table
    for c in range(0,row):
        for d in range(0,column):
            if i[c][d]==9:
                up_left(c,d)
                up(c,d)
                up_right(c,d)
                left(c,d)
                right(c,d)
                down_left(c,d)
                down(c,d)
                down_right(c,d)

def config_button(c,d):
    global grid
    grid[c][d].config(command=lambda:gr_id(c,d))

def creat_button():#table button
    global grid,a,b,pikachu,width,smile,row,column
    y=30
    grid=[]
    for c in range(0,row):
        y=y+20
        grid.append([])
        x=10
        for d in range(0,column):
            grid[c].append(Button(win,relief=RAISED,bg="#ffd700",activebackground="#daa520"))
            config_button(c,d)
            grid[c][d].pack()
            grid[c][d].place(x=x,y=y,width=20,height=20)
            x=x+20
    for a in range(0,row):
        for b in range(0,column):
            flag_bind(a, b)
    smile=Button(win,image=pikachu,command=restart,bg="#b8860b",bd=4)#smile button is for restart
    smile.pack()
    smile.place(x=80,y=10,width=40,height=40)
            
def up_left(x,y):#x=row, y=column
    if x>0 and y>0:
        if i[x-1][y-1]!=9:
            i[x-1][y-1]=i[x-1][y-1]+1           
def up(x,y):
    if x>0:
        if i[x-1][y]!=9:
            i[x-1][y]=i[x-1][y]+1
def up_right(x,y):
    if x>0 and y<column-1:
        if i[x-1][y+1]!=9:
            i[x-1][y+1]=i[x-1][y+1]+1
def left(x,y):
    if y>0:
        if i[x][y-1]!=9:
            i[x][y-1]=i[x][y-1]+1
def right(x,y):
    if y<column-1:
        if i[x][y+1]!=9:
            i[x][y+1]=i[x][y+1]+1
def down_left(x,y):
    if x<row-1 and y>0:
        if i[x+1][y-1]!=9:
            i[x+1][y-1]=i[x+1][y-1]+1
def down(x,y):
    if x<row-1:
        if i[x+1][y]!=9:
            i[x+1][y]=i[x+1][y]+1
def down_right(x,y):
    if x<row-1 and y<column-1:
        if i[x+1][y+1]!=9:
            i[x+1][y+1]=i[x+1][y+1]+1
     
def gr_id(c,d):#for grid
    global grid,i,boom1,boom2,win,row,column
    if i[c][d]==9:
        playsound("./minesweeper/boom.wav",block=False)
        grid[c][d].config(image=boom1,bd=0.5,bg="red")
        win.update()
        for a in range(0,row):
            for b in range(0,column): 
                gamet.game=False
                if i[a][b]==9 and (a!=c or d!=b):
                    if grid[a][b]["state"]==DISABLED:
                        grid[a][b].config(image=boom3,bd=0.5,bg="#fafad2")
                    else:
                        playsound("./minesweeper/boom.wav",block=False)
                        grid[a][b].config(image=boom2,bd=0.5,bg="#fafad2")
                    win.update()
                grid[a][b].config(state=DISABLED)
        
        for a in range(0,row):
            for b in range(0,column):
                grid[a][b].forget()
                grid[a][b].place_forget()
        time.sleep(0.5)
        gamet.text.delete(1.0,END)
        gamet.text.insert(END, "GAME")
        timert.text.delete(1.0,END)
        timert.text.insert(END," OVER")
        time.sleep(0.5)
        game_lose(0)
    elif i[c][d]==0:
        grid[c][d].config(state=DISABLED,bd=0.5,bg="#daa520")
        i[c][d]="f"
        table_open(c,d)
    else:
        grid[c][d].config(state=DISABLED,text=i[c][d],bd=0.5,bg="#daa520",font=("bold",15))
        i[c][d]="f"

def table_open(x,y):#if the grid is empty, open all the grid around it
    global i
    if x>0 and y>0:        
        if i[x-1][y-1]!=9 and i[x-1][y-1]!="f":
            if grid[x-1][y-1]["state"]!=DISABLED:
                gr_id(x-1,y-1)
    if x>0:
        if i[x-1][y]!=9 and i[x-1][y]!="f":
            if grid[x-1][y]["state"]!=DISABLED:
                gr_id(x-1,y)
    if x>0 and y<column-1 :
        if i[x-1][y+1]!=9 and i[x-1][y+1]!="f":
            if grid[x-1][y+1]["state"]!=DISABLED:
                gr_id(x-1,y+1)
    if y>0:
        if i[x][y-1]!=9 and i[x][y-1]!="f":
            if grid[x][y-1]["state"]!=DISABLED:
                gr_id(x,y-1)
    if y<column-1:
        if i[x][y+1]!=9 and i[x][y+1]!="f":
            if grid[x][y+1]["state"]!=DISABLED:
                gr_id(x,y+1)
    if x<row-1 and y>0:
        if i[x+1][y-1]!=9 and i[x+1][y-1]!="f":
            if grid[x+1][y-1]["state"]!=DISABLED:
                gr_id(x+1,y-1)
    if x<row-1:
        if i[x+1][y]!=9 and i[x+1][y]!="f":
            if grid[x+1][y]["state"]!=DISABLED:
                gr_id(x+1,y)
    if x<row-1 and y<column-1:
        if i[x+1][y+1]!=9 and i[x+1][y+1]!="f":
            if grid[x+1][y+1]["state"]!=DISABLED:
                gr_id(x+1,y+1)

#game ovre
def game_lose(ind):
    global losers,label_win
    if ind <16:
        label_win.place_forget()
        loser = losers[ind]
        ind += 1
        label_win.configure(image=loser)
        label_win.pack()
        label_win.place(x=20,y=60,width=160,height=160)
        win.after(120, game_lose, ind)



#keep check for the consequence of game
class game_check(threading.Thread):
    def __init__(self):
        global win,boom
        threading.Thread.__init__(self)
        self.runn=True
        self.game=True
        self.mine_left=boom
        self.text=tk.Text(win.master, height=1,width=5,bg="black",fg="white",font="Verdana 15")
        self.text.pack()
        self.text.place(x=10,y=15)
        win.update()
    def draw(self):
        self.text.delete(1.0,END)
        if self.mine_left>9:
            self.text.insert(END,"  "+str(self.mine_left))
        else:
            self.text.insert(END,"    "+str(self.mine_left))
    def wing(self):
        global grid,row,column
        for a in range(0,row):
            for b in range(0,column):
                try:
                    if i[a][b]!=9:
                        if grid[a][b]["state"]!=DISABLED:
                            return False
                except IndexError:
                    pass
        if self.game!=False:
            return True
    #win!!
    def game_win(self,ind):
        global winners,label_win
        if ind <5:
            label_win.place_forget()
            winner = winners[ind]
            ind += 1
            label_win.configure(image=winner)
            label_win.pack()
            label_win.place(x=20,y=60,width=160,height=160)
            win.after(120, self.game_win, ind)

    def run(self):
        global smile,win,row,column
        self.draw()
        while self.runn:
            if not (self.game):
                smile.config(image=pikachu2)
            if self.wing():
                self.game=False
                for a in range(0,row):
                    for b in range(0,column):
                        if i[a][b]==9:
                            grid[a][b].config(state=DISABLED)
                        grid[a][b].place_forget()
                self.text.delete(1.0,END)
                self.text.insert(END, "GOOD")
                timert.text.delete(1.0,END)
                timert.text.insert(END," JOB")
                time.sleep(0.5)
                self.game_win(0)
                        
                
            
class timer(threading.Thread):
    def __init__(self):
        global win
        threading.Thread.__init__(self)
        self.time=0
        self.runn=True
        self.text=tk.Text(win.master, height=1,width=5,bg="black",fg="white",font="Verdana 15")
        self.text.pack()
        self.text.place(x=120,y=15)
        self.text.insert(END, "00:00")
        win.update()
        self.second=0
        self.minute=0
    def run(self):
        while self.runn:
            time.sleep(1)
            if gamet.game:
                self.time+=1
                self.second=int(self.time%60)
                self.minute=int((self.time-self.second)/60)
                self.text.delete(1.0,END)
                if self.minute<10 and self.second<10:
                    self.text.insert(END, ("0"+str(self.minute)+":0"+str(self.second)))
                elif self.minute<10:
                    self.text.insert(END, ("0"+str(self.minute)+":"+str(self.second)))
                elif self.second<10:
                    self.text.insert(END, (str(self.minute)+":0"+str(self.second)))
                else:
                    self.text.insert(END, (str(self.minute)+":"+str(self.second)))
            

def restart():#restart the game
    global grid,boo,gamet,timert,row,column,label_win
    label_win.place_forget()
    boo=0
    for a in range(0,row):
            for b in range(0,column):
                grid[a][b].place_forget()
    creat_table()
    creat_button()
    gamet.game=True
    timert.time=0
    timert.second=0
    timert.minute=0

def main(aaa,bbb,mine):#arrange all the functions
    global win,row,column,boo,boom,grid,width,gamet,timert,winners,label_win,losers,start
    boom=mine
    boo=0
    row=aaa
    column=bbb
    creat_table()
    width=row*20+20
    height=column*20+60
    win.after(1,creat_image)
    win.after(1,creat_button)
    if start>0:
        label_win.place_forget()
        for a in range(0,30):
            for b in range(0,30):
                try:
                    grid[a][b].config(state=DISABLED)
                    grid[a][b].place_forget()
                except IndexError:
                    pass
    elif start==0:
        winners = [PhotoImage(file='./minesweeper/winner.gif',format = 'gif -index %i' %(i)) for i in range(5)]
        losers=[PhotoImage(file='./minesweeper/loser.gif',format = 'gif -index %i' %(i)) for i in range(16)]
        label_win = Label(win)
        label_win.pack()
        label_win.place(x=0,y=0)
        timert=timer()
        gamet=game_check()
        gamet.start()
        timert.start()
    start+=1
    gamet.game=True
    gamet.mine_left=boom
    gamet.draw()

   

#when right click happened, a flag will appear   
def flag_bind(a, b):
    grid[a][b].bind("<Button-3>",lambda x: flag(a,b))

def flag(a,b):
    global grid,flagpic,gamet
    grid[a][b].config(image=flagpic,bg="white",state=DISABLED)
    grid[a][b].bind("<Button-3>",lambda x: flag_off(a,b))
    gamet.mine_left-=1
    gamet.draw()
    
def flag_off(a,b):
    global grid,gamet
    grid[a][b].config(image="",bg="#ffd700",state=NORMAL)
    grid[a][b].bind("<Button-3>",lambda x: flag(a,b))
    gamet.mine_left+=1
    gamet.draw()
    
#creat a main window
from graphics import*
win=GraphWin("HANGMAN",800,600)
win.setBackground("white")


#HOME PAGE
#user name
def namea():
    global textab,name
    name=E1.get()
    textab.undraw()
    #check if the user enter the name (can be a space)
    if name!="":
        menu()
    else:
        textab=Text(Point(400,425),"Please enter your name( can be spaces )")
        textab.setOutline("orange")
        textab.draw(win)

#the rule window
r=1
def rule():
    global B2,T,win3
    win3=GraphWin("RULE",570,300)
    #the rule text
    rulea="""       RULE
  Left-click an empty square to reveal it.
  Right-click  an empty square to flag it (make the button disabled).
  Pilachu Button is for restart
  The number on the grid indicates the amount of booms around.
  Clear the board without detonating any mines as fast as you can!
        MODE
  Easy: 9x9 grid, 10 mines
  Medium: 15x13 grid, 40 mines
  Hard: 30x16 grid, 99mines
        WARNING: if you lose game, do NOT change mode before all 
    the booms appears on the button."""
    T = tk.Text(win3.master, height=12,width=60,bg="#fffaf0")
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

#for user to choose the level
scores=0
def menu():
    global text,Be,Bh,Bm,user,B5,name,start
    textab.undraw()
    textaa.undraw()
    E1.place_forget()
    B1.place_forget()
    L1.place_forget()
    text=Text(Point(400,550),"*_*  MINESWEEPER  *_*")
    text.setOutline(color_rgb(200,149,237))
    text.setSize(20)
    text.draw(win)
    #button for 3 levels
    Be=Button(win.master,command=Beg,text="EASY",fg="#9370bd",font=(None,14),activebackground="#d3d3d3")
    Be.pack()
    Be.place(x=700,y=370,width=80,height=40)
    Bm=Button(win.master,command=Bmg,text="MEDIUM",fg="#9370bd",font=(None,14),activebackground="#d3d3d3")
    Bm.pack()
    Bm.place(x=700,y=420,width=80,height=40)
    Bh=Button(win.master,command=Bhg,text="HARD",fg="#9370bd",font=(None,14),activebackground="#d3d3d3")
    Bh.pack()
    Bh.place(x=700,y=470,width=80,height=40)
    #display player on right corner of window
    user=Text(Point(730,40),name)
    user.setSize(25)
    user.setOutline("#4169e1")
    user.draw(win)
    #start the game
    start=0
    main(9,9,10)
    
def Beg():
    main(9,9,10)
def Bmg():
    main(13,15,40)
def Bhg():
    main(16,30,99)

#HOME,enter name
#lable for entry
from tkinter import  *
L1 = Label(win.master, text="User Name",bg="white")
L1.config(font=("system",20))
L1.pack()
L1.place(x=180,y=300)
#entry for user name
E1 = Entry(win.master,width=20,font=(None,18),bd=5,bg="white")
E1.pack()
E1.place(x=340,y=300)
#button for enter the user name
B1=Button(win.master,command=namea,text="START",activebackground="gray",fg="brown")
B1.config(font=(None,16))
B1.pack()
B1.place(x=655,y=520)
#button for rule
B2=Button(win.master,command=rule,text="?",activebackground="yellow",font=(None,20))
B2.pack()
B2.place(x=30,y=520,width=40,height=40)

#backgriund music
class music(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.photo_on=tk.PhotoImage(file="./minesweeper/speaker.gif")
        self.photo_off=tk.PhotoImage(file="./minesweeper/no_speaker.gif")
        self.B3=tk.Button(master,command=self.sound_off,image=self.photo_on,activebackground="yellow")
        self.B3.pack()
        self.B3.place(x=90,y=520,width=40,height=40)
    def sound_on(self):
        winsound.PlaySound("./minesweeper/music.wav", winsound.SND_FILENAME|winsound.SND_LOOP|winsound.SND_ASYNC)
        self.B3.config(image=self.photo_on,command=self.sound_off)
    def sound_off(self):
        winsound.PlaySound(None, winsound.SND_FILENAME)
        self.B3.config(image=self.photo_off,command=self.sound_on)
    def run(self):
        winsound.PlaySound("./minesweeper/music.wav", winsound.SND_FILENAME|winsound.SND_LOOP|winsound.SND_ASYNC)
mu=music(win)
mu.start()
from graphics import *
textab=Text(Point(400,350),"")
textab.draw(win)
textaa=Text(Point(400,150),"^6^  MINESWEEPER  ^6^")#display welcome when user enter the game
textaa.setSize(30)
textaa.setOutline(color_rgb(200,149,237))
textaa.draw(win)


#EXIT game
#use the button to exit the game
def exit_game():
    global gamet, timert
    try:
        gamet.runn=False
        timert.runn=False
    except NameError:
        pass
    winsound.PlaySound(None,winsound.SND_PURGE)
    win.close()
exit_button=Button(win.master,command=exit_game,text="EXIT",activebackground="gray",fg="brown")
exit_button.pack()
exit_button.place(x=763,y=3)
win.mainloop()

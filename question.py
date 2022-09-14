from random import randint
import time
import tkinter as tk
from tkinter import *
from playsound import playsound
f = open("questions.txt","r+")
file = f.readlines()
line_list=[]
def select():
    global start,end,line_list,count,line
    line=randint (1,6)
    count=0
    while line in line_list:
        if count>10:
            break
        count+=1
        line=randint (1,6)
    line_list.append(line)
    for i in file:
        if i == (str(line)+"\n"):
            start=file.index(i)
        if i == (str(line+1)+"\n") or i=="END\n":
            end=file.index(i)
            break
    return file[start+1:end]

def right():
    global que_text,b1,b2,b3,masterr,runq
    playsound("./sound/hit.wav")
    b2.place_forget()
    b3.place_forget()
    que_text.place_forget()
    b1.config(state=DISABLED,text="Correct!",font="Verdana 22 bold",relief=GROOVE)
    b1.place(x=280,y=100,width=150,height=50)
    masterr.update()
    time.sleep(0.5)
    b1.place_forget()
    runq=False
    
def wrong():
    global que_text,b1,b2,b3,masterr
    playsound("./sound/question.wav")
    b2.place_forget()
    b3.place_forget()
    que_text.place_forget()
    b1.config(state=DISABLED,text="Wrong!",font="Verdana 22 bold",relief=GROOVE)
    b1.place(x=280,y=100,width=150,height=50)
    masterr.update()
    time.sleep(0.5)
    b1.place_forget()
    question_d(masterr)
    
    
def question_d(master):
    global start,end,que,q,an,que_text,masterr,t,b1,b2,b3,runq
    runq=True
    masterr=master
    q=select()
    que=""
    for i in q:
        if i!="A\n" and i!="B\n" and i!="C\n":
            que+="  "+i
        else:
            answer=i
    que_text=tk.Text(master,width=48,height=8)
    que_text.pack()
    que_text.place(x=80,y=185)
    que_text.insert(END, que)
    que_text.config(font=(None,14))
    t=[]
    for char in "ABC":
        if char != answer[0]:
            t.append(char)
    b1=Button(master,command=right,text=answer[0],bg="#ffd700",font="Verdana 16 bold",activebackground="#b8860b")
    b1.pack()
    b1.place(x=270,y=300,width=40,height=30)
    b2=Button(master,command=wrong,text=t[0],bg="#ffd700",font="Verdana 16 bold",activebackground="#b8860b")
    b2.pack()
    b2.place(x=370,y=300,width=40,height=30)
    b3=Button(master,command=wrong,text=t[1],bg="#ffd700",font="Verdana 16 bold",activebackground="#b8860b")
    b3.pack()
    b3.place(x=470,y=300,width=40,height=30)
    master.update()


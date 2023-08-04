from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


t = Tk()
t.title("Student manger")
t.resizable(0, 0)
w = 700
h = 600
x = (t.winfo_screenwidth() - w) / 2
y = (t.winfo_screenheight() - h) / 2
t.geometry("%dx%d+%d+%d" % (w, h, x, y))


def login():
    f2 = Frame(bg="black")
    f2.place(x=0, y=0, width=700, height=600)
    u3 = Label(f2, text="Name", font=("arial", 15, "underline"), bg="cyan", fg="black")
    u3.place(x=150, y=200, width=150, height=25)
    u4 = Label(f2, text="Password", font=("arial", 15, "underline"), bg="cyan", fg="black")
    u4.place(x=150, y=250, width=150, height=25)
    e1 = Entry(f2, font=("", 15), textvariable=p)
    e1.place(x=350, y=200, width=250, height=25)
    e2 = Entry(f2, font=("", 15), textvariable=q, show="*")
    e2.place(x=350, y=250, width=250, height=25)
    b1 = Button(f2, text="Login", font=("", 15), bg="gold", fg="black", activebackground="cyan",
                activeforeground="black", command=login1)
    b1.place(x=260, y=310, width="110", height="35")
    b2 = Button(text="Register", font=("", 15), bg="gold", fg="black", activebackground="cyan",
                activeforeground="black", command=regis)
    b2.place(x=560, y=540, width="110", height="35")


def regis():
    f1 = Frame(bg="black")
    f1.place(x=0, y=0, width=700, height=600)
    u3 = Label(f1, text="Name", font=("arial", 15, "underline"), bg="cyan", fg="black")
    u3.place(x=150, y=200, width=150, height=25)
    u4 = Label(f1, text="Email", font=("arial", 15, "underline"), bg="cyan", fg="black")
    u4.place(x=150, y=250, width=150, height=25)
    u5 = Label(f1, text="Password", font=("arial", 15, "underline"), bg="cyan", fg="black")
    u5.place(x=150, y=300, width=150, height=25)
    e1 = Entry(f1, font=("", 11), textvariable=a)
    e1.place(x=350, y=200, width=250, height=25)
    e2 = Entry(f1, font=("", 11), textvariable=b)
    e2.place(x=350, y=250, width=250, height=25)
    e3 = Entry(f1, font=("", 11), textvariable=c, show="*")
    e3.place(x=350, y=300, width=250, height=25)
    b1 = Button(text="Login", font=("", 15), bg="GOLD", fg="black", activebackground="CYAN", activeforeground="black",
                command=login)
    b1.place(x=580, y=540, width="90", height="35")
    b2 = Button(text="Register", font=("", 15), bg="gold", fg="black", activebackground="cyan",
                activeforeground="black", command=regis1)
    b2.place(x=250, y=360, width="150", height="35")


f0 = Frame(bg="lavender")
f0.place(x=0, y=0, width=700, height=600)
u2 = Label(text="Student management system", font=("arial", 15, "underline"), bg="yellow", fg="lightgreen")
u2.place(x=50, y=110, width=600, height=30)
b1 = Button(text="Login", font=("", 15), bg="black", fg="gold", activebackground="gold", activeforeground="black",
            command=login)
b1.place(x=180, y=160, width="90", height="35")
b2 = Button(text="Register", font=("", 15), bg="black", fg="gold", activebackground="gold", activeforeground="black",
            command=regis)
b2.place(x=410, y=160, width="100", height="35")
b3 = Button(text="Exit", bg="black", fg="gold", activebackground="gold", activeforeground="black", command=t.destroy)
b3.place(x=0, y=0, width=10, height=10)
t.mainloop()
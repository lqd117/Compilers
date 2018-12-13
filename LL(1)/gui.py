from tkinter import *
import tkinter.font as tkFont
from PIL import Image
from PIL import ImageTk
import data,algorithm

root = Tk()
root.title('应用程序窗口')        #窗口标题
root.resizable(False, False)    #固定窗口大小
windowWidth = 1300               #获得当前窗口宽
windowHeight = 900              #获得当前窗口高
screenWidth,screenHeight = root.maxsize()     #获得屏幕宽和高
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)
root.geometry(geometryParam)    #设置窗口大小及偏移坐标



defaultValue1 = StringVar()
defaultValue1.set("请在下方输入文法及待测表达式")
entry1 = Entry(root,width = 70,font =18,bd = 7,bg = "white",fg = "black",textvariable = defaultValue1,state = 'disabled')
entry1.place(x=0,y=0)

text1 = Text(root,width = 81)
text1.place(x=0,y=35)

text2 = Text(root,width = 95)
text2.place(x=600,y=35)

text3 = Text(root,width = 181,height = 36)
text3.place(x=0,y=400)

def go1():#输入文法及待测表达式
    text2.delete(1.0,END)
    text3.delete(1.0,END)
    data.clear()
    text1.update()
    a = text1.get('1.0',END)
    data.array = a.strip().split('\n')
    data.stringJudge = data.array[-1]
    data.array.pop()
    print(data.array)
    algorithm.work()

button1 = Button(root,text="确定",command = go1)
button1.place(x=0,y=355)

def go2():#改写文法
    text2.delete(1.0,END)
    text2.insert(INSERT,data.string)

button2 = Button(root,text="改写文法",command = go2)
button2.place(x=800,y=0)

def go3():#First集合
    text2.delete(1.0,END)
    text2.insert(INSERT,data.stringFirst)
    pass
button3 = Button(root,text="First集合",command = go3)
button3.place(x=870,y=0)

def go4():#Follow集合
    text2.delete(1.0, END)
    text2.insert(INSERT, data.stringFollow)

button4 = Button(root,text="Follow集合",command = go4)
button4.place(x=940,y=0)

def go5():#LL(1)分析表
    text2.delete(1.0, END)
    text2.insert(INSERT, data.stringTable)

button5 = Button(root,text="LL(1)分析表",command = go5)
button5.place(x=1025,y=0)

def go6():#分析过程
    text2.delete(1.0, END)
    if data.flagResult:
        text2.insert(INSERT, "分析成功")
    else:
        text2.insert(INSERT,"分析失败")
    text3.delete(1.0, END)
    text3.insert(INSERT, data.stringResult)

button6 = Button(root,text="分析过程",command = go6)
button6.place(x=1110,y=0)



root.mainloop()

'''
5
exp -> exp addop term | term
addop -> + | -
term -> term mulop factor | factor
mulop -> *
factor -> ( exp ) | number
( number + number - number ) * number

9
expr -> expr addop term
expr -> term
addop -> +
addop -> -
term -> term mulop factor
term -> factor
mulop -> *
factor -> ( expr )
factor -> number

5
E -> T E'
E' -> + T E' | ε
T -> F T'
T' -> * F T' | ε
F -> ( E ) | i

Expr -> Expr Addop Term | Term
Addop -> + | -
Term -> Term Mulop Factor | Factor
Mulop -> *
Factor -> ( Expr ) | number
number + number


A -> B a | A a | c
B -> B b | A b | d
d a

A -> a b | a c
a c

A -> a b c d | a b a c
B -> c d | c d a
a b a c

S -> ( S ) S | ε
( ) ( )
'''

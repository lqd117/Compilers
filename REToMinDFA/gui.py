from tkinter import *
import tkinter.font as tkFont
import tkinter
import tkinter.messagebox
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

label1 = Label(root,background = "white")
label1.grid(row = 3,rowspan = 50,columnspan = 200,sticky = W)

defaultValue1 = StringVar()
defaultValue1.set("请输入正则表达式")
entry1 = Entry(root,width = 55,font =17,bg = "white",fg = "black",textvariable = defaultValue1)
entry1.grid(row = 0,column = 0,columnspan = 60)

def go1():#表达式
    data.regularExpression = entry1.get()
    algorithm.work()
    data.flag = 1
button1 = Button(root,text="确定",command = go1)
button1.grid(row = 0,column = 60)

defaultValue2 = StringVar()
defaultValue2.set("请输入待测字符串")
entry2 = Entry(root,width = 55,font = 17,bg = "white",fg = "black",textvariable = defaultValue2)
entry2.grid(row = 1,column = 0,columnspan = 60)
def go2():#待测字符串
    data.string = entry2.get()
    algorithm.checkString()
    print(data.result)
    label3 = Label(root, background='white', text=data.result)
    label3.grid(row=1, column=70, sticky=W)

button2 = Button(root,text="确定",command = go2)
button2.grid(row = 1,column = 60)
label2 = Label(root,text = "测试结果：")
label2.grid(row = 1,column = 64)


def go3():#逆波兰表达式
    print("go3")
    ft = tkFont.Font(size = 17)
    label1 = Label(root,text=data.inversePolishexpression,font = ft,bg = 'white',width = 105,height = 35)
    label1.grid(row=3, rowspan=50, columnspan=200, sticky=W)

button3 = Button(root,text = "逆波兰表达式",command = go3)
button3.grid(row = 2,column = 0,columnspan = 6,sticky = W)


def go4():#NFA
    print("go4")
    label1 = Label(root, background="white")
    img = Image.open("NFA.gif")
    img = img.resize((1250, 800), Image.ANTIALIAS)
    img_gif = ImageTk.PhotoImage(img)
    label1.grid(row=3, rowspan=50, columnspan=200, sticky=W)
    label1.config(image=img_gif)
    label1.image = img_gif
button4 = Button(root,text = "NFA",command = go4)
button4.grid(row = 2,column = 6,columnspan = 3,sticky = W)


def go5():#DFA
    print("go5")
    label1 = Label(root, background="white")
    img = Image.open("DFA.gif")
    img = img.resize((1250, 800), Image.ANTIALIAS)
    img_gif = ImageTk.PhotoImage(img)
    label1.grid(row=3, rowspan=50, columnspan=200, sticky=W)
    label1.config(image=img_gif)
    label1.image = img_gif
button5 = Button(root,text = "DFA",command = go5)
button5.grid(row = 2,column = 9,columnspan = 3,sticky = W)


def go6():#最小化DFA
    print("go6")
    label1 = Label(root, background="white")
    img = Image.open("minDFA.gif")
    img = img.resize((1250, 800), Image.ANTIALIAS)
    img_gif = ImageTk.PhotoImage(img)
    label1.grid(row=3, rowspan=50, columnspan=200, sticky=W)
    label1.config(image=img_gif)
    label1.image = img_gif
button6 = Button(root,text = "最小化DFA",command = go6)
button6.grid(row = 2,column = 12,columnspan = 6,sticky = W)


def go7():#演示
    print("go7")
button7 = Button(root,text = "演示",command = go7)
button7.grid(row = 2,column = 18,columnspan = 3,sticky = W)

def go8():#表格
    print("go8")
button8 = Button(root,text = "表格",command = go8)
button8.grid(row = 2,column = 21,columnspan = 3,sticky = W)





root.mainloop()


from graphviz import Digraph
import time
from wand.image import Image


def checkLetter(var):
    if(var >= 'a' and var <= 'z'):
        return 1
    return 0

def check(var1,var2):
    flag1 = checkLetter(var1)
    flag2 = checkLetter(var2)
    if(flag1 == 1 and flag2 == 1): return 1
    elif(flag1 == 1 and flag2 == 0):
        if(var2 == '('):return 1
        else: return 0
    elif(flag1 == 0 and flag2 == 1):
        if(var1 == ')' or var1 == '*'): return 1
        else: return 0
    else:
        if(var1 == ')' and var2 == '('): return 1
        elif(var1 == '*' and var2 == '('): return 1
        else: return 0

def comparePriority(var1,var2):

    if(var1 == '*'): return 1
    elif(var1 == '·'):
        if(var2 == '*'): return 0
        else: return 1
    else:
        if(var2 == '|'): return 1
        else: return 0

class NFA:
    def __init__(self):
        self.ID = []
        self.startID = -1
        self.acceptID = -1
        self.side = {}

class DFA:
    def __init__(self):
        self.ID = []
        self.startID = -1
        self.acceptID = {}
        self.side = {}



def generateGraph(name,ID,startID,acceptID,side):
    dot = Digraph()
    for x in ID:
        flag = 0
        if(acceptID.get(x,0)): flag = 1
        if(flag):dot.node(str(x),str(x),shape = 'doublecircle',rankdir = 'LR')
        else: dot.node(str(x),str(x),shape = 'circle',rank = 'LR')
    for x in ID:
        for y in side[x]:
            temp = y[1]
            if(temp == ' '): temp = 'ε'
            dot.edge(str(x),str(y[0]),temp,rankdir = 'LR')
    dot.node("","",shape = 'none')
    dot.edge("",str(startID),' ')
    dot.graph_attr['rankdir'] = 'LR'
    print(dot.source)
    dot.render(filename = name)
    name1 = str(name) + ".pdf"
    name2 = str(name) + ".gif"
    with Image(filename=name1, resolution=300) as img:
        img.format = 'gif'
        img.save(filename=name2)
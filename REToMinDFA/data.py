import lib

flag = 0
regularExpression = "" #正则表达式

inversePolishexpression = "" #逆波兰表达式

NFA = lib.NFA()

queue = []

DFA = lib.DFA()

string = ""
result = "False"

minDFA = lib.DFA()
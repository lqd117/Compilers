
global array,string,stringFirst,stringFollow,flag,stringTable,stringJudge,flagResult,stringResult

array = [] #存输入的文法

string = "" #存修改过后的文法

stringFirst = "" #存要输出的First集合

stringFollow = "" #存要输出的Follow集合

flag = 0 #标记该文法是否符合LL(1)文法

stringTable = "" #存要输出的LL(1)分析表

stringJudge = "" #存待判断的表达式

flagResult = 0 #存最后分析结果

stringResult = "" #存要输出的分析过程

def clear():
    global array, string, stringFirst, stringFollow, flag, stringTable, stringJudge, flagResult, stringResult
    string,stringFirst,stringFollow,stringTable,stringJudge,stringResult = "","","","","",""
    flag,flagResult = 0,0
    array = []


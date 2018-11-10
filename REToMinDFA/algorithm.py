import lib
import data

def work():

    regularExpression = data.regularExpression

    #添加与操作符号
    lenRE = len(regularExpression)
    temp = "("
    for id in range(lenRE-1):
        temp += regularExpression[id]
        if(lib.check(regularExpression[id],regularExpression[id+1]) == 1): temp += '·'
    temp += regularExpression[lenRE - 1] + ")"
    regularExpression = temp
    stk = []
    inversePolishexpression = ""

    #求逆波兰表达式
    for x in regularExpression:
        if(lib.checkLetter(x) == 1):
            inversePolishexpression += x
            continue
        if(x == '('):
            stk.append(x)
            continue
        if(x == ')'):
            while(1):
                if(stk[-1] == '('):
                    stk.pop()
                    break
                inversePolishexpression += stk[-1]
                stk.pop()
            continue
        while(1):
            if(stk[-1] == '('):
                stk.append(x)
                break
            if(lib.comparePriority(stk[-1],x) == 1):
                inversePolishexpression += stk[-1]

                stk.pop()
            else:
                stk.append(x)
                break
    print("inversePolishexpression is %s" % (inversePolishexpression))
    data.inversePolishexpression = inversePolishexpression

    #求NFA
    id = 1
    stk = []
    for x in inversePolishexpression:
        if(lib.checkLetter(x) == 1):
            stk.append(lib.NFA())
            stk[-1].startID = id
            stk[-1].ID.append(id)
            id += 1
            stk[-1].acceptID = id
            stk[-1].ID.append(id)
            stk[-1].side[id-1] = [];stk[-1].side[id] = []
            stk[-1].side[id-1].append([id,x])
            id += 1
        elif(x == '·'):
            object2 = stk.pop();object1 = stk.pop()
            for x in object2.ID: object1.ID.append(x)
            for x in object2.side: object1.side[x] = object2.side[x]
            object1.side[id] = []
            object1.side[id].append([object1.startID, ' '])
            object1.side[object1.acceptID].append([object2.startID,' '])
            object1.startID = id;object1.ID.append(id)
            id += 1
            object1.side[id] = []
            object1.side[object2.acceptID].append([id,' '])
            object1.acceptID = id;object1.ID.append(id)
            id += 1
            stk.append(object1);del object2
        elif(x == '|'):
            object2 = stk.pop();object1 = stk.pop()
            for x in object2.ID: object1.ID.append(x)
            for x in object2.side: object1.side[x] = object2.side[x]
            object1.side[id] = []
            object1.side[id].append([object1.startID,' '])
            object1.side[id].append([object2.startID,' '])
            object1.startID = id;object1.ID.append(id)
            id += 1
            object1.side[id] = []
            object1.side[object1.acceptID].append([id,' '])
            object1.side[object2.acceptID].append([id,' '])
            object1.acceptID = id;object1.ID.append(id)
            id += 1
            stk.append(object1);del object2
        else:
            object1 = stk.pop()
            object1.side[object1.acceptID].append([object1.startID,' '])
            object1.side[id] = []
            object1.side[id].append([object1.startID,' '])
            object1.startID = id;object1.ID.append(id)
            id += 1
            object1.side[id] = []
            object1.side[object1.acceptID].append([id,' '])
            object1.acceptID = id;object1.ID.append(id)
            id += 1
            object1.side[object1.startID].append([object1.acceptID,' '])
            stk.append(object1)
    NFA = stk[-1];stk.pop()
    data.NFA = NFA
    temp = {};temp[NFA.acceptID] = 1
    lib.generateGraph("NFA", NFA.ID, NFA.startID, temp, NFA.side)

    #求DFA
    visble = {}
    DFA = lib.DFA()
    array = []
    queue = [];top = 0;end = 0
    def findPoint(id):
        if(array.count(id)): return
        array.append(id)
        for x in NFA.side[id]:
            if(x[1] == ' '):
                findPoint(x[0])

    findPoint(NFA.startID)
    array.sort();
    for i in range(0,array.__len__()): array[i] = str(array[i])
    string = ",".join(array)
    visble[string] = 1
    queue.append(string);end += 1
    DFA.ID.append(string);DFA.startID = string
    DFA.side[string] = []

    while(top < end):
        temp = queue[top].split(",")
        for i in range(0,temp.__len__()): temp[i] = int(temp[i])
        for x in range(0,26):
            array = []
            for y in temp:
                for z in NFA.side[y]:
                    if(z[1] == chr(x + ord('a'))):
                        findPoint(z[0])
            array.sort()
            for i in range(0,array.__len__()): array[i] = str(array[i])
            string = ",".join(array)
            if(string.__len__() == 0): continue
            if(visble.get(string,0)):
                DFA.side[queue[top]].append([string,chr(x + ord('a'))])
                continue
            visble[string] = 1
            DFA.ID.append(string);DFA.side[string] = []
            DFA.side[queue[top]].append([string,chr(x + ord('a'))])
            queue.append(string)
            end += 1
        top += 1

    for x in DFA.ID:
        array = x.split(",")
        for i in range(0,array.__len__()): array[i] = int(array[i])
        if(array.count(NFA.acceptID)): DFA.acceptID[x] = 1

    print(NFA.acceptID)
    print(visble)
    print(DFA.side)
    print(DFA.acceptID)
    print(DFA.ID.__len__())
    data.DFA = DFA
    lib.generateGraph("DFA", DFA.ID, DFA.startID, DFA.acceptID, DFA.side)

    #DFA转最小化DFA
    queue = []
    for i in range(0,DFA.ID.__len__()): queue.append([])
    for i in range(0,DFA.ID.__len__()):
        for j in range(i+1,DFA.ID.__len__()):
            if(DFA.acceptID.get(DFA.ID[i],0)):
                DFA.ID[i],DFA.ID[j] = DFA.ID[j],DFA.ID[i]
    array = [];
    dict = {}

    if(DFA.ID.__len__()-DFA.acceptID.__len__()):
        dict[DFA.ID.__len__()-DFA.acceptID.__len__()] = 1
        array.append(DFA.ID.__len__()-DFA.acceptID.__len__())
    array.append(DFA.ID.__len__())
    dict[DFA.ID.__len__()] = 1
    array.sort()
    for x in queue:
        for i in range(0,26):
            x.append(-1)
    has =  {}
    id = 0
    for i in range(0,DFA.ID.__len__()):
        if(i >= array[id]): id += 1
        has[DFA.ID[i]] = id
    print(has)
    while(1):
        for i in range(0,DFA.ID.__len__()):
            for y in DFA.side[DFA.ID[i]]:
                queue[i][ord(y[1]) - ord('a')] = has[y[0]]
        pre = 0
        for x in array:
            for i in range(pre,x):
                for j in range(i+1,x):
                    flag = 0
                    for r in range(0,26):
                        if(queue[i][r] > queue[j][r]):
                            flag = 1
                            break
                    if(flag):
                        queue[i],queue[j] = queue[j],queue[i]
                        DFA.ID[i],DFA.ID[j] = DFA.ID[j],DFA.ID[i]
            pre = x
        flag = 0
        for i in range(1,queue.__len__()):
            if(queue[i-1] != queue[i]):
                if(dict.get(i,0) == 0):
                    dict[i] = 1
                    array.append(i)
                    flag = 1
        array.sort();id = 0
        for i in range(0, DFA.ID.__len__()):
            if (i >= array[id]): id += 1
            has[DFA.ID[i]] = id
        if(flag == 0): break
    print(has)
    data.queue = queue
    print(queue)

    DFA.startID = has[DFA.startID]
    temp = DFA.acceptID
    DFA.acceptID = {}
    for x in temp:
        DFA.acceptID[has[x]] = 1
    dict = {}
    temp = []
    for i in range(0,DFA.ID.__len__()):
        if(dict.get(has[DFA.ID[i]],0)): continue
        dict[has[DFA.ID[i]]] = 1
        temp.append(queue[i])
    DFA.side = {}
    print(temp)

    for i in range(0,array.__len__()):
        DFA.side[i] = []
        for j in range(0,26):
            if(temp[i][j] == -1):continue
            DFA.side[i].append([temp[i][j],chr(j + ord('a'))])

    DFA.ID = []
    for i in range(0,array.__len__()): DFA.ID.append(i)
    print('---------------')
    print(DFA.ID)
    print(DFA.acceptID)
    print(DFA.startID)
    print(DFA.side)
    data.minDFA = DFA
    lib.generateGraph("minDFA", DFA.ID, DFA.startID, DFA.acceptID, DFA.side)


def checkString():
    DFA = data.minDFA
    string = data.string
    id = DFA.startID
    flag = 1
    if(data.flag):
        for x in string:
            flag = 0
            for y in DFA.side[id]:
                if(y[1] == x):
                    flag = 1
                    id = y[0]
            if(flag == 0):break
    if(data.flag==0 or flag == 0 or DFA.acceptID.get(id,0) == 0):
        data.result = 'False'
    else:data.result = 'True'

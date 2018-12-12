from functools import reduce
import data
def work():
    # 输入产生式
    dict = {}  # 储存每个终结符所对应的产生式
    for i in data.array:
        array = i.split()
        if (dict.get(array[0], 0) == 0):
            dict[array[0]] = []
        temp = []
        for id in range(2, len(array)):
            if (array[id] == '|'):
                dict[array[0]].append(temp)
                temp = []
            else:
                temp.append(array[id])
        dict[array[0]].append(temp)
    arrN = list(dict.keys())  # 非终结符
    arrT = ['ε', '$']  # 终结符
    for x in dict:
        for y in dict[x]:
            for z in y:
                if (arrN.count(z) == 0 and arrT.count(z) == 0):
                    arrT.append(z)
    startSymbol = arrN[0]
    print("输入产生式", dict)
    print("非终结符", arrN)
    print("终结符", arrT)
    print("开始符", startSymbol)

    # 消除左递归
    tot = 0
    array = list(dict.keys())
    for id in array:
        flag = reduce(lambda x, y: x or y, map(lambda x: x[0] == id, dict[id]))
        if (flag):
            dict[id + str(tot)] = [item for item in dict[id] if item[0] == id and (item.append(id + str(tot)) or 1)]
            dict[id] = [item for item in dict[id] if item[0] != id and (item.append(id + str(tot)) or 1)]
            dict[id + str(tot)] = [item for item in dict[id + str(tot)] if item.pop(0)]
            dict[id + str(tot)].append(['ε'])
            tot += 1
    print("消除左递归", dict)

    # 提取左因子
    array = list(dict.keys())
    flag = 0
    while (1):
        flag = 0
        for id in array:
            dict[id].sort(key=lambda x: x[0])
            cnt, l, r = 1, 0, 0
            for x in range(1, len(dict[id])):
                if (dict[id][x][0] == dict[id][x - 1][0]):
                    cnt += 1
                else:
                    if (cnt != 1):
                        flag, l, r = 1, x - cnt, x
                        temp = dict[id][l:r]
                        for y in temp: dict[id].remove(y)
                        dict[id].append([temp[0][0], id + str(tot)])
                        dict[id + str(tot)] = [item for item in temp if len(item) != 1 or item.append(['ε']) or 1]
                        dict[id + str(tot)] = [item for item in dict[id + str(tot)] if len(item) != 2 or item.pop(0)]
                        tot += 1
                        break
            if (flag == 0 and cnt != 1):
                flag, l = 1, len(dict[id]) - cnt
                temp = dict[id][l:]
                for y in temp: dict[id].remove(y)
                dict[id].append([temp[0][0], id + str(tot)])
                dict[id + str(tot)] = [item for item in temp if len(item) != 1 or item.append(['ε']) or 1]
                dict[id + str(tot)] = [item for item in dict[id + str(tot)] if len(item) != 2 or item.pop(0)]
                tot += 1
                break
            if (flag): break
        if (flag == 0): break
    print("提取左因子", dict)


    # 计算first集合
    dictFirst, arrN = {}, list(dict.keys())
    dictFirst['ε'] = 'ε'
    for x in dict:
        if arrT.count(x):
            dictFirst[x] = [x]
        else:
            dictFirst[x] = []
        for y in dict[x]:
            for z in y:
                if arrT.count(z):
                    dictFirst[z] = [z]
                else:
                    dictFirst[z] = []
    while (1):
        flag = 0
        for x in dict:
            temp = sorted(dictFirst[x])
            for id in range(0, len(dict[x])):
                cnt = 0
                for y in dict[x][id]:
                    dictFirst[x] = list(set(dictFirst[x]).union(set(dictFirst[y]).difference(set('ε'))))
                    if dictFirst[y].count('ε') == 0:
                        break
                    cnt += 1
                if cnt == len(dict[x][id]) and dictFirst[x].count('ε') == 0:
                    dictFirst[x].append('ε')
            if temp != sorted(dictFirst[x]):
                flag = 1
        if (flag == 0):
            break
    print("非终结符", arrN)
    print("终结符", arrT)
    print("计算First集合", dictFirst)
    for x in dictFirst:
        if arrT.count(x):continue
        data.stringFirst +="First(" + x + ')' + ' = ' + '{ ' + ' , '.join(dictFirst[x]) + ' }' + '\n'
    print(data.stringFirst)

    # 计算follow集合
    dictFollow = {}
    for item in arrN:
        dictFollow[item] = []
    dictFollow[startSymbol].append('$')


    def cal(lst):
        temp, cnt = [], 0
        for x in lst:
            temp = list(set(temp).union(set(dictFirst[x]).difference(set('ε'))))
            if dictFirst[x].count('ε') == 0:
                break
            cnt += 1
        if cnt == len(lst): temp.append('ε')
        return temp


    while (1):
        flag = 0
        for x in dict:
            for y in dict[x]:
                for id in range(0, len(y)):
                    if (arrT.count(y[id])): continue
                    temp = sorted(dictFollow[y[id]])
                    array = []
                    if (id < len(y) - 1):
                        array = cal(y[id + 1:])
                        dictFollow[y[id]] = list(set(dictFollow[y[id]]).union(set(array).difference(set('ε'))))
                    if id == len(y) - 1 or array.count('ε'):
                        dictFollow[y[id]] = list(set(dictFollow[y[id]]).union(set(dictFollow[x])))
                    if temp != sorted(dictFollow[y[id]]): flag = 1
        if (flag == 0): break
    print("计算Follow集合", dictFollow)
    for x in dictFollow:
        data.stringFollow += "Follow(" + x + ")" + ' = ' + '{ ' + ' , '.join(dictFollow[x]) + ' }' + '\n'
    print(data.stringFollow)

    # 求LL(1)分析表
    vis = 1 #标记是否符合LL(1)文法
    n, m = len(arrN), len(arrT)
    if (arrT.count('ε')): m -= 1
    table = [[-1 for i in range(m + 1)] for i in range(n + 1)]
    print(table)
    print(len(table), len(table[0]))
    for i in range(1, n + 1):
        table[i][0] = arrN[i - 1]
    for i in range(1, m + 1):
        table[0][i] = arrT[i]
    dictF = {}
    cnt = 1
    for x in dict:
        for y in dict[x]:
            temp = x + ' -> ' + ' '.join(y)
            dictF[cnt] = temp
            data.string += str(cnt) + '. ' + temp + '\n'
            y.append(cnt)
            cnt += 1
    for x in dict:
        if (arrT.count(x)): continue
        for y in dict[x]:
            temp = [item for item in y]
            temp.pop()
            array = cal(temp)
            for z in array:
                if z == 'ε': continue
                if table[arrN.index(x) + 1][arrT.index(z)] != -1:vis = 0
                table[arrN.index(x) + 1][arrT.index(z)] = y[-1]
            if array.count('ε'):
                for w in dictFollow[x]:
                    table[arrN.index(x) + 1][arrT.index(w)] = y[-1]

    for i in range(0, len(table)):
        print(table[i])
    if vis:print('success')
    else:print('failed')
    if vis:
        for i in range(0, len(table)):
            for j in range(0, len(table[0])):
                if table[i][j] == -1:
                    print("%7s" % "-", end="")
                else:
                    print("%7s" % table[i][j], end="")
            print()
    data.flag = vis
    if data.flag:
        data.stringTable += "符合LL(1)文法" + '\n'
    else:
        data.stringTable += "不符合LL(1)文法" + '\n'
    for i in range(0,len(table)):
        for j in range(0,len(table[0])):
            if(table[i][j] == -1):
                data.stringTable += '-'.rjust(7,' ')
            else:
                data.stringTable += str(table[i][j]).rjust(7,' ')
        data.stringTable += '\n'
    print(data.stringTable)

    #判断输入串是否符合LL(1)文法
    array = data.stringJudge.split()
    stk,stk1,action,now = [],[],[],0
    stk.append([startSymbol,'$'])
    stk1.append(array+['$'])
    farrN,farrT = {},{}
    for i in range(0,len(arrN)):
        farrN[arrN[i]] = i+1
    for i in range(1,len(arrT)):
        farrT[arrT[i]] = i
    flag = 0
    while(1):
        if(len(stk[-1]) == 1 and len(stk1[-1]) == 1):
            flag = 1;now += 1
            action.append('接受')
            break
        if len(stk[-1]) == 1:
            break
        a = [item for item in stk[-1]]
        b = [item for item in stk1[-1]]
        if stk[-1][0] == stk1[-1][0]:
            action.append('匹配')
            a.pop(0);b.pop(0)
            stk.append(a);stk1.append(b)
            now += 1
            continue
        x,y = farrN[stk[-1][0]],farrT[stk1[-1][0]]
        id = table[x][y]
        if id == -1:
            break
        action.append(dictF[id])
        a.pop(0)
        temp = dictF[id].split()
        for id in range(1,len(temp)-1):
            a = [temp[-id]] + a
        if a[0] == 'ε':a.pop(0)
        stk.append(a);stk1.append(b)
        now += 1

    print(flag)
    data.flagResult= flag
    for i in range(0,now):
        string,string1 = ' '.join(stk[i]),' '.join(stk1[i])
        print("%40s %40s %30s"%(string,string1,action[i]))
    for i in range(0,now):
        string,string1 = ' '.join(stk[i]),' '.join(stk1[i])
        data.stringResult += string.rjust(50,' ') + string1.rjust(60,' ') + action[i].rjust(50,' ') + '\n'
    print(data.stringResult)




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

'''

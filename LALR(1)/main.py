import time
# 输入产生式
print("请输入产生式数量以及产生式")
production_num = int(input())  # 产生式数目
production_data = {}  # 存放产生式
arr_N, arr_T = {}, {}  # 存放非终结符和终结符
start_character = ''  # 开始符
cnt = 0
for id in range(production_num):
    string = input()
    arr = string.strip().split(' -> ')
    arr_N[arr[0]] = 1
    if id == 0:
        start_character = arr[0]
    for item in arr[1].split('|'):
        if production_data.get(arr[0], 0):
            production_data[arr[0]].append(item.strip().split())
        else:
            production_data[arr[0]] = [item.strip().split()]
# 得到终结符
for item in production_data:
    for x in production_data[item]:
        for y in x:
            if arr_N.get(y, 0) == 0:  # 注意在这里ε就被认为是终结符了，如果有的话
                arr_T[y] = 1

# 拓广文法
point_list = []  # 存放每个产生式
DFA_list = []  # 存放每个状态的产生式，产生式可能有多个
point_list.append([start_character + "'", start_character])
DFA_list.append([[start_character + "'", ".", start_character, "|", '$']])
arr_N[start_character + "'"] = 1  # 其实这个没有太大用处
for item in production_data:  # 将产生式存入
    for y in production_data[item]:
        point_list.append([item] + y)

# 计算first集合
dict_first = {}  # 记录每个符号的first集合
dict_first['ε'] = ['ε']  # 这个是为了在计算字符串first集合时方便处理
# 加入终结符的first集合，终结符的first集合就是其本身
for x in arr_T:
    dict_first[x] = [x]
# 初始化非终结符的first集合
for x in arr_N:
    dict_first[x] = []
# 利用循环计算每个非终结符的first集合
while 1:
    flag = 0  # 记录本次循环中是否有非终结符的first集合被更新，如果有进入下次循环
    for item in point_list:  # 遍历每个产生式
        x = item[0]  # x 为产生式的符号
        temp = sorted(dict_first[x])  # 取出该符号的first集合并排序，排序之后便于比较
        cnt = 0  # 用来记录该产生式符号前几个first集合有ε
        for id in range(1, len(item)):  # 遍历该产生式右边的每个符号
            # 利用set合并first集合
            dict_first[x] = list(set(dict_first[x]).union(set(dict_first[item[id]]).difference(set('ε'))))
            if dict_first[item[id]].count('ε') == 0:  # 如果当前first集合没有ε，退出
                break
            cnt += 1
        if cnt == len(item) - 1 and dict_first[x].count('ε') == 0:  # 这时候说明该非终结符的first集合中应该有ε
            dict_first[x].append('ε')
        if temp != sorted(dict_first[x]):  # 这是说明该非终结符的first集合有更新
            flag = 1
    if flag == 0:
        break

# 输出非终结符的first集合
print("非终结符的first集合")
for x in dict_first:
    if arr_T.get(x, 0) or x == 'ε':  # 如果是终结符，就不输出，不过好像第二个条件没用耶
        continue
    string_first = "First(" + x + ')' + ' = ' + '{ ' + ' , '.join(dict_first[x]) + ' }'
    print(string_first)


# 生成NFA
def cal_first(lst, other):  # 求某一后缀的first集合
    lst.pop(0)
    if lst.__len__() == 0:
        return other
    temp, cnt = [], 0
    for x in lst:  # 遍历每个符号
        temp = list(set(temp).union(set(dict_first[x]).difference(set('ε'))))
        if dict_first[x].count('ε') == 0:
            break
        cnt += 1
    if cnt == len(lst):  # 这时候说明应该包含上一个产生式的展望符
        temp = temp + other
    return temp


def cal(arr):  # 生成状态中所有的产生式
    for item in arr:  # 每个item都由产生式和展望符组成，由'|'分开
        # 首先将两者区分开
        temp_id = item.index('|')
        production, look_ahead = item[0:temp_id], item[temp_id + 1:]
        id = production.index(".")  # 得到该产生式中点的位置
        if id == item.__len__() - 1:  # 如果点在最后，继续处理下一个产生式
            continue
        char = item[id + 1]  # 得到点后面的符号
        if arr_T.get(char, 0):  # 如果点后面的符号式终结符，没有新的产生式可以添加，继续处理下一个产生式
            continue
        # 否则添加新的产生式
        for item1 in point_list:  # 遍历每个产生式
            if item1[0] == char:  # 如果找到符合条件的产生式
                temp_look_ahead = cal_first(production[id + 1:], look_ahead)  # 首先计算出该产生式的展望符
                look_ahead.sort()
                # 这时候应该查看该产生式有没有已经在状态中出现
                temp_flag = 1  # 1代表没有出现，0代表出现
                for i in range(0, arr.__len__()):
                    temp1_id = arr[i].index('|')
                    temp1_production, temp1_look_ahead = arr[i][0:temp1_id], arr[i][temp1_id + 1:]
                    if temp1_production == [item1[0], "."] + item1[1:]:  # 如果出现了就合并展望集
                        temp1_look_ahead = list(set(temp1_look_ahead).union(set(temp_look_ahead)))
                        temp_flag = 0
                        temp1_look_ahead.sort()
                        arr[i] = temp1_production + ['|'] + temp1_look_ahead
                        break
                if temp_flag == 0:  # 如果之前出现就不用添加新的产生式
                    continue
                # 否则添加新的产生式
                temp_look_ahead.sort()
                arr.append([item1[0], "."] + item1[1:] + ['|'] + temp_look_ahead)
    arr.sort()
    return arr
table = {}  # 用来存放状态边表
for arr in DFA_list:  # 遍历每个状态的产生式
    i = DFA_list.index(arr)  # 找到每个状态的下标
    table[i] = []  # 初始化每个状态的边表
    arr = cal(arr)  # 补全该状态中的产生式
    # 对这个状态建边
    vis = {}  # 用来储存点后面相同的产生式
    # 首先对点后面所有相同的产生式归类并移动
    # 遍历产生式
    for item in arr:
        temp_id = item.index('|')
        temp_production, look_ahead = item[0:temp_id], item[temp_id + 1:]
        id1 = temp_production.index(".")  # 得到该产生式中点的位置
        if id1 == temp_production.__len__() - 1:  # 如果点在最右端就继续处理下一个产生式
            continue
        temp_char = temp_production[id1 + 1]  # 得到点后面的符号
        if temp_char == 'ε':  # 如果点后面是空也不必处理
            continue
        # 然后移动产生式中的点
        if id1 != temp_production.__len__() - 2:  # 如果点不在倒数第二个中
            temp = temp_production[0:id1] + temp_production[id1 + 1:id1 + 2] + ["."] + temp_production[id1 + 2:]
        else:
            temp = temp_production[0:id1] + temp_production[id1 + 1:id1 + 2] + ["."]
        if vis.get(temp_char, 0):  # 如果已经有相同的
            look_ahead.sort()
            vis[temp_char].append(temp + ['|'] + look_ahead)
        else:
            look_ahead.sort()
            vis[temp_char] = [temp + ['|'] + look_ahead]
    for item in vis:  # 排序处理便于之后比较
        vis[item].sort()
    # 对vis中的每一个核心式连边
    for item in vis:
        temp = cal(vis[item])  # 首先生成所有产生式
        # 查找该状态是否已经出现
        if DFA_list.count(temp):  # 如果出现
            # 找到该状态的下标
            id1 = DFA_list.index(temp)
            # 添加当前状态与该状态的边
            table[i].append((item, id1))
        else:
            # 没有出现则加入list中
            table[i].append((item, DFA_list.__len__()))
            DFA_list.append(temp)

final_flag = 1  # 判断该文法是不是能用LR(1)分析

#上面已经得到先前LR(1)中的NFA了，这时候需要对NFA进行同心项合并
#合并的时候需要注意判断“规约-规约”冲突，并需要改变NFA边表
fa = [] #首先初始化映射数组并映射到自己
for i in range(DFA_list.__len__()):
    fa.append(i)
vis = [0 for _ in range(DFA_list.__len__())] # 标记有哪些状态经过合并后被废弃 1 表示被废弃

for i in range(DFA_list.__len__()):# 判断当前状态是否是后面的同心项
    if vis[i] == 1: # 如果当前状态已经被废弃说明当前状态已经被合并，不在考虑
        continue
    all_same = [DFA_list[i]] # 存放可以合并的同心项
    all_same_id = [i] # 存放可以合并的同心项id
    temp = [] #存放当前状态所有的产生式并排序，方便比较
    for item in DFA_list[i]:# 遍历当前状态每个产生式
        temp_id = item.index('|')
        temp.append(item[0:temp_id]) # 添加当前产生式
    temp.sort() # 排序方便比较
    for j in range(i+1,DFA_list.__len__()):
        temp_j = [] #存放当前状态所有产生式，同上
        for item in DFA_list[j]:
            temp_id = item.index('|')
            temp_j.append(item[0:temp_id])
        temp_j.sort()
        if temp == temp_j: # 如果相等说明状态i找到了同心项
            all_same.append(DFA_list[j])
            all_same_id.append(j)
    if all_same.__len__() == 1: #说明状态i没有找到可以合并的同心项
        continue
    # 这时候说明有同心项可以合并，首先需要将后面的状态作废，并且改变映射
    for j in range(1,all_same_id.__len__()): # 这里不包括开头注意
        vis[all_same_id[j]] = 1
        fa[all_same_id[j]] = i
    # 然后需要合并展望符，以第一个为蓝本
    for item in all_same[0]: # 遍历每一个产生式,注意修改的时候需要先找到item的id
        temp_id = item.index('|')
        temp_production,look_ahead = item[0:temp_id] , item[temp_id + 1:]
        # 然后从其余的状态中寻找可以合并的展望符
        for j in range(1,all_same.__len__()): # 这里也不包括开头
            for item1 in all_same[j]: # 遍历每个产生式
                temp1_id = item1.index('|')
                temp1_production,temp_look_ahead = item1[0:temp1_id] , item1[temp1_id + 1:]
                if temp_production == temp1_production: # 这时候说明可以有展望符合并
                    look_ahead = list(set(look_ahead).union(set(temp_look_ahead))) # 使用list合并
        # 最后更新
        look_ahead.sort()
        all_same[0][all_same[0].index(item)] = temp_production + ['|'] + look_ahead
    # 最后需要判断是否出现了“规约-规约”冲突
    temp = [] # 用来存需要规约的产生式的展望符
    for item in all_same[0]: # 遍历已经更新好的状态
        temp_id = item.index('|')
        if item[0:temp_id][-1] != '.' and item[0:temp_id][-1] != 'ε': # 说明该产生式不需要规约
            continue
        temp.append(item[temp_id+1:])
    for x in range(temp.__len__()):
        for y in range(x+1,temp.__len__()):
            if list(set(temp[x]).difference(set(temp[y]))) != []:# 如果不为空说明产生了“规约-规约”冲突,该文法不能用LALR(1)法分析
                final_flag = 0
# 这里需要对DFA_list 更新
temp = DFA_list
DFA_list = []
new_fa = {}
for i in range(temp.__len__()):
    if vis[i] == 1: #这时说明该状态被废弃
        new_fa[i] = new_fa[fa[i]]
        continue
    new_fa[i] = DFA_list.__len__()
    DFA_list.append(temp[i])

# 这里需要对DFA边表table更新
temp = table
table = {}
for item in temp:
    table[new_fa[item]] = []
    for x in temp[item]:
        table[new_fa[item]].append((x[0],new_fa[x[1]]))



# 输出每个状态的产生式
for i in range(DFA_list.__len__()):
    print("该状态编号为{id}".format(id=i))
    for item in DFA_list[i]:
        temp_id = item.index('|')
        temp_production, look_ahead = item[0:temp_id], item[temp_id + 1:]
        print(temp_production[0] + "->" + "".join(temp_production[1:]), look_ahead)
# 输出状态之间的边表
print("DFA的边表")
for item in table:
    for temp in table[item]:
        print("状态 {x} 经 {y} 到状态 {z}".format(x=item, y=temp[0], z=temp[1]))

# 输出扩广文法
for i in range(point_list.__len__()):
    print(str(i).rjust(len(str(point_list.__len__()))), end='')
    print("  " + point_list[i][0] + "->" + "".join(point_list[i][1:]))


# 求LALR(1)分析表
print("LALR(1)分析表")
len = 2
for item in arr_T:
    len = max(len, item.__len__())
for item in arr_N:
    len = max(len, item.__len__())
arr_T['$'] = 1  # 将该符加入终结符中，方便之后处理
arr = [['']]  # 用二维数组存分析表
sum = 0  # 记录终结符和非终结符一共有几个，方便制作表格
for item in arr_T:
    if item == 'ε':
        continue
    arr[0].append(item)  # 添加表头，先添加终结符
    sum += 1
for item in arr_N:
    if item == start_character + "'":
        continue
    arr[0].append(item)  # 添加表头，后添加非终结符
    sum += 1
temp_id = 1
for id in range(DFA_list.__len__()):
    temp_flag = 0
    for x in DFA_list[id]:
        temp_id = x.index('|')
        if x[0:temp_id] == [start_character + "'", start_character, "."]:
            temp_flag = 1
            break
    if temp_flag == 1:
        temp_id = id
        break
table[temp_id].append(('$', 'acc'))  # 将结束条件加入边表中，方便之后处理
map_text = {}  # 存分析表中的边表
for i in range(DFA_list.__len__()):  # 遍历每个状态
    arr.append([str(i)] + ['-' for _ in range(sum)])  # 首先初始化分析表中该状态的一行
    for item in table[i]:  # 遍历该状态的边表
        x, y = item[0], item[1]
        if arr_T.get(x, 0):  # 如果是终结符
            id_x = arr[0].index(x)  # 找到该终结符在表中的列位置
            map_text[(str(i), x)] = str(y)  # 加入分析表的边表中
            y = str(y) if str(y) == 'acc' else 's' + str(y)  # 加一些符号
            arr[-1][id_x] = y  # 加入分析表中
        else:
            id_x = arr[0].index(x)  # 找到该非终结符在表中的位置
            arr[-1][id_x] = str(y)  # 加入分析表中
            map_text[(str(i), x)] = str(y)  # 加入边表中
    # 查看该状态中是否有产生式需要规约并判断该文法是不是可以用LR(1)方法分析
    for item in DFA_list[i]:
        temp_id = item.index('|')  # 找到|的id
        production, look_ahead = item[0:temp_id], item[temp_id + 1:]  # 分别得到产生式和展望符
        if production[-1] != '.' and production[-1] != 'ε':  # 如果点不在最后或者产生式不是空不需要规约
            continue
        # 如果需要规约
        temp = production
        if production[-1] == '.':
            temp.pop()  # 提取出该产生式
        else:
            temp = temp[0:1] + temp[2:]  # 去掉空产生式中的点
        id = point_list.index(temp)  # 找到该产生式的标号
        for j in range(1, arr[-1].__len__()):
            if look_ahead.count(arr[0][j]):  # 如果可以填
                if arr[-1][j] != '-' and arr[-1][j] != 'acc':  # 产生冲突，这时候说明该文法不能用LR(1)方法分析
                    final_flag = 0
                if arr[-1][j] == '-':
                    arr[-1][j] = 'r' + str(id)  # 加入分析表中
                    map_text[(str(i), arr[0][j])] = 'r' + str(id)  # 加入边表中

# 输出分析表
for item in arr:
    for x in item:
        print(x.rjust(len + 2), end='')
    print()
if final_flag == 0:
    print("这个文法其实不能用LALR(1)文法分析，分析表是错的")

# 测试字符串

print("请输入待测字符串")
string_arr = input().strip().split()
result = []
arr_test = []
result.append(['分析栈', '输入', '动作'])
stk_test = [str(0)]
stk_str = string_arr + ['$']
while 1:
    result.append([])
    result[-1].append('$,' + ','.join(stk_test))
    result[-1].append("".join(stk_str))
    temp = map_text[(stk_test[-1], stk_str[0])]  # 查找应该进行什么动作
    if temp == 'acc':  # 这时说明成功
        result[-1].append('accept')
        break
    elif temp[0] == 'r':  # 这时说明需要规约
        i = int(temp[1:])
        result[-1].append('reduce  ' + point_list[i][0] + "->" + "".join(point_list[i][1:]))
        len = point_list[i].__len__() - 1
        if point_list[i].count('ε'):
            len -= 1
        len = 2 * len
        while len:  # 弹出相应东西
            stk_test.pop()
            len -= 1
        id = stk_test[-1]
        stk_test.append(point_list[i][0])
        stk_test.append(map_text[(id, point_list[i][0])])
    else:  # 这时候继续前进
        result[-1].append('shift')
        stk_test.append(stk_str[0])
        stk_test.append(map_text[(stk_test[-2], stk_test[-1])])
        stk_str = stk_str[1:]
length = 0
for item in result:
    for x in item:
        length = max(length, x.__len__())
for item in result:
    print(item[0].ljust(length + 2), end='')
    print(item[1].rjust(length + 2), end='')
    print("".rjust(length // 2), end='')
    print(item[2].ljust(length + 2))

'''
1
A -> B c | d
d

1
E -> E + n | n
n + n

3
S -> a A | b B
A -> c A | d
B -> c B | d
a c d

2
S -> a A
A -> c A | d
a c c d

3
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
id * id + id

1
E -> E + n | n
n + n

1
S -> ( S ) S | ε
( ) ( )

3
S -> id | V := E
V -> id
E -> V | n
id := id

1
A -> ( A ) | a
( ( a ) )

2
S -> C C
C -> c C | d
c d c d

3
S -> a A d | b B d | a B e | b A e
A -> c
B -> c

3
S -> L = R | R
L -> * R | i
R -> L
'''

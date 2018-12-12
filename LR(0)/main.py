print("请输入产生式数量以及产生式：")
# 输入产生式
production_num = int(input())
production_data = {}  # 存放产生式
arr_N, arr_T = {}, {}  # 存放非终结符和终结符
start_character = ''  # 开始符
cnt = 0  # 变量名计数
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
            if arr_N.get(y, 0) == 0:
                arr_T[y] = 1
# 拓广文法
point_list = []  # 存放每个产生式
DFA_list = []  # 存放每个状态的产生式,产生式可能有多个
point_list.append([start_character + "'", start_character])
DFA_list.append([[start_character + "'", ".", start_character]])

for item in production_data:
    for y in production_data[item]:
        point_list.append([item] + y)


def cal(arr):  # 不断加入可以加入的产生式
    for item in arr:
        # 处理item这个产生式
        id = item.index(".")  # 得到点的位置
        if id == item.__len__() - 1:  # 点在最后,继续处理下一个产生式
            continue
        char = item[id + 1]  # 得到点后面的符号
        # 否则添加新的产生式
        for item1 in point_list:
            if item1[0] == char and arr.count([item1[0], "."] + item1[1:]) == 0:  # 找到符合条件的产生式
                arr.append([item1[0], "."] + item1[1:])  # 添加产生式
    arr.sort()
    return arr


# 生成DNA和分析表
table = {}
for arr in DFA_list:
    i = DFA_list.index(arr)
    table[i] = []
    arr = cal(arr)
    # 对这个状态建边
    vis = {}
    # 首先对点后面所有相同的产生式归类同时移动
    # 遍历产生式
    for item in arr:
        id1 = item.index(".")
        if id1 == item.__len__() - 1:  # 如果点已经在最后就处理下一个产生式
            continue
        temp_char = item[id1 + 1]
        if temp_char == 'ε':  # 如果点后面是空也不必处理
            continue
        # 然后移动核心式
        if id1 != item.__len__() - 2:
            temp = item[0:id1] + item[id1 + 1:id1 + 2] + ["."] + item[id1 + 2:]
        else:
            temp = item[0:id1] + item[id1 + 1:id1 + 2] + ["."]
        if vis.get(temp_char, 0):
            # 如果已经有相同的了
            vis[temp_char].append(temp)
        else:
            vis[temp_char] = [temp]
    for item in vis:
        vis[item].sort()
    # 对vis中的每一个产生式连边
    for item in vis:
        temp = cal(vis[item])
        # 查找移动过后的核心式是否已经出现
        if DFA_list.count(temp):
            # 如果出现
            id1 = DFA_list.index(temp)
            # 找到id并加入边表中
            table[i].append((item, id1))
        else:
            # 没有出现则新加入list中
            table[i].append((item, DFA_list.__len__()))
            DFA_list.append(temp)
flag = 1  # 用来记录该文法是不是能用LR(0)
for i in range(0, DFA_list.__len__()):
    for x in DFA_list[i]:
        if (x[-1] == '.' or x[-1] == 'ε') and DFA_list[i].__len__() != 1:
            flag = 0

# 实在是不想写UI了
# 输出每个状态的产生式
for i in range(DFA_list.__len__()):
    print("该状态编号为{id}".format(id=i))
    for item in DFA_list[i]:
        print(item[0] + "->" + "".join(item[1:]))
# 输出状态之间的边表
print("DFA的边表")
for item in table:
    for temp in table[item]:
        print("状态 {x} 经 {y} 到状态 {z}".format(x=item, y=temp[0], z=temp[1]))
# 输出扩广文法
for i in range(point_list.__len__()):
    print(str(i).rjust(len(str(point_list.__len__()))), end='')
    print("  " + point_list[i][0] + "->" + "".join(point_list[i][1:]))
# LR(0)输出分析表
print("LR(0)分析表")
len = 2
for item in arr_T:
    len = max(len, item.__len__())
for item in arr_N:
    len = max(len, item.__len__())
arr_T['$'] = 1
arr = [['']]
sum = 0
for item in arr_T:
    if item == 'ε':
        continue
    arr[0].append(item)
    sum += 1
for item in arr_N:
    arr[0].append(item)
    sum += 1
temp_id = 1
for id in range(DFA_list.__len__()):
    flag = 0
    for x in DFA_list[id]:
        if x == [start_character + "'", start_character, "."]:
            flag = 1
            break
    if flag == 1:
        temp_id = id
        break
table[temp_id].append(('$', 'acc'))
map_text = {}
for i in range(DFA_list.__len__()):
    arr.append([str(i)] + ['-' for _ in range(sum)])
    for item in table[i]:
        x, y = item[0], item[1]
        if arr_T.get(x, 0):
            id_x = arr[0].index(x)
            map_text[(str(i), x)] = str(y)
            y = str(y) if str(y) == 'acc' else 's' + str(y)
            arr[-1][id_x] = y
        else:
            id_x = arr[0].index(x)
            arr[-1][id_x] = str(y)
            map_text[(str(i), x)] = str(y)
    temp_flag = 0  # 查找当前状态中是否有ε
    temp_production = []
    for item in DFA_list[i]:
        for x in item:
            if x == 'ε':
                temp_flag = 1
                temp_production = item
    if table[i].__len__() == 0 or temp_flag:
        temp = DFA_list[i][0]
        if table[i].__len__() == 0:
            temp.pop()
        else:
            temp = temp_production[0:1] + temp_production[2:]
        id = point_list.index(temp)
        for j in range(1, arr[-1].__len__()):
            if arr_T.get(arr[0][j], 0):
                if arr[-1][j] == '-':
                    arr[-1][j] = 'r' + str(id)
                    map_text[(str(i), arr[0][j])] = 'r' + str(id)

for item in arr:
    for x in item:
        print(x.rjust(len + 2), end='')
    print()
if flag == 0:
    print("这个文法其实不能用LR(0)文法分析，分析表是错的")
# 测试字符串
print('请输入待测字符串')
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
    temp = map_text[(stk_test[-1], stk_str[0])]
    if temp == 'acc':
        result[-1].append('accept')
        break
    elif temp[0] == 'r':
        i = int(temp[1:])
        result[-1].append('reduce  ' + point_list[i][0] + "->" + "".join(point_list[i][1:]))
        len = point_list[i].__len__() - 1
        if point_list[i].count('ε'):
            len -= 1
        len = 2 * len
        while len:
            stk_test.pop()
            len -= 1
        id = stk_test[-1]
        stk_test.append(point_list[i][0])
        stk_test.append(map_text[(id, point_list[i][0])])
    else:
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
    print("".rjust(length + 2), end='')
    print(item[2].ljust(length + 2))

'''
1
A -> B c | d

1
E -> E + n | n

3
S -> a A | b B
A -> c A | d
B -> c B | d
a c c d

2
S -> a A
A -> c A | d

1
S -> ( S ) S | ε
( ) ( )

'''

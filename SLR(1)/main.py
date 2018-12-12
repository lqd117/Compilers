# 输入产生式
print("请输入产生式数量以及产生式：")
production_num = int(input())  # 产生式数目
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
arr_N[start_character + "'"] = 1

for item in production_data:
    for y in production_data[item]:
        point_list.append([item] + y)

# 计算first集合
dict_first = {}  # 记录每个符号的first集合
dict_first['ε'] = ['ε']  # 这个待定
# 加入终结符的first集合 ，终结符的first集合就是其本身
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
        temp = sorted(dict_first[x])  # 找出该符号的first集合并排序，排序便于之后比较
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
    if arr_T.get(x, 0) or x == 'ε':  # 如果是终结符，就不输出
        continue
    string_first = "First(" + x + ')' + ' = ' + '{ ' + ' , '.join(dict_first[x]) + ' }'
    print(string_first)

# 计算follow集合
dict_follow = {}  # 存每个非终结符的follow集合，follow集合只有非终结符有
for item in arr_N:  # 初始化每个非终结符的follow集合
    dict_follow[item] = []
dict_follow[start_character + "'"].append('$')  # 开始符一开始有$符号


def cal(lst):  # 该方法用来计算字符串的first集合
    temp, cnt = [], 0
    for x in lst:  # 遍历每个符号
        temp = list(set(temp).union(set(dict_first[x]).difference(set('ε'))))
        if dict_first[x].count('ε') == 0:
            break
        cnt += 1
    if cnt == len(lst):  # 这时候说明该字符串的first集合需要ε
        temp.append('ε')
    return temp


while 1:  # 通过不断循环的方式计算非终结符的follow集合
    flag = 0  # 用来标记是否在该次循环中有某个非终结符的follow集合有所更新
    for item in point_list:  # 遍历每个产生式
        x = item[0]  # x为产生式的符号
        for id in range(1, len(item)):
            if arr_T.get(item[id], 0):  # 如果当前元素是终结符，继续处理下一条产生式
                continue
            array = []  # 用来存字符串的first集合
            temp = sorted(dict_follow[item[id]])  # 取出当前非终结符的follow集合并排序，方便之后比较
            if id < len(item) - 1:  # 如果当前非终结符没有处在该产生式最右端
                array = cal(item[id + 1:])  # 获取该非终结符之后字符串的first集合
                dict_follow[item[id]] = list(set(dict_follow[item[id]]).union(set(array).difference(set('ε'))))
            if id == len(item) - 1 or array.count('ε'):  # 这时候需要将该产生式符号的follow集合合并
                dict_follow[item[id]] = list(set(dict_follow[item[id]]).union(set(dict_follow[x])))
            if temp != sorted(dict_follow[item[id]]):  # 这个时候说明需要再次循环
                flag = 1
    if flag == 0:  # 如果不需要再次循环就退出循环
        break
print("非终结符的follow集合")
for x in dict_follow:
    string_follow = "Follow(" + x + ")" + ' = ' + '{ ' + ' , '.join(dict_follow[x]) + ' }'
    print(string_follow)

# 生成NFA
def cal(arr):  # 生成状态中所有的产生式
    for item in arr:
        # 处理item这个产生式
        id = item.index(".")  # 得到该产生式中点的位置
        if id == item.__len__() - 1:  # 如果点在最后，继续处理下一个产生式
            continue
        char = item[id + 1]  # 得到点后面的符号
        if arr_T.get(char, 0):  # 如果点后面的符号是终结符，没有新的产生式可以添加，继续处理下一个产生式
            continue
        # 否则添加新的产生式
        for item1 in point_list:
            if item1[0] == char and arr.count([item1[0], "."] + item1[1:]) == 0:  # 如果找到符合条件的产生式
                arr.append([item1[0], "."] + item1[1:])  # 添加产生式
    arr.sort()
    return arr


table = {}  # 用来存放状态边表
for arr in DFA_list:  # 遍历每个状态的产生式
    i = DFA_list.index(arr)  # 找到每个状态的下标
    table[i] = []  # 初始化每个状态的边表
    cal(arr)
    # 对这个状态建边
    vis = {}  # 用来储存点后面相同的产生式
    # 首先对点后面所有相同的产生式归类并移动
    # 遍历产生式
    for item in arr:
        id1 = item.index(".")  # 得到该产生式中点的位置
        if id1 == item.__len__() - 1:  # 如果点在最右端就继续处理下一个产生式
            continue
        temp_char = item[id1 + 1]  # 得到点后面的符号
        if temp_char == 'ε':  # 如果点后面是空也不必处理
            continue
        # 然后移动产生式中的点
        if id1 != item.__len__() - 2:  # 如果点不在倒数第二个中
            temp = item[0:id1] + item[id1 + 1:id1 + 2] + ["."] + item[id1 + 2:]
        else:
            temp = item[0:id1] + item[id1 + 1:id1 + 2] + ["."]
        if vis.get(temp_char, 0):  # 如果已经有相同的
            vis[temp_char].append(temp)
        else:
            vis[temp_char] = [temp]
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

final_flag = 1  # 判断该文法是不是能用SLR(1)分析

# 求SLR(1)分析表
print("SLR(1)分析表")
# 先求最大长度方便制作表格
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
    arr[0].append(item)  # 添加表头,先添加终结符
    sum += 1
for item in arr_N:
    if item == start_character + "'":
        continue
    arr[0].append(item)  # 添加表头，后添加非终结符
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
    # 查看该状态中是否有产生式需要规约并判断该文法是不是可以用SLR(1)方法分析
    for item in DFA_list[i]:
        if item[-1] != '.' and item[-1] != 'ε':  # 如果点不在最右端说明该产生式不需要规约
            continue
        # 如果需要规约
        temp = item
        if item[-1] == '.':
            temp.pop()  # 提取出该产生式
        else:
            temp = temp[0:1] + temp[2:]
        id = point_list.index(temp)  # 找到该产生式的标号
        for j in range(1, arr[-1].__len__()):
            if dict_follow[temp[0]].count(arr[0][j]):  # 如果可以填
                if arr[-1][j] != '-' and arr[-1][j] != 'acc':  # 产生冲突，这时候说明该文法不能用SLR(1)方法分析
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
    print("这个文法其实不能用SLR(1)文法分析，分析表是错的")

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

1
E -> E + n | n

3
S -> a A | b B
A -> c A | d
B -> c B | d

2
S -> a A
A -> c A | d

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
'''

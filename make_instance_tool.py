import random
import math, sys
import MASTER

random.seed(MASTER.random_seed)
print("random seed: ", MASTER.random_seed)

def get_ramp_block(a, b):
    enter_block = MASTER.ramp_block_to_down_floor
    exit_block = MASTER.ramp_block_to_upper_floor

    return enter_block, exit_block


def split_total_car_area(total_area, m):
    theta_list = [0]
    
    # total_areaをm個の区間に分割し、m-1個の区切りをランダムに選択する
    for k in range(m-1):
        theta_list.append(random.randint(int(total_area*k/m), int(total_area*(k+1)/m)))
    theta_list.append(total_area)
    
    return theta_list


def generate_car(m, total_amount, port_list):
    car_info_list = []
    theta_list = split_total_car_area(total_amount, m)
    Port_Pair_flag = {(l,d): 0 for l in range(len(port_list)) for d in range(len(port_list))}
    
    for k in range(m):
        # LPは前半の半分から、DPは後半の半分からランダムに選択する
        lp = random.choice(port_list[:math.floor(len(port_list)/2)])
        dp = random.choice(port_list[math.floor(len(port_list)/2):])
        while Port_Pair_flag[lp,dp] == 1:
            lp = random.choice(port_list[:math.floor(len(port_list)/2)])
            dp = random.choice(port_list[math.floor(len(port_list)/2):])
        Port_Pair_flag[lp,dp] = 1
        
        # amount = math.floor(total_amount / m) # 一様に分配
        # car_info_list.append((lp, dp, amount))
        
        car_area = theta_list[k+1] - theta_list[k] # 乱数で分配
        car_info_list.append((lp, dp, car_area))
    
    # print("car_info_list: ", car_info_list)
    
    return car_info_list


def generate_dummy_car(port_list):
    lp = random.choice(port_list[:math.floor(len(port_list)/2)])
    dp = random.choice(port_list[math.floor(len(port_list)/2):])
    
    return lp, dp


def generate_block(a, b):    
    E = []
    
    # 一旦全ての枝を作成
    for i in range(a):
        for j in range(b-1):
            E.append((i*b+j, i*b+j+1))
            E.append((i*b+j+1, i*b+j))
    
    for i in range(a-1):
        for j in range(b):
            E.append((i*b+j, i*b+j+b))
            E.append((i*b+j+b, i*b+j))
    
    # 入口0への枝と、出口n+1からの枝を削除する
    enter_block, exit_block = get_ramp_block(a, b)
    for edge in E:
        if edge[1] == enter_block:
            E = [e for e in E if e != edge]
            
        if edge[0] == exit_block:
            E = [e for e in E if e != edge]
    
    ## 出入口からの枝を1方向に限定（右のみ）
    if MASTER.limit_ramp_branch_model == 1:
        for edge in E:
            if edge[0] == enter_block:
                if edge[1] != enter_block + 1:
                    E = [e for e in E if e != edge]
            elif edge[1] == exit_block:
                if edge[0] != exit_block - 1:
                    E = [e for e in E if e != edge]
    
    return E

def get_block_direction(EdgeList, input_b):
    a = {(i,j): 0 for (i,j) in EdgeList}
    
    for edge in EdgeList:
        if edge[1] - edge[0] == 1 or edge[1] - edge[0] == -1:
            a[edge] = 1
        elif edge[1] - edge[0] == input_b or edge[1] - edge[0] == -input_b:
            a[edge] = 0
        else:
            print("error")
            sys.exit()
    
    return a

def set_hold():
    a, b = MASTER.input_a, MASTER.input_b
    enter_block, exit_block = get_ramp_block(a, b)
    H1, H2, H3, H4 = [], [], [], []
    
    for i in range(a*b):
        if i == enter_block or i == exit_block:
            continue
        temp = i % b
        if temp <= round(b/4):
            H1.append(i)
        elif temp <= round(b/2):
            H2.append(i)
        elif temp <= round(b*3/4):
            H3.append(i)
        else:
            H4.append(i)
    
    Hold_List = [H1, H2, H3, H4]
    
    return Hold_List


def get_sekiwari_results(M: list):
    C1, C2, C3, C4 = [], [], [], []
    
    # ホールドh(1,2,3,4)に対して配置できない車種をランダムに選択する
    C1.append(random.choice(M))
    C2.append(random.choice(M))
    C3.append(random.choice(M))
    C4.append(random.choice(M))
    Penalty_Car_List = [C1, C2, C3, C4]
    
    # 各車種に対して配置できるホールドをリストに格納する
    Sekiwari_Results = []
    for k in range(len(M)):
        temp_Results = []
        if M[k] not in C1:
            temp_Results.append(1)
        if M[k] not in C2:
            temp_Results.append(2)
        if M[k] not in C3:
            temp_Results.append(3)
        if M[k] not in C4:
            temp_Results.append(4)
        Sekiwari_Results.append(temp_Results)
        
    return Penalty_Car_List, Sekiwari_Results


def get_detailed_sekiwari_results(M: list, p: list):
    r = [[0 for i in range(4)] for j in range(len(M))]
    
    for k in range(len(M)):
        for h in range(4):
            r[k][h] = p[k]/4 # 一旦全てのホールドに同じ割合で配置する
    
    return r


def get_Next_block_list(i):
    a, b = MASTER.input_a, MASTER.input_b
    Next_block_list = []
    
    if not i % b == 0:
        Next_block_list.append(i - 1)
    if not i % b == b-1:
        Next_block_list.append(i + 1)
    if not i < b:
        Next_block_list.append(i - b)
    if not i >= b*(a-1):
        Next_block_list.append(i + b)
    
    enter_block, exit_block = get_ramp_block(a, b)
    try:
        Next_block_list.remove(enter_block)
    except:
        pass
    try:
        Next_block_list.remove(exit_block)
    except:
        pass
    
    return Next_block_list


def get_gang_preferences(M):
    M_same = [] # 同じ方向での出入りを好む車種
    M_reverse = [] # 逆方向での出入りを好む車種
    M_discripttion = []
    
    for i in range(len(M)):
        rand_flag = random.randint(0, 2)
        if rand_flag == 0:
            M_same.append(i)
            M_discripttion.append("same")
        elif rand_flag == 1:
            M_reverse.append(i)
            M_discripttion.append("reverse")
        else:
            M_discripttion.append("none")
            
    return M_same, M_reverse, M_discripttion


def get_delta(i, E):
    N_i = get_Next_block_list(i)
    for j in N_i:
        if (j, i) in E:
            continue
        else:
            N_i.remove(j)
            
    return N_i

def get_sigma(i, j):
    reverse_block = get_reverse_block(i, j)
    if reverse_block != None:
        enter_block, exit_block = get_ramp_block(MASTER.input_a, MASTER.input_b)
        if reverse_block == enter_block or reverse_block == exit_block:
            return None
        return reverse_block
    
    return None
    

def get_reverse_block(i,j):
    a, b = MASTER.input_a, MASTER.input_b
    
    if i == j+1 and i % b != b-1 and i % b != 0:
        return i+1
    elif i == j-1 and i % b != 0 and i % b != b-1:
        return i-1
    elif i == j+b and i < b*(a-1):
        return i+b
    elif i == j-b and i >= b:
        return i-b
    else:
        return None
    

def get_penalty_edges(i, j, E):
    a, b = MASTER.input_a, MASTER.input_b
    
    penalty_edges = []
    if i == j+1 or i == j-1:
        if (j, j-b) in E:
            penalty_edges.append((j, j-b))
        if (j, j+b) in E:
            penalty_edges.append((j, j+b))
    else:
        if (j, j-1) in E:
            penalty_edges.append((j, j-1))
        if (j, j+1) in E:
            penalty_edges.append((j, j+1))
    
    return penalty_edges
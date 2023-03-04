import random
import math
import MASTER

random.seed(MASTER.random_seed)
print("random seed: ", MASTER.random_seed)

def get_ramp_block(a, b):
    enter_block = math.floor(b/2)
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
        while Port_Pair_flag[lp,dp] == 0:
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
    
    # # 入口からの枝を1方向に限定（右のみ）
    if MASTER.limit_ramp_branch_model == 1:
        for edge in E:
            if edge[0] == enter_block:
                if edge[1] != enter_block + 1:
                    E = [e for e in E if e != edge]
    
    return E


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


def make_Next_block_list(i):
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
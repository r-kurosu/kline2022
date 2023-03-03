import random
import math
import MASTER

random.seed(MASTER.random_seed)
print("random seed: ", MASTER.random_seed)

def get_ramp_block(a, b):
    enter_block = math.floor(b/2)
    exit_block = enter_block + 1 

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

    for k in range(m):
        # LPは前半の半分から、DPは後半の半分からランダムに選択する
        lp = random.choice(port_list[:math.floor(len(port_list)/2)])
        dp = random.choice(port_list[math.floor(len(port_list)/2):])
            
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
    edge_list = []
    
    # 一旦全ての枝を作成
    for i in range(a):
        for j in range(b-1):
            edge_list.append((i*b+j, i*b+j+1))
            edge_list.append((i*b+j+1, i*b+j))
    
    for i in range(a-1):
        for j in range(b):
            edge_list.append((i*b+j, i*b+j+b))
            edge_list.append((i*b+j+b, i*b+j))
    
    # 入口0への枝と、出口n+1からの枝を削除する
    enter_block, exit_block = get_ramp_block(a, b)
    
    for edge in edge_list:
        if edge[1] == enter_block:
            edge_list = [e for e in edge_list if e != edge]
            
        if edge[0] == exit_block:
            edge_list = [e for e in edge_list if e != edge]
    
    return edge_list


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
import random
import math

def get_ramp_block(a, b):
    enter_block = math.floor(b/2)
    exit_block = enter_block + 1 

    return enter_block, exit_block


def generate_car(m, total_amount, port_list):
    car_info_list = []
    
    for _ in range(m):
        # LPは前半の半分から、DPは後半の半分からランダムに選択する
        lp = random.choice(port_list[:math.floor(len(port_list)/2)])
        dp = random.choice(port_list[math.floor(len(port_list)/2):])
        amount = math.floor(total_amount / m) # TODO:今は全ての車種が同じ台数であるが、車種によって可変にする 
        
        car_info_list.append((lp, dp, amount))
        
    return car_info_list


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
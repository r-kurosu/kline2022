import random
import math

def get_edge_direction(edge_list):
    a = []
    for edge in edge_list:
        if edge[0] == edge[1] + 1 or edge[0] == edge[1] - 1:
            a.append(1)
        else:
            a.append(0)
            
    return 0

    
def get_ramp_brock(a, b):
    enter_block = math.floor(b/2)
    exit_block = enter_block + 1 

    return enter_block, exit_block


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
    enter_block, exit_block = get_ramp_brock(a, b)
    
    for edge in edge_list:
        if edge[1] == enter_block:
            edge_list = [e for e in edge_list if e != edge]
            
        if edge[0] == exit_block:
            edge_list = [e for e in edge_list if e != edge]
    # print(edge_list)
    
    return edge_list


def generate_car(m, total_amount, port_list):
    car_info_list = []
    
    for _ in range(m):
        # LPは前半の半分から、DPは後半の半分からランダムに選択する
        lp = random.choice(port_list[:math.floor(len(port_list)/2)])
        dp = random.choice(port_list[math.floor(len(port_list)/2):])
        amount = math.floor(total_amount / m) # TODO:今は全ての車種が同じ台数であるが、車種によって可変にする 
        
        car_info_list.append((lp, dp, amount))
        
    return car_info_list


def output_dat_file(a,b,m,total_amount,block_capacity,LP_list, DP_list, Edge_list):
    LP_list.append(port_list[0]-1)
    DP_list.append(port_list[-1]+1)
    
    LP_list = [str(i) for i in LP_list]
    DP_list = [str(i) for i in DP_list]
    
    block_capacity_list = [block_capacity]*(a*b)
    enter_block, exit_block = get_ramp_brock(a, b)
    block_capacity_list[enter_block] = 0
    block_capacity_list[exit_block] = 0
    
    outfile = open('sample_data.dat', 'w')

    outfile.write(f'# m n\n')
    outfile.write(f'{m} {a*b}\n')
    outfile.write(f'# p\n')
    outfile.write(f'{(str(total_amount//(m)) + " ")*(m)}\n')
    outfile.write(f'# o (last one for m+1)\n')
    outfile.write(f'{" ".join(LP_list)}\n')
    outfile.write(f'# d (last one for m+1)\n')
    outfile.write(f'{" ".join(DP_list)}\n')
    outfile.write(f'# q\n')
    outfile.write(f'{" ".join([str(cap) for cap in block_capacity_list])}\n')
    outfile.write(f'# E (first line is the size of E)\n')
    outfile.write(f'{len(Edge_list)}\n')
    for edge in Edge_list:
        outfile.write(f'{edge[0]} {edge[1]}\n')
        
    return


def input_check(a, b, m, T):
    if m*(math.ceil(math.floor(T/m) / math.ceil(T/a*b-1))) > a*b-1:
        return False
    
    return True


port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9] # input port list

def main(a, b, m, total_amount):
    if input_check(a, b, m, total_amount) == False:
        print("input error")
        print("please check input")
        # return
    else:
        print("input OK")
        
    edge_list = generate_block(a, b)
    car_info_list = generate_car(m, total_amount, port_list)
    block_capacity = math.ceil(total_amount / (a * b - 2))

    output_dat_file(a,b,m,total_amount,block_capacity,[i[0] for i in car_info_list], [i[1] for i in car_info_list], edge_list)
    
    return

## 基本的にここから実行することはない（auto_execution.pyから実行する）
# if __name__ == "__main__":
#     a = 5 # input row of brock
#     b = 6 # input column of brock
#     m = 4 # input number of car kinds
#     total_amount = 120 # input total amount of car
    
#     main(a, b, m, total_amount)
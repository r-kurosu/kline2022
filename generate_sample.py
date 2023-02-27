import random
import math


def get_ramp_brock(a, b):
    if b % 2 == 0:
        return int(b/2)
    else:
        return math.floor(b/2)


def generate_block(a, b):
    num_edge = a*(b-1) + b*(a-1) + 1
    ramp_block = get_ramp_brock(a, b)
    
    edge_list = []
    for i in range(a):
        for j in range(b-1):
            if i*b+j >= ramp_block:
                edge_list.append((i*b+j, i*b+j+1)) # NOTE: fix 1/20 12:30
            else:
                edge_list.append((i*b+j+1, i*b+j))
    
    for i in range(a-1):
        for j in range(b):
            edge_list.append((i*b+j, i*b+j+b)) # NOTE: fix 1/20 12:30
    
    return num_edge, edge_list


def generate_car(m, total_amount, port_list):
    car_info_list = []
    
    for _ in range(m):
        # 最後から1つ前までの要素をランダムに選択
        lp = random.choice(port_list[:-1])
        while True:
            dp = random.choice(port_list)
            if lp < dp:
                break
        amount = total_amount // m # TODO:車種によって可変にする 
        
        car_info_list.append((lp, dp, amount))
        
    return car_info_list


def output_dat_file(a,b,m,total_amount,block_capacity,LP_list, DP_list, num_edge, Edge_list):
    LP_list.append(port_list[0]-1)
    DP_list.append(port_list[-1]+1)
    
    LP_list = [str(i) for i in LP_list]
    DP_list = [str(i) for i in DP_list]
    
    block_capacity_list = [block_capacity]*(a*b)
    ramp_block = get_ramp_brock(a, b)
    block_capacity_list[ramp_block] = 0
    
    outfile = open('sample_data.dat', 'w')

    outfile.write(f'# m n\n')
    outfile.write(f'{m} {a*b-1}\n')
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
        return
    else:
        print("input OK")
        
    num_edge, edge_list = generate_block(a, b)
    car_info_list = generate_car(m, total_amount, port_list)
    block_capacity = math.ceil(total_amount / (a * b - 1))
    
    # print(f"num_block: {num_brock}")
    # print(f"num_edge: {num_edge}")
    # print(f"block_capcity: {block_capacity}")
    # print(f"edge_list: {edge_list}")
    # print(f"car_info_list(LP, DP, amount): {car_info_list}")

    output_dat_file(a,b,m,total_amount,block_capacity,[i[0] for i in car_info_list], [i[1] for i in car_info_list], num_edge, edge_list)
    
    return

## 基本的にここから実行することはない（auto_execution.pyから実行する）
# if __name__ == "__main__":
#     a = 5 # input row of brock
#     b = 6 # input column of brock
#     m = 4 # input number of car
#     total_amount = 120 # input total amount of car
    
#     main(a, b, m, total_amount)
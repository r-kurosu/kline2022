import random
import math

def generate_block(a, b):
    num_block = a*b - 1
    
    num_edge = a*(b-1) + b*(a-1) + 1
    
    edge_list = []
    for i in range(a):
        for j in range(b-1):
            edge_list.append((i*a+j, i*a+j+1)) 
    
    for i in range(a-1):
        for j in range(b):
            edge_list.append((i*a+j, (i+1)*a+j))
            
    return num_block, num_edge, edge_list


def generate_car(m, total_amount, port_list):
    car_info_list = []
    
    for idx in range(m):
        # 最後から1つ前までの要素をランダムに選択
        lp = random.choice(port_list[:-1])
        while True:
            dp = random.choice(port_list)
            if lp < dp:
                break
        amount = total_amount // m
        
        car_info_list.append((lp, dp, amount))
        
    return car_info_list


def main():
    a = 5 # input row of block
    b = 5 # input column of block
    m = 4 # input number of car
    total_amount = 120 # input total amount of car
    port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9] # input port list
    block_capcity = math.ceil(total_amount / (a * b - 1))
    
    num_brock, num_edge, edge_list = generate_block(a, b)
    car_info_list = generate_car(m, total_amount, port_list)
    
    print(f"num_block: {num_brock}")
    print(f"num_edge: {num_edge}")
    print(f"block_capcity: {block_capcity}")
    print(f"edge_list: {edge_list}")
    print(f"car_info_list(LP, DP, amount): {car_info_list}")

    return


main()
import random

def generate_brock(a, b):
    num_brock = a*b
    
    num_edge = a*(b-1) + b*(a-1)
    
    edge_list = []
    for i in range(a):
        for j in range(b-1):
            edge_list.append((i*b+j, i*b+j+1)) # NOTE: fix 1/20 12:30
    
    for i in range(a-1):
        for j in range(b):
            edge_list.append((i*b+j, i*b+j+b)) # NOTE: fix 1/20 12:30
            
    return num_brock, num_edge, edge_list


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


def output_dat_file(a,b,m,total_amount,LP_list, DP_list, num_edge, Edge_list):
    LP_list.append(port_list[0])
    DP_list.append(port_list[-1])
    
    LP_list = [str(i) for i in LP_list]
    DP_list = [str(i) for i in DP_list]
    
    outfile = open('sample_data.dat', 'w')

    outfile.write(f'# m n\n')
    outfile.write(f'{m} {a*b-1}\n')
    outfile.write(f'# p\n')
    outfile.write(f'{(str(total_amount//(m-1)) + " ")*(m-1)}\n')
    outfile.write(f'# o (last one for m+1)\n')
    outfile.write(f'{" ".join(LP_list)}\n')
    outfile.write(f'# d (last one for m+1)\n')
    outfile.write(f'{" ".join(DP_list)}\n')
    outfile.write(f'# q\n')
    outfile.write(f'{(str(total_amount//(a*b))+" ")*(a*b)}\n')
    outfile.write(f'# E (first line is the size of E)\n')
    outfile.write(f'{num_edge}\n')
    for edge in Edge_list:
        outfile.write(f'{edge[0]} {edge[1]}\n')
        
    return


port_list = [1, 2, 3, 4, 5, 6, 7, 8, 9] # input port list
def main():
    a = 5 # input row of brock
    b = 5 # input column of brock
    m = 4 # input number of car
    total_amount = 120 # input total amount of car
    
    num_brock, num_edge, edge_list = generate_brock(a, b)
    car_info_list = generate_car(m, total_amount, port_list)
    
    print(f"num_brock: {num_brock}")
    print(f"num_edge: {num_edge}")
    print(f"edge_list: {edge_list}")
    print(f"car_info_list: {car_info_list}")

    output_dat_file(a,b,m,total_amount,[i[0] for i in car_info_list], [i[1] for i in car_info_list], num_edge, edge_list)
    
    return


main()
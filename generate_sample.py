
def generate_brock(a, b):
    num_brock = a*b
    
    num_edge = a*(b-1) + b*(a-1)
    
    edge_list = []
    for i in range(a):
        for j in range(b-1):
            edge_list.append((i*a+j, i*a+j+1))
    
    for i in range(a-1):
        for j in range(b):
            edge_list.append((i*a+j, (i+1)*a+j))
            
    return num_brock, num_edge, edge_list


def main():
    a = 5 # input row of brock (a >= 2)
    b = 5 # input column of brock (b >= 2)
    
    num_brock, num_edge, edge_list = generate_brock(a, b)
    
    print(f"num_brock: {num_brock}")
    print(f"num_edge: {num_edge}")
    print(f"edge_list: {edge_list}")
    
    return

main()
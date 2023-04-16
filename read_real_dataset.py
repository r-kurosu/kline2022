import pandas as pd
import MASTER
import make_instance_tool


def read_dataset():
    df = pd.read_csv('datasets/BRA_12dk.csv', sep=',')
    print(df)
    input_a = MASTER.input_a
    input_b = MASTER.input_b
    
    input_m = df['車種番号'].max()
    input_total_amount = df['面積'].sum()
    
    return input_data(df, input_a, input_b, input_m, input_total_amount)


def input_data(df, input_a, input_b, input_m, input_total_amount):
    # ブロック
    V_p = [i for i in range(input_a * input_b)]
    enter_block, exit_block = make_instance_tool.get_ramp_block(input_a, input_b)
    V = [i for i in V_p if i != enter_block and i != exit_block]
    q = [(input_total_amount + MASTER.gap_area) / (input_a * input_b -2) for _ in range(input_a * input_b)]
    q[enter_block] = 0
    q[exit_block] = 1
    q = fix_block_area(q, input_a, input_b) # ブロックの面積を実際の　船に合わせて調整する
    
    # 車
    M = [i for i in range(input_m)]
    M_p = [i for i in range(input_m + 1)]
    o, d = get_port_list(df, input_m)
    p = [df['車種番号'][i] for i in range(input_m)]
    o_max = max(o)
    d_max = max(d)
    lp_dummy = df['上の階層に行く車種積み地の最大値'].max()
    dp_dummy = df['上の階層に行く車種上げ地の最小値']
    o.append(lp_dummy)
    d.append(dp_dummy)
    
    #枝について
    E = make_instance_tool.generate_block(input_a, input_b)
    E_bar = [(j,i) for (i,j) in E]
    a = make_instance_tool.get_block_direction(E, input_b)
    a_bar = make_instance_tool.get_block_direction(E_bar, input_b)
    
    return V, V_p, M, M_p, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar


def fix_block_area(q, a, b):
    # 1. 左下の面積を0にする
    q[(a-1)*b] = 0
    
    # 2. 左上・右上・右下の面積を半分にする
    q[0] = q[0] / 2
    q[b-1] = q[b-1] / 2
    q[a*b-1] = q[a*b-1] / 2
    
    # 3. TODO: 他のブロックの面積を調整する
    
    return q

def get_port_list(df, input_m):
    LP_max = df['積み地'].max()
    LP_max = max(LP_max, df['上の階層に行く車種積み地の最大値'].max())
    o = [df['積み地'][i] for i in range(input_m)]
    d = [df['揚げ地'][i] + LP_max for i in range(input_m)]
    
    return o, d


if __name__ == '__main__':
    read_dataset()
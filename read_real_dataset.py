import pandas as pd
import MASTER
import make_instance_tool


def read_dataset():
    try:
        df = pd.read_csv(f'datasets/{MASTER.input_property}_6-11dk/{MASTER.input_property}_{MASTER.input_DK}dk.csv', sep=',')
    except FileNotFoundError:
        print('FileNotFoundError: Please check the file name or input dk.')
        exit()
        
    print(df)
    input_a = MASTER.input_a
    input_b = MASTER.input_b
    
    input_m = df['車種番号'].max() + 1
    input_total_amount = df['合計RT'].sum()
    
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
    p = [df[df['車種番号'] == k]['合計RT'].sum() for k in range(input_m)]
    o_max = max(o)
    d_max = max(d)
    lp_dummy = df['上の階層に行く車種積み地の最大値'].max()
    dp_dummy = df['上の階層に行く車種上げ地の最小値'].max() + df['積み地'].max()
    o.append(lp_dummy)
    d.append(dp_dummy)
    M_same = df[df['ギャングの好み'] == 1]['車種番号'].unique()
    M_reverse = df[df['ギャングの好み'] == -1]['車種番号'].unique()
    r = get_hold_amount_for_each_car(df, input_m)
    M_h = [df[df['ホールド'] == h+1]['車種番号'].unique().tolist() for h in range(4)]
    M_h_bar = [[x for x in M if x not in M_h[h]] for h in range(4)]
    
    #枝について
    E = make_instance_tool.generate_block(input_a, input_b)
    E_bar = [(j,i) for (i,j) in E]
    a = make_instance_tool.get_block_direction(E, input_b)
    a_bar = make_instance_tool.get_block_direction(E_bar, input_b)
    
    return V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar


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

def get_hold_amount_for_each_car(df, input_m):
    r = [[0 for i in range(4)] for j in range(input_m)]
    for k in range(input_m):
        for h in range(4):
            try:
                # 車種番号がkで，ホールドがhの時の面積を取得
                r[k][h] = df[(df['車種番号'] == k) & (df['ホールド'] == h+1)]['合計RT'].values[0]
            except:
                r[k][h] = 0
    return r

if __name__ == '__main__':
    V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar = read_dataset()
    print(M_h_bar, type(M_h_bar[0]))
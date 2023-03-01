import pandas as pd
import numpy as np
import gurobipy as gp

#TODO: add gurobi path ?)

# define constants----------------------------------------------
df_car = pd.read_csv('sample_car_data.csv')
n = len(df_car)
lp = df_car['lp'].to_list()
dp = df_car['dp'].to_list()

# TODO: ブロックに関する情報はどうやって入手する？
m = 10
V = [0]*m
q = [0]*m

E = [[]] # TODO: 隣接行列、接続行列、隣接リストなど
delta_p = [0] * m #TODO: Eを用いて生成（隣接リスト？）
delta_m = [0] * m

o_max = max(lp)
d_max = max(dp)

y_0_p, y_0_p = o_max, o_max
z_0_p, z_0_m = 1,1
# --------------------------------------------------------------

def case1():
    # モデル定義
    model = gp.Model('case1')
    
    # NOTE: 二次元配列の初期化, 行と列が逆かも。。。
    
    # 変数定義
    x = [0 for i in range(n)]*m 
    alfa = [0 for i in range(n)]*m # 一旦、n*mのリストとして定義
    beta = [0 for i in range(n)]*m
    for i in range(n):
        for j in range(m):
            x[i][j] = model.addVar(vtype=gp.GRB.BINARY, name=f'x_{i}_{j}')
            alfa[i][j] = model.addVar(vtype=gp.GRB.BINARY, name=f'alfa_{i}_{j}')
            beta[i][j] = model.addVar(vtype=gp.GRB.BINARY, name=f'beta_{i}_{j}')

    y_p = [0] * m # y^+
    y_m = [0] * m # y^-
    z_p = [0] * m
    z_m = [0] * m
    for j in range(m):
        y_p[i] = model.addVar(vtype=gp.GRB.CONTINUOUS, name=f'y_p_{j}')
        y_m[i] = model.addVar(vtype=gp.GRB.CONTINUOUS, name=f'y_m_{j}')
        z_p[i] = model.addVar(vtype=gp.GRB.CONTINUOUS, name=f'z_p_{j}')
        z_m[i] = model.addVar(vtype=gp.GRB.CONTINUOUS, name=f'z_m_{j}')
        
    gamma = model.addVar(vtype=gp.GRB.CONTINUOUS, name=f'gamma')
    
    # 目的関数
    model.setObjective(gamma, gp.GRB.MINIMIZE)
    
    # 制約条件 (数字は原稿の行数) 
    const1 = [0] * m
    const2 = [0] * m
    const3 = [0] * m
    for i in range(m):
        const1[i] = model.addConstr(gamma>y_p[i]-y_m[i]) # >は禁止なはず、微少量入れて>=に変更する
        const2[i] = model.addConstr(gamma>z_p[i]-z_m[i])
        const3[i] = model.addConstr(gp.quicksum(x[i][j] for j in range(n)) <= q[i])
    
    const4 = [0] * n
    for i in range(n):
        const4[i] = model.addConstr(gp.quicksum(x[i][j] for j in range(m)) >= 1)
    
    const5 = [0 for i in range(n)] * m
    const6 = [0 for i in range(n)] * m
    const7 = [0 for i in range(n)] * m
    const8 = [0 for i in range(n)] * m
    for i in range(m):
        for j in range(n):
            const5[i][j] = model.addConstr(y_p[i] >= lp[j] * x[i][j] - o_max*(1 - x[i][j]))
            const6[i][j] = model.addConstr(y_m[i] <= lp[j] * x[i][j] + o_max*(1 - x[i][j]))
            const7[i][j] = model.addConstr(z_p[i] >= dp[j] * x[i][j] - o_max*(1 - x[i][j]))
            const8[i][j] = model.addConstr(z_m[i] <= dp[j] * x[i][j] + o_max*(1 - x[i][j]))
    
    const9 = [0 for i in range(m)] * m # 一旦、m*mのリストとして定義→必要なセルだけ制約として使う
    for i in range(m):
        for j in range(m):
            if j in delta_p[i]:
                const9[i][j] = model.addConstr(y_p[i] <= y_m[j] + (1-alfa[i][j])*o_max)
    
    const10 = [0]*m
    for i in range(m):
        const10[i] = model.addConstr(gp.quicksum(alfa[i][j] for j in delta_p) >= 1)
    
    const11 = [0 for i in range(m)] * m 
    for i in range(m):
        for j in delta_p:
            const11[i][j] = model.addConstr(z_p[i] >= z_m[j] + (1-beta[i][j])*d_max)
    
    const12 = [0]*m
    for i in range(m):
        const12[i] = model.addConstr(gp.quicksum(beta[i][j] for j in delta_p) >= 1)
        
    #13,14,15行目の制約に関しては、変数定義で済ます
    
    return

def main():
    case1()
    return

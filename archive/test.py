import gurobipy as gp
import sys
import auto_excution
import generate_sample


def main():
    with open("sample_data.dat", 'r') as f:
    # with open("small.dat", 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    lines = [line for line in lines if line[0] != '#']
    items = lines.pop(0).split(' ')
    m, n = int(items[0]),  int(items[1])
    M = {i for i in range(1,m+1)}
    M_p = {i for i in range(1,m+2)}
    V = {i for i in range(0,n+1)} # NOTE: 1/23 fixed by Kurosu
    V_p = {i for i in range(0,n+2)}
    items = lines.pop(0).split(' ')
    p = {i+1: int(v) for i, v in enumerate(items)}
    items = lines.pop(0).split(' ')
    o = {i+1: int(v) for i, v in enumerate(items)}
    items = lines.pop(0).split(' ')
    d = {i+1: int(v) for i, v in enumerate(items)}
    items = lines.pop(0).split(' ')
    q = {i: int(v) for i, v in enumerate(items)} # NOTE: 1/23 fixed by Kurosu
    q[n+1] = 1
    n_E =  int(lines.pop(0))
    E, E_b = set(), set()
    for i in range(n_E):
        items = lines.pop(0).split(' ')
        E.add((int(items[0]), int(items[1]),))
        E_b.add((int(items[1]), int(items[0]),))
    
    q_sum = sum(q.values())
    d_max, o_max = max(d), max(o)

    # ランプブロックの取得
    a, b = auto_excution.a, auto_excution.b
    ramp_block = generate_sample.get_ramp_brock(a, b)
    
    model = gp.Model('assignment')
    # print(f"V={V}, M={M}, p={p}, q={q}")
    x = {(i,k): model.addVar(vtype = gp.GRB.BINARY, name = "x[{},{}]".format(i,k)) for i in V for k in M}
    x.update({(n+1,k): 0 for k in M})
    x.update({(i,m+1): 0 for i in V})
    x[n+1,m+1] = 1
    alpha = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "a[{},{}]".format(i,j)) for (i,j) in E}
    beta = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "b[{},{}]".format(i,j)) for (i,j) in E_b}
    model.update()

    # 目標関数


    # 制約関数
    model.addConstrs((gp.quicksum(q[i] * x[i,k] for i in V-{ramp_block}) >= p[k] for k in M), name="(34)")
    model.addConstrs((gp.quicksum(x[i,k] for k in M) == 1 for i in V-{ramp_block}), name="(35)")
    model.addConstrs((gp.quicksum(o[k] * x[j,k] for k in M_p) <= gp.quicksum(o[k] * x[i,k] for k in M_p) + o_max * (1-alpha[i,j]) 
                                    for (i,j) in E if i != ramp_block), name="(36)")
    model.addConstrs((gp.quicksum(d[k] * x[j,k] for k in M_p) <= gp.quicksum(d[k] * x[i,k] for k in M_p) + d_max * (1-beta[i,j])
                                    for (i,j) in E_b if j != ramp_block), name="(37)")
    model.addConstrs((gp.quicksum(alpha[j,i] for j in V_p if (j,i) in E) == 1 for i in V-{ramp_block} | {n+1}), name="(38a)")
    model.addConstrs((gp.quicksum(beta[i,j] for j in V_p if (i,j) in E_b) == 1 for i in V^{ramp_block} | {n+1}), name="(38b)")

    # TBD
    # 1.向きの対応
    # 2.高さ制限の対応
    # 3.元のグラフに閉路が存在する場合，さらに部分巡回路を排除する制約の追加が必要
    model.params.LogToConsole = False #NOTE: これをTrueにすると，Gurobiの出力がコンソールに出力される
    
    model.optimize()

    if model.status == gp.GRB.OPTIMAL:
        print("Tree model is solved!!!")
        
        # (ブロック: 車種)
        sol = {i: k for i,k in x if isinstance(x[i,k], gp.Var) and  x[i,k].X > 0.5}
        print("sol = ", sol)

        # 有向辺の集合 (LP)
        sola = {(i,k) for i,k in alpha if isinstance(alpha[i,k], gp.Var) and  alpha[i,k].X > 0.5}
        # print(sola)
        
        # 有向辺の集合（DP）
        solb = {(i,k) for i,k in beta if isinstance(beta[i,k], gp.Var) and  beta[i,k].X > 0.5}
        # print(solb)
        #print(o[m+1])
    else:
        print("Tree model is infeasible")
        return None, None, None
        
    return sol, sola, solb


if __name__ == '__main__':
    sol, sola, solb = main()
    
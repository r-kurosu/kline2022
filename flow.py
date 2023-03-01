import gurobipy as gp
import sys
import archive.auto_excution as auto_excution
import generate_sample


def main():
    with open("sample_data.dat", 'r') as f:
    # with open("small.dat", 'r') as f:
        lines = [line.rstrip() for line in f.readlines()]
    lines = [line for line in lines if line[0] != '#']
    items = lines.pop(0).split(' ')
    m, n = int(items[0]),  int(items[1])
    M = {i for i in range(1,m+1)}
    M_p = {i for i in range(1,m+2)} # TODO: M'は今はいらないかも
    V = {i for i in range(n)} #全部含む（出口と入口も含む）
    # V_p = {i for i in range(0,n+2)}
    items = lines.pop(0).split(' ')
    p = {i+1: int(v) for i, v in enumerate(items)}
    p[m+1] = 1
    items = lines.pop(0).split(' ')
    o = {i+1: int(v) for i, v in enumerate(items)}
    items = lines.pop(0).split(' ')
    d = {i+1: int(v) for i, v in enumerate(items)}
    items = lines.pop(0).split(' ')
    q = {i: int(v) for i, v in enumerate(items)}
    # q[n+1] = 1
    n_E =  int(lines.pop(0))
    E, E_b = set(), set()
    for i in range(n_E):
        items = lines.pop(0).split(' ')
        E.add((int(items[0]), int(items[1]),))
        E_b.add((int(items[1]), int(items[0]),))
        
    q_sum = sum(q.values())
    d_max, o_max = max(d), max(o)

    # ランプブロックの取得
    input_a, input_b = auto_excution.a, auto_excution.b
    enter_block, exit_block = generate_sample.get_ramp_brock(input_a, input_b)
    
    model = gp.Model('assignment')
    x = {(i,k): model.addVar(vtype = gp.GRB.BINARY, name = "x[{},{}]".format(i,k)) for i in V for k in M}
    # x.update({(n+1,k): 0 for k in M})
    # x.update({(i,m+1): 0 for i in V})
    # x[n+1,m+1] = 1
    alpha = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "a[{},{}]".format(i,j)) for (i,j) in E}
    beta = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "b[{},{}]".format(i,j)) for (i,j) in E_b}

    u = {(i,j): model.addVar(vtype = gp.GRB.CONTINUOUS, lb = 0, name = "u[{},{}]".format(i,j)) for (i,j) in E}
    v = {(i,j): model.addVar(vtype = gp.GRB.CONTINUOUS, lb = 0, name = "v[{},{}]".format(i,j)) for (i,j) in E_b}
    model.update()

    # 目標関数


    # 制約関数
    model.addConstrs((gp.quicksum(q[i] * x[i,k] for i in V) >= p[k] for k in M), name="(18)") #NOTE: ここでランプブロックの容量は0なので、除外しなくても良い
    
    model.addConstrs((gp.quicksum(x[i,k] for k in M) == 1 for i in V-{enter_block, exit_block}), name="(19)")
    
    # TODO: ここなんか違う気がする
    # model.addConstrs((gp.quicksum(o[k] * x[j,k] for k in M_p) <= gp.quicksum(o[k] * x[i,k] for k in M_p) + o_max * (1-alpha[i,j]) for (i,j) in E if i != enter_block), name="(20)")
    # 20の代替案
    for edge in E:
        if edge[0] != enter_block:
            model.addConstr((gp.quicksum(o[k] * x[edge[1],k] for k in M) <= gp.quicksum(o[k] * x[edge[0],k] for k in M) + (1-alpha[edge[0],edge[1]])*o_max), name="(20)")
            # NOTE: M'ではなくMで良いのでは？
            
    # TODO: ここなんか違う気がする
    # model.addConstrs((gp.quicksum(d[k] * x[j,k] for k in M_p) <= gp.quicksum(d[k] * x[i,k] for k in M_p) + d_max * (1-beta[i,j]) for (i,j) in E_b if j != enter_block), name="(21)")
    # 21の代替案
    for edge in E_b:
        if edge[1] != enter_block:
            model.addConstr((gp.quicksum(d[k] * x[edge[1],k] for k in M) >= gp.quicksum(d[k] * x[edge[0],k] for k in M) - (1-beta[edge[0],edge[1]])*d_max), name="(21)")
            
    # TODO: ここなんか違う気がする
    # model.addConstrs((gp.quicksum(u[edge[0], edge[1]] for edge in E) - gp.quicksum(u[edge[0],edge[1]] for edge in E) == gp.quicksum(q[i] * x[i,k] for k in M_p) for i in V | {exit_block}), name = "(22)")
    # 22の代替案
    for i in V:
        model.addConstr((gp.quicksum(u[j, i] for j in V if (j, i) in E) - gp.quicksum(u[i, j] for j in V if (i, j) in E) == gp.quicksum(q[i] * x[i, k] for k in M)), name = "(22)")
        
    model.addConstr((gp.quicksum(u[enter_block, j] for j in V if (enter_block, j) in E) == gp.quicksum(p[k] for k in M)), name = "(23)") 
    
    #TODO: ここなんか違う気がする
    # model.addConstrs((gp.quicksum(v[i,j] for j in V_p if (i,j) in E_b) - gp.quicksum(v[j,i] for j in V_p if (j,i) in E_b) == gp.quicksum(q[i] * x[i,k]for k in M_p) for i in V-{ramp_block} | {n+1}), name = "(24)")
    # 24の代替案
    for i in V:
        if i != exit_block:
            model.addConstr((gp.quicksum(v[i, j] for j in V if (i, j) in E_b) - gp.quicksum(v[j, i] for j in V if (j, i) in E_b) == gp.quicksum(q[i] * x[i, k] for k in M)), name = "(24)")
    
    model.addConstr((gp.quicksum(v[i, enter_block] for i in V if (i, enter_block) in E_b) == gp.quicksum(p[k] for k in M)), name = "(25)")

    model.addConstrs((u[j,i] <= q_sum * alpha[j,i] for (j,i) in E), name = "(26b)")

    model.addConstrs((v[i,j] <= q_sum * beta[i,j] for (i,j) in E_b), name = "(27b)")
    
    #TODO: ここなんか違う気がする (for文で書く必要がある気がする)
    # model.addConstrs((gp.quicksum(alpha[j,i] for j in V_p if (j,i) in E) == 1 for i in V-{ramp_block} | {n+1}), name="(28a)")
    # model.addConstrs((gp.quicksum(beta[i,j] for j in V_p if (i,j) in E_b) == 1 for i in V-{ramp_block} | {n+1}), name="(28b)")
    # 28の代替案 (29の追加)
    for i in V:
        if i != exit_block:
            model.addConstr((gp.quicksum(alpha[j, i] for j in V if (j, i) in E) == 1), name = "(28a)")
            model.addConstr((gp.quicksum(beta[i, j] for j in V if (i, j) in E_b) == 1), name = "(28b)")
            
            # TODO: 29の追加
            # model.addConstr((gp.quicksum(a[j, i]*alpha[j, i] for j in V if (j, i) in E) == gp.quicksum(a[i,j]*beta[i, j] for j in V if (i, j) in E_b)), name = "(29)") 

    # TBD
    # 1.向きの対応
    # 2.高さ制限の対応
    # 3.元のグラフに閉路が存在する場合，さらに部分巡回路を排除する制約の追加が必要

    model.update()
    # model.write("a.lp")
    model.params.LogToConsole = False #NOTE: これをTrueにすると，Gurobiの出力がコンソールに出力される
    model.optimize()
    # print("Optimal status:", model.status)
    # model.write("solution.sol")

    #if model.status == gp.GRB.OPTIMAL:
    #    model.printAttr('x')
    #if model.solCount == 0:
        #print("Model is infeasible")
        #model.computeIIS()
        #model.write("model_iis.ilp")

    if model.status == gp.GRB.OPTIMAL:
        print("Flow model is solved!!!")
        sol = {i: k for i,k in x if isinstance(x[i,k], gp.Var) and  x[i,k].X > 0.5}
        print("sol =", sol)

        sola = {(i,k) for i,k in alpha if isinstance(alpha[i,k], gp.Var) and  alpha[i,k].X > 0.5}
        print("sol a =", sola)
        
        solb = {(i,k) for i,k in beta if isinstance(beta[i,k], gp.Var) and  beta[i,k].X > 0.5}
        print("sol b =", solb)
        
        return sol, sola, solb
    
    else:
        print("Flow model is infeasible")
        return None, None, None


if __name__ == '__main__':
    main()
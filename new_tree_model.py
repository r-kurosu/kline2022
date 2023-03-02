import gurobipy as gp
import sys
import random, math
import make_instance_tool
import new_visualize_tool
import MASTER


def input_data(input_a, input_b, input_m, input_total_amount):
    # ブロック
    V_p = [i for i in range(input_a * input_b)]
    enter_block, exit_block = make_instance_tool.get_ramp_block(input_a, input_b)
    V = [i for i in V_p if i != enter_block and i != exit_block]
    q = [input_total_amount // (input_a * input_b -2) + 1 for _ in range(input_a * input_b)]
    q[enter_block] = 0
    q[exit_block] = 1
    # print(q)
    
    # 車の情報
    M = [i for i in range(input_m)]
    M_p = [i for i in range(input_m + 1)]
    
    port_list = MASTER.PORT_list
    car_info_list = make_instance_tool.generate_car(input_m, input_total_amount, port_list)
    o = [car_info[0] for car_info in car_info_list]
    d = [car_info[1] for car_info in car_info_list]
    p = [car_info[2] for car_info in car_info_list]
    o_max = max(o)
    d_max = max(d) 
    lp_dummy, dp_dummy = make_instance_tool.generate_dummy_car(port_list)
    o.append(lp_dummy)
    d.append(dp_dummy)
    
    # 枝
    E = make_instance_tool.generate_block(input_a, input_b)
    E_bar = [(j,i) for (i,j) in E]
    
    # a
    a = [] #TODO: ここでaを作成する
    
    return V, V_p, M, M_p, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a


def solve_tree_model(V, V_p, M, M_p, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a):
    model = gp.Model('tree_model')
    
    # 変数定義
    x = {(i,k): model.addVar(vtype = gp.GRB.BINARY, name = f"x_{i}_{k}]") for i in V for k in M}
    alpha = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = f"a[{i},{j}]") for (i,j) in E}
    beta = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = f"b[{i},{j}]") for (i,j) in E_bar}
        
    # 定数固定
    #NOTE: ここで一部の変数を固定する
    x.update({(exit_block, k): 0 for k in M})
    x.update({(i,len(M)): 0 for i in V})
    x[exit_block, len(M)] = 1
    
    # 目的関数

    # 制約条件
    # 制約34
    for k in M:
        model.addConstr((gp.quicksum(q[i] * x[i,k] for i in V) >= p[k]), name=f"34_{k}")
    
    # 制約35
    for i in V:
        model.addConstr((gp.quicksum(x[i,k] for k in M) == 1), name=f"35_{i}")
    
    # 制約36
    for edge in E:
        i = edge[0]
        j = edge[1]
        if i != enter_block:
            model.addConstr(gp.quicksum(x[j,k]*o[k] for k in M_p) <= gp.quicksum(x[i,k]*o[k] for k in M_p) + (1-alpha[i,j])*o_max, name=f"36_{i}_{j}")
    
    # 制約37
    for edge in E_bar:
        i = edge[0]
        j = edge[1]
        if j != enter_block:
            model.addConstr(gp.quicksum(x[j,k]*d[k] for k in M_p) <= gp.quicksum(x[i,k]*d[k] for k in M_p) + (1-beta[i,j])*d_max, name=f"37_{i}_{j}")
    
    
    # 制約38
    for i in V + [exit_block]:
        edge_list = [j for j in V_p if (j,i) in E]
        model.addConstr(gp.quicksum(alpha[j,i] for j in edge_list) == 1, name=f"38a_{i}")
        edge_list_bar = [j for j in V_p if (i,j) in E_bar]
        model.addConstr(gp.quicksum(beta[i,j] for j in edge_list_bar) == 1, name=f"38b_{i}")
    
    # 制約39 TODO: 向き制約を追加する
    # for i in V + {exit_block}:
    #     model.addConstr(gp.quicksum(a[j,i]*alpha[j,i] for j in V if (j,i) in E) == gp.quicksum(a[j,i]*beta[i,j] for j in V if (i,j) in E_bar), name=f"39_{i}")
    
    if MASTER.potential_flag == 1:
        # Potential model
        # 変数定義
        mu = [model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"mu_{i}") for i in V_p]
        nu = [model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"nu_{i}") for i in V_p]
        # mu = [model.addVar(vtype = gp.GRB.CONTINUOUS, lb=0, ub=len(V_p), name = f"mu_{i}") for i in V_p]
        # nu = [model.addVar(vtype = gp.GRB.CONTINUOUS, lb=0, ub=len(V_p), name = f"nu_{i}") for i in V_p]
        mu[enter_block] = 0
        nu[enter_block] = 0
        # 制約条件
        for edge in E:
            i = edge[0]
            j = edge[1]
            if j != enter_block:
                model.addConstr(mu[i] <= mu[j] - 1 + len(V_p) - len(V_p)*alpha[i,j], name=f"potential_mu_{i}_{j}")
        
        for edge in E_bar:
            i = edge[0]
            j = edge[1]
            if i != enter_block:
                model.addConstr(nu[i] >= nu[j] + 1 - len(V_p) + len(V_p)*beta[i,j], name=f"potential_nu_{i}_{j}")

    if MASTER.next_block_flag == 1:
        # Next block model （隣接するブロックに配置する車種を同じにする）
        z = {(i, j, k) : model.addVar(vtype = gp.GRB.BINARY, name = f"z_{i}_{j}_{k}") for i in V_p for j in V_p for k in M}
        for i in V:
            N_i = make_instance_tool.make_Next_block_list(i)
            for j in N_i:
                for k in M:
                    model.addConstr(-z[i,j,k] <= x[i,k] - x[j,k], name=f"constr_l_{i}_{j}_{k}")
                    model.addConstr(z[i,j,k] >= x[i,k] - x[j,k], name=f"constr_r_{i}_{j}_{k}")
        
        model.setObjective(gp.quicksum(z[i,j,k] for i in V_p for j in V_p for k in M), sense=gp.GRB.MINIMIZE)
    
    
    # 求解
    model.update()
    model.params.LogToConsole = False #NOTE: これをTrueにすると，Gurobiの出力がコンソールに出力される
    model.optimize()


    if model.status == gp.GRB.OPTIMAL:
        print("Tree model is solved!!!")
        
        # input情報
        print("input information --------------------")
        print(f"total amount: {sum(p)}")
        print(f"total capacity: {sum(q)}")
        for k in M:
            print(f"car {k}: LP: {o[k]}, DP: {d[k]}, amount: {p[k]}")
        print(f"dummy car: LP: {o[-1]}, DP: {d[-1]}")
        print(f"number of block: {len(V_p)}")
        print(f"capacity of block: {q}")
        
        print("--------------------------------------")
        
        # (ブロック: 車種)
        sol = {i: k for i,k in x if isinstance(x[i,k], gp.Var) and  x[i,k].X > 0.5}
        print("sol (ブロック:車種): ", sol)

        # 有向辺の集合 (LP)
        sola = {(i,k) for i,k in alpha if isinstance(alpha[i,k], gp.Var) and  alpha[i,k].X > 0.5}
        print("sol a: ", sola)
        
        # 有向辺の集合（DP）
        solb = {(i,k) for i,k in beta if isinstance(beta[i,k], gp.Var) and  beta[i,k].X > 0.5}
        print("sol b: ", solb)
    else:
        print("Tree model is infeasible")
        print("input information --------------------")
        print(f"total amount: {sum(p)}")
        print(f"total capacity: {sum(q)}")
        for k in M:
            print(f"car {k}: LP: {o[k]}, DP: {d[k]}, amount: {p[k]}")
        print(f"number of block: {len(V_p)}")
        print(f"capacity of block: {q}")
        return None, None, None
        
    return sol, sola, solb


def main():
    input_a = MASTER.input_a
    input_b = MASTER.input_b
    input_m = MASTER.input_m
    input_total_amount = MASTER.input_total_amount
    
    V, V_p, M, M_p, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a = input_data(input_a, input_b, input_m, input_total_amount)
    sol, sola, solb = solve_tree_model(V, V_p, M, M_p, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a)
    
    if sol is not None:
        new_visualize_tool.visualize_solution(sol, sola, solb, input_a, input_b, len(M), o, d, "new_tree_model")
    
    return


if __name__ == '__main__':
    main()
    
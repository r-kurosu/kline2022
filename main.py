import gurobipy as gp
import sys
import random, math, time
import make_instance_tool
import visualize_tool
import read_real_dataset
import MASTER



def fix_block_area(q):
    a, b = MASTER.input_a, MASTER.input_b
    
    # 1. 左下の面積を0にする
    q[(a-1)*b] = 0
    
    # 2. 左上・右上・右下の面積を半分にする
    q[0] = q[0] / 2
    q[b-1] = q[b-1] / 2
    q[a*b-1] = q[a*b-1] / 2
    
    # 3. TODO: 他のブロックの面積を調整する
    
    return q


def input_data(input_a, input_b, input_m, input_total_amount):
    # ブロック
    V_p = [i for i in range(input_a * input_b)]
    enter_block, exit_block = make_instance_tool.get_ramp_block(input_a, input_b)
    V = [i for i in V_p if i != enter_block and i != exit_block]
    q = [(input_total_amount + MASTER.gap_area) / (input_a * input_b -2) for _ in range(input_a * input_b)]
    q[enter_block] = 0
    q[exit_block] = 1
    q = fix_block_area(q)
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
    M_same, M_reverse, M_description = make_instance_tool.get_gang_preferences(M)
    M_h_bar, Sekwiari_results = make_instance_tool.get_sekiwari_results(M)
    r = make_instance_tool.get_detailed_sekiwari_results(M, p)
    
    # 枝
    E = make_instance_tool.generate_block(input_a, input_b)
    E_bar = [(j,i) for (i,j) in E]
    a = make_instance_tool.get_block_direction(E, input_b)
    a_bar = make_instance_tool.get_block_direction(E_bar, input_b)
    
    return V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar


def solve_tree_model(V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar):
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
    
    
    if MASTER.potential_flag == 1:
        # Potential model
        # 変数定義
        mu = [model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"mu_{i}") for i in V_p]
        nu = [model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"nu_{i}") for i in V_p]
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
    
    # （ペナルティ1）出る向きと入る向きを同じにする
    y = {(i) : model.addVar(vtype = gp.GRB.BINARY, name = f"y_{i}") for i in V}
    for i in V:
        N_i = make_instance_tool.get_Next_block_list(i)
        model.addConstr(-y[i] <= gp.quicksum(a[j,i]*alpha[j,i] for j in N_i) - gp.quicksum(a_bar[i,j]*beta[i,j] for j in N_i), name=f"constr_l_{i}")
        model.addConstr(y[i] >= gp.quicksum(a[j,i]*alpha[j,i] for j in N_i) - gp.quicksum(a_bar[i,j]*beta[i,j] for j in N_i), name=f"constr_r_{i}")
    
    # （ペナルティ3) ギャングの好みを考慮する
    z3 = {(i) : model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"z3_{i}") for i in V}
    for i in V:
        delta = make_instance_tool.get_delta(i, E)
        for j in delta:
            model.addConstr(alpha[j,i]-beta[i,j] <= 1 + z3[i] - gp.quicksum(x[i,k] for k in M_same), name=f"constr_p3_18_{i}_{j}")
            model.addConstr(beta[i,j]-alpha[j,i] <= 1 + z3[i] - gp.quicksum(x[i,k] for k in M_same), name=f"constr_p3_19_{i}_{j}")
            sigma = make_instance_tool.get_sigma(i,j)
            if sigma is not None:
                model.addConstr(alpha[j,i]-beta[i,sigma] <= 1 + z3[i] - gp.quicksum(x[i,k] for k in M_reverse), name=f"constr_p3_20_{i}_{j}")
                model.addConstr(beta[i,sigma]-alpha[j,i] <= 1 + z3[i] - gp.quicksum(x[i,k] for k in M_reverse), name=f"constr_p3_21_{i}_{j}")
            
    # （ペナルティ4）席割りの結果を考慮する
    # 目的関数のみ
    
    
    # （ペナルティ5）隣接するブロックに配置する車種を同じにする
    z = {(i, j, k) : model.addVar(vtype = gp.GRB.BINARY, name = f"z_{i}_{j}_{k}") for i in V_p for j in V_p for k in M}
    for i in V:
        N_i = make_instance_tool.get_Next_block_list(i)
        for j in N_i:
            for k in M:
                model.addConstr(-z[i,j,k] <= x[i,k] - x[j,k], name=f"constr_l_{i}_{j}_{k}")
                model.addConstr(z[i,j,k] >= x[i,k] - x[j,k], name=f"constr_r_{i}_{j}_{k}")
    
    # (ペナルティ6) 席割りの結果を考慮する（改良版）
    Hold_List = make_instance_tool.set_hold()
    y6 = {(h, k) : model.addVar(vtype = gp.GRB.CONTINUOUS, name = f"free_space_{h}_{k}") for h in range(4) for k in M}
    for h in range(4):
        for k in M:
            model.addConstr(y6[h,k] >= 0, name=f"constr6_l_{h}_{k}")
            model.addConstr(y6[h,k] >= gp.quicksum(x[i,k]*q[i] for i in Hold_List[h]) - r[k][h], name=f"constr6_r_{h}_{k}")
            
    # （ペナルティ7）入庫と出庫の複雑さに関するペナルティ（改良版）
    t_a = {(i, j) : model.addVar(vtype = gp.GRB.CONTINUOUS, lb=0, name = f"t_a_{i}_{j}") for (i,j) in E}
    t_b = {(i,j) : model.addVar(vtype = gp.GRB.CONTINUOUS, lb=0, name = f"t_b_{i}_{j}") for (i,j) in E_bar}
    for edge in E:
        i, j = edge[0], edge[1]
        penalty_edges_alpha = make_instance_tool.get_penalty_edges(i, j, E)
        model.addConstr(gp.quicksum(alpha[penalty_e] for penalty_e in penalty_edges_alpha) <= t_a[edge] + len(penalty_edges_alpha)*(1-alpha[edge]), name=f"constr7_1_{i}_{j}")
    for edge in E_bar:
        j, i = edge[0], edge[1]
        penalty_edges_beta = make_instance_tool.get_penalty_edges(j, i, E_bar)
        model.addConstr(gp.quicksum(beta[penalty_e] for penalty_e in penalty_edges_beta) <= t_b[edge] + len(penalty_edges_beta)*(1-beta[edge]), name=f"constr7_2_{i}_{j}")
    
    # 目的関数
    model.setObjective(
        + MASTER.w1*gp.quicksum(y[i] for i in V)
        + MASTER.w2*(gp.quicksum(1-a_bar[edge]*beta[edge] for edge in E_bar))
        + MASTER.w3*gp.quicksum(z3[i] for i in V)
        + MASTER.w4*gp.quicksum(gp.quicksum(x[i,k] for i in Hold_List[h] for k in M_h_bar[h]) for h in range(4))
        + MASTER.w5*gp.quicksum(z[i,j,k] for i in V_p for j in V_p for k in M)
        + MASTER.w6*gp.quicksum(y6[h,k] for h in range(4) for k in M)
        + MASTER.w7*(gp.quicksum(t_a[edge] for edge in E) + gp.quicksum(t_b[edge] for edge in E_bar)),
        sense=gp.GRB.MINIMIZE)

    
    # 求解
    model.setParam("TimeLimit", MASTER.TIME_LIMIT)
    model.setParam("MIPFocus", 1)
    model.update()
    # model.params.LogToConsole = False #NOTE: これをTrueにすると，Gurobiの出力がコンソールに出力される
    model.optimize()


    if model.status != gp.GRB.INFEASIBLE:
        print("Tree model is solved!!!")
        print("Optimal value: ", model.objVal)
        print("status:", model.status)
        # staus: {1: 'LOADED', 2: 'OPTIMAL', 3: 'INFEASIBLE', 4: 'INF_OR_UNBD', 5: 'UNBOUNDED', 6: 'CUTOFF', 7: 'ITERATION_LIMIT', 8: 'NODE_LIMIT', 9: 'TIME_LIMIT', 10: 'SOLUTION_LIMIT', 11: 'INTERRUPTED', 12: 'NUMERIC', 13: 'SUBOPTIMAL', 14: 'INPROGRESS', 15: 'USER_OBJ_LIMIT'}
        if model.objVal >= 10**10:
            print("Not infeasble but No feasible solution has been founded!")
            print("Need more time!")
            return None, None, None
        
        # input情報
        print("input information --------------------")
        print(f"total amount: {sum(p)}")
        print(f"total capacity: {sum(q)}")
        for k in M:
            print(f"car {k}: LP: {o[k]}, DP: {d[k]}, RT: {p[k]}")
        print(f"dummy car: LP: {o[-1]}, DP: {d[-1]}")
        print(f"number of block: {len(V_p)}")
        print(f"capacity of a block: {q[0]}")
        print(f"number of car: {len(M)}")
        
        print(f"w1: {MASTER.w1}")
        print(f"w2: {MASTER.w2}")
        print(f"w3: {MASTER.w3}")
        print(f"w4: {MASTER.w4}")
        print(f"w5: {MASTER.w5}")
        print(f"w6: {MASTER.w6}")
        print(f"w7: {MASTER.w7}")
        print("--------------------------------------")
        
        # solution
        print("solution ------------------------------")
        penalty_sol = [
            sum(y[i].X for i in V),
            sum(1-a_bar[edge]*beta[edge].X for edge in E_bar),
            sum(z3[i].X for i in V),
            sum(sum(x[i,k].X for i in Hold_List[h] for k in M_h_bar[h]) for h in range(4)),
            sum(z[i,j,k].X for i in V_p for j in V_p for k in M),
            sum(y6[h,k].X for h in range(4) for k in M),
            sum(t_a[edge].X for edge in E) + sum(t_b[edge].X for edge in E_bar)
        ]
        for i in range(len(penalty_sol)):
            print(f"penalty {i+1}: {penalty_sol[i]}")
        print("--------------------------------------")
        
        # (ブロック: 車種)
        sol = {i: k for i,k in x if isinstance(x[i,k], gp.Var) and  x[i,k].X > 0.5}
        # print("sol (ブロック:車種): ", sol)

        # 有向辺の集合 (LP)
        sola = {(i,k) for i,k in alpha if isinstance(alpha[i,k], gp.Var) and  alpha[i,k].X > 0.5}
        # print("sol a: ", sola)
        
        # 有向辺の集合（DP）
        solb = {(i,k) for i,k in beta if isinstance(beta[i,k], gp.Var) and  beta[i,k].X > 0.5}
        # print("sol b: ", solb)
    else:
        print("Tree model is infeasible")
        print("input information --------------------")
        print(f"total amount: {sum(p)}")
        print(f"total capacity: {sum(q)}")
        for k in M:
            print(f"car {k}: LP: {o[k]}, DP: {d[k]}, area(RT): {p[k]}")
        print(f"number of block: {len(V_p)}")
        print(f"capacity of a block: {q[0]}")
        return None, None, None, None
        
    return sol, sola, solb, penalty_sol


def main():
    begin_time = time.time()
    input_a = MASTER.input_a
    input_b = MASTER.input_b
    
    if MASTER.USE_REAL_DATA == 0:
        input_m = MASTER.input_m
        input_total_amount = MASTER.input_total_amount
        
        V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar = input_data(input_a, input_b, input_m, input_total_amount)
    else:
        V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar = read_real_dataset.read_dataset()
    
    variables = {
        'V': V,
        'V_p': V_p,
        'M': M,
        'M_p': M_p,
        'M_same': M_same,
        'M_reverse': M_reverse,
        'M_h_bar': M_h_bar,
        'r': r,
        'E': E,
        'E_bar': E_bar,
        'q': q,
        'p': p,
        'o': o,
        'o_max': o_max,
        'd': d,
        'd_max': d_max,
        'enter_block': enter_block,
        'exit_block': exit_block,
        'a': a,
        'a_bar': a_bar,
    }

    # for var_name, var_value in variables.items():
    #     print(f"{var_name}: {var_value}")

    
    sol, sola, solb, penalty_sol = solve_tree_model(V, V_p, M, M_p, M_same, M_reverse, M_h_bar, r, E, E_bar, q, p, o, o_max, d, d_max, enter_block, exit_block, a, a_bar)
    
    if sol is not None:
        visualize_tool.visualize_solution(sol, sola, solb, penalty_sol, input_a, input_b, len(M), o, d, p)
    end_time = time.time()
    print(f"calculation time: {end_time - begin_time} sec")
    
    return


if __name__ == '__main__':
    main()
    
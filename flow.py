import gurobipy as gp


with open("small.dat", 'r') as f:
    lines = [line.rstrip() for line in f.readlines()]
lines = [line for line in lines if line[0] != '#']
items = lines.pop(0).split(' ')
m, n = int(items[0]),  int(items[1])
M = {i for i in range(1,m+1)}
M_p = {i for i in range(1,m+2)}
V = {i for i in range(1,n+1)}
V_p = {i for i in range(0,n+2)}
items = lines.pop(0).split(' ')
p = {i+1: int(v) for i, v in enumerate(items)}
p[m+1] = 1
items = lines.pop(0).split(' ')
o = {i+1: int(v) for i, v in enumerate(items)}
items = lines.pop(0).split(' ')
d = {i+1: int(v) for i, v in enumerate(items)}
items = lines.pop(0).split(' ')
q = {i+1: int(v) for i, v in enumerate(items)}
q[n+1] = 1
n_E =  int(lines.pop(0))
E, E_b = set(), set()
for i in range(n_E):
    items = lines.pop(0).split(' ')
    E.add((int(items[0]), int(items[1]),))
    E_b.add((int(items[1]), int(items[0]),))
    
q_sum = sum(q.values())
d_max, o_max = max(d), max(o)

model = gp.Model('assignment')
x = {(i,k): model.addVar(vtype = gp.GRB.BINARY, name = "x[{},{}]".format(i,k)) for i in V for k in M}
x.update({(n+1,k): 0 for k in M})
x.update({(i,m+1): 0 for i in V})
x[n+1,m+1] = 1
alpha = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "a[{},{}]".format(i,j)) for (i,j) in E}
beta = {(i,j): model.addVar(vtype = gp.GRB.BINARY, name = "b[{},{}]".format(i,j)) for (i,j) in E_b}

u = {(i,j): model.addVar(vtype = gp.GRB.CONTINUOUS, lb = 0, name = "u[{},{}]".format(i,j)) for (i,j) in E}
v = {(i,j): model.addVar(vtype = gp.GRB.CONTINUOUS, lb = 0, name = "v[{},{}]".format(i,j)) for (i,j) in E_b}
model.update()

# 目標関数


# 制約関数
model.addConstrs((gp.quicksum(q[i] * x[i,k] for i in V) >= p[k] for k in M), name="(18)")
model.addConstrs((gp.quicksum(x[i,k] for k in M) == 1 for i in V), name="(19)")
model.addConstrs((gp.quicksum(o[k] * x[j,k] for k in M_p) <= gp.quicksum(o[k] * x[i,k] for k in M_p) + o_max * (1-alpha[i,j]) 
                                for (i,j) in E if i != 0), name="(20)")
model.addConstrs((gp.quicksum(d[k] * x[j,k] for k in M_p) <= gp.quicksum(d[k] * x[i,k] for k in M_p) + d_max * (1-beta[i,j])
                                for (i,j) in E_b if j != 0), name="(21)")

model.addConstrs((gp.quicksum(u[j,i] for j in V_p if (j,i) in E) - gp.quicksum(u[i,j] for j in V_p if (i,j) in E) == gp.quicksum(q[i] * x[i,k] for k in M_p)
                                for i in V | {n+1}), name = "(22)")
model.addConstr((gp.quicksum(u[0,j] for j in V_p if (0,j) in E) == gp.quicksum(p[k] for k in M_p)), name = "(23)") 
model.addConstrs((gp.quicksum(v[i,j] for j in V_p if (i,j) in E_b) - gp.quicksum(v[j,i] for j in V_p if (j,i) in E_b) == gp.quicksum(q[i] * x[i,k]for k in M_p)
                                for i in V | {n+1}), name = "(24)")
model.addConstr((gp.quicksum(v[i,0] for i in V_p if (i,0) in E_b) == gp.quicksum(p[k] for k in M_p)), name = "(25)")

model.addConstrs((u[j,i] <= q_sum * alpha[j,i] for (j,i) in E), name = "(26b)")

model.addConstrs((v[i,j] <= q_sum * beta[i,j] for (i,j) in E_b), name = "(27b)")
model.addConstrs((gp.quicksum(alpha[j,i] for j in V_p if (j,i) in E) == 1 for i in V | {n+1}), name="(28a)")
model.addConstrs((gp.quicksum(beta[i,j] for j in V_p if (i,j) in E_b) == 1 for i in V | {n+1}), name="(28b)")



# TBD
# 1.向きの対応
# 2.高さ制限の対応
# 3.元のグラフに閉路が存在する場合，さらに部分巡回路を排除する制約の追加が必要



model.update()
model.write("a.lp")

model.optimize()
model.write("solution.sol")

#if model.status == gp.GRB.OPTIMAL:
#    model.printAttr('x')
#if model.solCount == 0:
    #print("Model is infeasible")
    #model.computeIIS()
    #model.write("model_iis.ilp")


sol = {i: k for i,k in x if isinstance(x[i,k], gp.Var) and  x[i,k].x > 0.5}
print(sol)

sola = {(i,k) for i,k in alpha if isinstance(alpha[i,k], gp.Var) and  alpha[i,k].x > 0.5}
print(sola)
solb = {(i,k) for i,k in beta if isinstance(beta[i,k], gp.Var) and  beta[i,k].x > 0.5}
print(solb)
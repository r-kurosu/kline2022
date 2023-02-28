import generate_sample
import visualize_sol
import test
import flow

# input parameters !!!
a = 4 # input row of block
b = 16 # input column of block
m = 1 # input number of car kinds
total_amount = 120 # input total amount of car


def main():
    # 1. generate sample data
    print(f"generate sample data: a={a}, b={b}, m={m}, total_amount={total_amount}")
    generate_sample.main(a, b, m, total_amount)
    
    # 2a. solve the problem flow and get the solution
    sol, sola,solb = flow.main()
    if sol is not None:
        visualize_sol.visualize_solution(sol, sola, solb, a, b, "flow")
    
    # 2b. solve the problem tree and get the solution
    sol, sola,solb = test.main()
    if sol is not None:
        visualize_sol.visualize_solution(sol, sola, solb, a, b, "tree")
    
    
    return

if __name__ == "__main__":
    main()
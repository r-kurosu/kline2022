import generate_sample
import visualize_sol
import test
import flow


def main():
    a = 5 # input row of brock
    b = 5 # input column of brock
    m = 4 # input number of car
    total_amount = 120 # input total amount of car
    
    # 1. generate sample data
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
import generate_sample
import visualize_sol

def main():
    a = 5 # input row of brock
    b = 5 # input column of brock
    m = 3 # input number of car
    total_amount = 120 # input total amount of car
    
    generate_sample.main(a, b, m, total_amount)
    visualize_sol.main(a, b)
    
    return

if __name__ == "__main__":
    main()
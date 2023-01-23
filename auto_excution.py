import generate_sample
import visualize_sol

def main():
    a = 5 # input row of brock
    b = 5 # input column of brock
    
    generate_sample.main(a,b)
    visualize_sol.main(a,b)
    
    return

if __name__ == "__main__":
    main()
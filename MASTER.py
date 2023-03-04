# input parameters
input_a = 4
input_b = 16
input_m = 6 # 車の数
input_total_amount = 500 # 車の総面積 (各車種の面積はランダム)

# set port list
PORT_list = [i for i in range(10)]

gap_area = 50 # ブロック容量に対するギャップ面積（0は車の総面積＝ブロックの総キャパシティ）

TIME_LIMIT = 100

# set weight (0はペナルティなし)
w1 = 1 # 各ブロックに入る向きと出る向きに関するペナルティ
w2 = 1 # 船と平行かどうかに関するペナルティ
w3 = 0 # 各港のギャングの好みに関するペナルティ
w4 = 1 # 席割り違反のペナルティ
w5 = 1 # 隣接ブロックのペナルティ

# set random seed
random_seed = 7 #1~100: fixed seed

# choose model
potential_flag = 1 #0: no potential, 1: with potential
next_block_flag = 1 #0: no block, 1: with block
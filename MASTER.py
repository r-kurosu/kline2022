# input parameters
input_a = 4
input_b = 16
input_m = 5 # 車の数
input_total_amount = 500 # 車の総面積 (各車種の面積はランダム)

ramp_block_to_upper_floor = 56 # 上のデッキにいくブロックの番号 (0〜a*b-1)

# set port list
input_port_num = 10 # 港の数
PORT_list = [i for i in range(input_port_num)]

gap_area = 100 # ブロック容量に対するギャップ面積（0は車の総面積＝ブロックの総キャパシティ）

TIME_LIMIT = 60

# set weight (0はペナルティなし)
w1 = 1 # 各ブロックに入る向きと出る向きに関するペナルティ
w2 = 1 # 船と平行かどうかに関するペナルティ
w3 = 1 # 各港のギャングの好みに関するペナルティ
w4 = 0 # 席割での指定ホールドのペナルティ
w5 = 1 # 隣接ブロックのペナルティ
w6 = 0 # ホールドのペナルティ（w4の改良版）
w7 = 0 # 入庫と出庫パスの複雑さのペナルティ（w1の改良版）

# set random seed
random_seed = 7 #1~100: fixed seed

# choose model
potential_flag = 1 #0: no potential, 1: with potential
next_block_flag = 1 #0: no block, 1: with block

limit_ramp_branch_model = 1 #0: no limit, 1: limit (入り口ランプに対する枝の方向を一つに固定)

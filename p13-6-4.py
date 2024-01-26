#
# オセロゲーム
#
# 定数の定義

OPEN = 0
FIRST = 1
SECOND = 2
DRAW = 3

# 恒常的な変数
turn = 1 
if turn == FIRST:
    opponent_turn = SECOND
if turn == SECOND:
    opponent_turn = FIRST
# 
board = [[0,0,0,0,0,0,0,0,],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,1,2,0,0,0],
         [0,0,0,2,1,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0], 
         [0,0,0,0,0,0,0,0]]
#
# テスト用の棋譜
#
log = [[3,5], [5,4], [2,4], [1,4], [1,5], [2,2], [1,3], [0,4], [4,2], [2,6], [0,6], [4,1], [5,3], [5,2], [4,0], [5,5], [3,2], [2,5], [6,3], [0,5], [1,6], [0,7], [1,7], [2,7], [5,6], [5,7], [6,5], [1,2], [4,7], [3,7], [0,2], [3,6], [4,6], [4,5], 2, [2,3], [1,1], [1,0], [7,2], [6,6], [7,5], [6,4], [0,0], [2,0], [0,1], [7,7], [7,4], [0,3], [7,6], [6,7], [3,0], [6,2], [2,1], [7,3], [3,1], [7,1], [5,0], [5,1], [SECOND]]
#
# 手番関連の関数
#
# 手番を文字列に
#
def show_turn():
    '手番を示す文字列を返す'
    if turn == FIRST:
        return('先手')
    elif turn == SECOND:
        return('後手')
    else:
        return('手番の値が不適切です')
#
# 手番の初期化
#
def init_turn():
    '手番を初期化する'
    global turn
    turn = 1
#
# 手番の交代
#
def change_turn():
    '手番を交代する'
    global turn
    global opponent_turn
    if turn == FIRST:
        turn = SECOND
        opponent_turn = FIRST
    elif turn == SECOND:
        turn = FIRST
        opponent_turn = SECOND

# 手羽の関連の関数のテスト
#
# def test_turn():
#     '手番をテストする'
#     init_turn()
#     print(show_turn(),"の番です")
#     change_turn()
#     print(show_turn(),"の番です")
#     change_turn()
#     print(show_turn(),"の番です")
#     print(turn)
#     print(opponent_turn)
# #
# #
# # 盤面関連の関数
# #
# # 盤面を表示する文字列
# #
def show_board():
    '盤面を表す文字列を返す'
    s = ' : 0 1 2 3 4 5 6 7\n-------------------\n'
    for i in range (8):
        s = s + str(i) + ': '
        for j in range(8):
            cell = ''
            if board[i][j] == OPEN:
                cell = ' '
            elif board[i][j] == FIRST:
                cell = '○'
            elif board[i][j] == SECOND:
                cell = '●'
            else:
                cell = '?'
            s = s + cell + ' '
        s = s + '\n'
    return s 
#
# 盤面の初期化
# 
def init_board():
    '盤面の中心に先手と後手の石を２ずつ置く、他をすべて空(OPEN)に初期化する'
    for i in range(8):
        for j in range(8):
            if i == 3 and j == 3:
                board[i][j] = FIRST
            elif i == 4 and j == 4:
                board[i][j] = FIRST
            elif i == 3 and j == 4:
                board[i][j] = SECOND
            elif i == 4 and j == 3:
                board[i][j] = SECOND
            else:
                board[i][j] = OPEN
#
# 盤面の i, j の位置の値を返す
# #
def examine_board(i,j):
    '盤面の i 行 j 行の値を返す'
    return board[i][j]
#
# 盤面が埋まっていることの判定
#
def is_full():
    '盤面に空きがないことを確認します'
    for i in range(8):
        for j in range(8):
            if board[i][j] == OPEN:
                return False
    return True
#
# 盤面の i, j に手番 t を登録、状態を文字列で返す
#
def set_board(i,j,t):
    '''
盤面の i, j に手番 t を登録、状態を文字列で返す
返す値は
    'ok' は成功
    'Not empty' 空いている場所ではない
    'illegal turn' 手番が正しくない
    'illegal slot' 指定された場所が正しくない
'''
    # 盤面上のマスである
    if (i>=0) and (i<8) and (j>=0) and (j<8):
        if (t>0) and (t<3):
            # マスが空いている（OPEN）
            if examine_board(i, j) == 0:
                board[i][j] = t
                return 'OK'
            else:
                return 'not empty'
        else:
            return 'illegal turn'
    else:
        return 'nonexistent slot'

def set_board_to_0(i, j):
    # 盤面上のマスである
    if (i>=0) and (i<8) and (j>=0) and (j<8):
        board[i][j] = 0
        return 'OK'
    else:
        return 'nonexistent slot'

# 盤面のテスト関数
#     
# def test_board1():
#     init_board()
#     print(show_board())
    # print(set_board(0,0,1))
    # print(show_board())
    # print(set_board(1,1,2))
    # print(show_board())
    # print(set_board(7,7,0))
    # print(show_board())
#
# ここから手番が置けるマスを探して、リスト化する
#     
# 手番 t が置けるマスのリスト（相手の石をひっくり返せる）
#
correct_place_list = []
#
def init_list():
    # 手番tが置けるマスのリストを空にする
    correct_place_list.clear()
#
# 垂直上方向で手番 t が置けるマスの判定
#
def check_board_vertical_upward(t):
    '垂直上方向に手番 t が置けるマスがあることを判定します'
    for i in range (8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            #  残りマスが少なくてダメ
            if i == 0 or i == 1:
                set_board_to_0(i, j)
                continue
            #　以下iが2以上の場合
            elif i >= 2:
                if board[i-1][j] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j] == opponent_turn:
                    for k in range(i-2,-1, -1):
                        if board [k][j] == OPEN:
                            break
                        elif board[k][j] == t:
                            place = [i,j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[k][j] == opponent_turn:
                            if k == 0:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
def check_board_vertical_downward(t):
    '垂直下方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if i == 6 or i == 7:
                set_board_to_0(i, j)
                continue
            # 以下iが０以上５以下の場合
            elif i <= 5:
                if board[i+1][j] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j] == opponent_turn:
                    for k in range(i+2, 8):
                        if board[k][j] == OPEN:
                            break
                        elif board[k][j] == t:
                            place = [i,j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[k][j] == opponent_turn:
                            if k == 7:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
def check_board_horizontal_left(t):
    '水平左方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            #  残りマスが少なくてダメ
            if j == 0 or j == 1:
                set_board_to_0(i, j)
                continue
            #　以下jが2以上の場合
            elif j >= 2:
                if board[i][j-1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i][j-1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i][j-1] == opponent_turn:
                    for k in range(j-2 ,-1, -1):
                        if board [i][k] == OPEN:
                            break
                        elif board[i][k] == t:
                            place = [i,j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[i][k] == opponent_turn:
                            if k == 0:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
def check_board_horizontal_right(t):
    '水平右方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if j == 6 or j == 7:
                set_board_to_0(i, j)
                continue
            # 以下 j が０以上５以下の場合
            elif j <= 5:
                if board[i][j+1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i][j+1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i][j+1] == opponent_turn:
                    for k in range(j+2, 8):
                        if board[i][k] == OPEN:
                            break
                        elif board[i][k] == t:
                            place = [i,j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[i][k] == opponent_turn:
                            if k == 7:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#                            
def check_board_diagonal_upward(t):
    '対角左上方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if i == 0 or i == 1:
                set_board_to_0(i, j)
                continue
            elif j == 0 or j == 1:
                set_board_to_0(i, j)
                continue
            # 以下i, j が２以上の場合
            elif i >= 2 and j >= 2:
                # t 番手の左斜め上のマスの判定
                if board[i-1][j-1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j-1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j-1] == opponent_turn:
                    # t 番手から左斜め上方向に２以上離れたマスを判定する範囲を決める
                    m = i - j
                    if m <= 0:
                        m == 0
                    l = j-1
                    # t 番手から２以上離れたマスがある時の判定
                    for k in range(i-2, m-1, -1):
                        l = l-1
                        if board[k][l] == OPEN:
                            break
                        elif board[k][l] == t:
                            place = [i, j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 0 or l == 0:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#            
def check_board_diagonal_downward(t):
    '対角右下方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            # print(f"Checking: {i}, {j}")
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if i == 6 or i == 7:
                set_board_to_0(i, j)
                continue
            elif j == 6 or j == 7:
                set_board_to_0(i, j)
                continue
            # 以下i, j が5以下の場合
            elif i <= 5 and j <= 5:
                # t 番手の右斜め下のマスの判定
                if board[i+1][j+1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j+1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j+1] == opponent_turn:
                    # print("1")
                    # t 番手から右斜め下方向に２以上離れたマスを判定する範囲を決める
                    m = i - j
                    # 対角線以下
                    if m >= 0:
                        m = 8
                    # 対角線より上
                    elif m < 0:
                        m = abs(m)
                        m = 8 - m
                    # 以下のfor文で、マスの縦列の始まりをt番手の１つ次に設定
                    l = j+1
                    # print("2")
                    # print("i:", i, "m:", m)
                    # t 番手から２以上離れたマスがある時の判定
                    for k in range(i+2, m):
                        # print(f"INSIDE FOR LOOP -- k: {k} l: {l}")
                        l = l+1
                        if board[k][l] == OPEN:
                            break
                        elif board[k][l] == t:
                            place = [i, j]
                            correct_place_list.append(place)
                            # print("INSIDE FOR LOOP -- cpl:", correct_place_list)
                            break
                        elif board[k][l] == opponent_turn:
                            # print("INSIDE FOR LOOP -- arrived")
                            if k == 7 or l == 7:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
def check_board_inverse_diagonal_upward(t):
    '逆対角右上方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if i == 0 or i == 1:
                set_board_to_0(i, j)
                continue
            elif j == 6 or j == 7:
                set_board_to_0(i, j)
                continue
            # 以下i が2以上, j が5以下の場合
            elif i >= 2 and j <= 5:
                # t 番手の右斜め上のマスの判定
                if board[i-1][j+1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j+1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i-1][j+1] == opponent_turn:
                    # t 番手から右斜め上方向に２以上離れたマスを判定する範囲を決める
                    m = i + j
                    # 対角線以上
                    if m <= 7:
                        m = 0
                    # 対角線より下
                    elif m >= 8:
                        m = (i + j) - 7
                    # 以下のfor文で、マスの縦列の始まりをt番手の１つ次に設定
                    l = j + 1
                    # t 番手から２以上離れたマスがある時の判定
                    for k in range(i-2, m-1, -1):
                        l = l + 1
                        if board[k][l] == OPEN:
                            break
                        elif board[k][l] == t:
                            place = [i, j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 0 or l == 7:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
def check_board_inverse_diagonal_downward(t):
    '逆対角左下方向に手番 t が置けるマスがあることを判定します'
    for i in range(8):
        for j in range(8):
            if board[i][j] != OPEN:
                continue
            set_board(i,j,t)
            # 残りマスが少なくてダメ
            if i == 6 or i == 7:
                set_board_to_0(i, j)
                continue
            elif j == 0 or j == 1:
                set_board_to_0(i, j)
                continue
            # 以下i が5以下, j が2以上の場合
            elif i <= 5 and j >= 2:
                # t 番手の左斜め下のマスの判定
                if board[i+1][j-1] == OPEN:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j-1] == t:
                    set_board_to_0(i, j)
                    continue
                elif board[i+1][j-1] == opponent_turn:
                    # t 番手から左斜め下方向に２以上離れたマスを判定する範囲を決める
                    m = i + j
                    # 対角線より下
                    if m >= 8:
                        m = 7
                    # 以下のfor文で、マスの縦列の始まりをt番手の１つ前fに設定
                    l = j - 1
                    # t 番手から２以上離れたマスがある時の判定
                    for k in range(i+2, m+1):
                        l = l - 1
                        if board[k][l] == OPEN:
                            break
                        elif board[k][l] == t:
                            place = [i, j]
                            correct_place_list.append(place)
                            print("cpl:", correct_place_list)
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 7 or l == 0:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
#
# 盤面のテスト関数２つめ、石を置けるマス判定のテスト
#
# def test_board2():
#     init_board()
#     print(show_board())
#     check_board_vertical_upward(turn)
#     print("cpl:", correct_place_list)        
# test_board2()
# # 
# set_board(1, 5, 3)
#
# ここから実際に手番が石を置いて、相手の石をひっくり返す
#
# 手番tが登録されたrow, columnから縦上方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_vertical_upward(row, column, t):
    changeable_place_list = []
    #  縦上方向に残りマスが少なくてダメ
    if row == 0 or row == 1:
        pass
    # 以下 row が2以上の場合
    # 登録された手番turnの上のマスを順に見て、相手方のマスなら手番turnを代入
    elif row >= 2:
        if board[row-1][column] == OPEN:
            pass
        elif board[row-1][column] == t:
            pass
        elif board[row-1][column] == opponent_turn:
            changeable_place = [row-1, column]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            for k in range(row-2,-1, -1):
                if board[k][column] == open:
                    break
                # 手番turnが出たら、ひっくり返せるリストのマスに手番turnを登録
                elif board[k][column] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                elif board[k][column] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)                                                     
#
# 手番tが登録されたrow, columnから縦下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_vertical_downward(row, column, t):
    changeable_place_list = []
    # 縦下方向に残りマスが少なくてダメ
    if row == 6 or row == 7:
        pass
    # 以下 row が５以下の場合
    # 登録された手番turnの下のマスを順に見て、相手方のマスなら手番turnを代入
    elif row <= 5:
        if board[row+1][column] == OPEN:
            pass
        elif board[row+1][column] == t:
            pass
        elif board[row+1][column] == opponent_turn:
            changeable_place =[row+1, column]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            for k in range(row+2, 8):
                if board[k][column] == OPEN:
                    break
                elif board[k][column] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                elif board[k][column] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)
#
# 手番tが登録されたrow, columnから水平左方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_horizontal_left(row, column, t):
    changeable_place_list = []
    # 水平左方向に残りマスが少なくてダメ
    if column == 0 or column == 1:
        pass
    # 以下column が2以上の場合
    elif column >= 2:
        if board[row][column-1] == OPEN:
            pass
        elif board[row][column-1] == t:
            pass
        elif board[row][column-1] == opponent_turn:
            changeable_place =[row, column-1]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            for k in range(column-2 ,-1, -1):
                if board [row][k] == OPEN:
                    break
                elif board[row][k] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                elif board[row][k] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls", changeable_place_list) 
                        
#          
# 手番tが登録されたrow, columnから水平右方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_horizontal_right(row, column, t):
    changeable_place_list = []
    # 水平右方向に残りマスが少なくてダメ
    if column == 6 or column == 7:
        pass
    # 以下columnが５以下の場合
    elif column <= 5:
        if board[row][column+1] == OPEN:
            pass
        elif board[row][column+1] == t:
            pass
        elif board[row][column+1] == opponent_turn:
            changeable_place =[row, column+1]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            for k in range(column+2, 8):
                if board[row][k] == OPEN:
                    break
                elif board[row][k] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                elif board[row][k] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)                   
#
# 手番turnが登録されたrow, columnから左斜め上方向にひっくり返せるマスを検査し、相手方のマスに手番tを登録
def check_changeable_place_diagonal_upward(row, column, t):
    changeable_place_list = []
    # 左斜め上方向に残りマスが少なくてダメ
    if row == 0 or row == 1:
        pass
    elif column == 0 or column == 1:
        pass
    # 以下rowが２以上、columnが２以上の場合
    elif row >= 2 and column >= 2:
        # t 番手の左斜め上のマスの判定
        if board[row-1][column-1] == OPEN:
            pass
        elif board[row-1][column-1] == t:
            pass
        elif board[row-1][column-1] == opponent_turn:
            changeable_place = [row-1, column-1]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            # 対角線より上のマスについては、検査するrowを０までとする
            m = row - column
            if m <= 0:
                m = 0
            # マスの左斜め上の列を検査の起点とする
            l = column-1
            # 左斜め上に２以上離れたマスの判定
            for k in range(row-2, m-1, -1):
                l = l - 1
                if board[k][l] == OPEN:
                    break
                elif board[k][l] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)      
#                   
#            
# 手番turnが登録されたrow, columnから右斜め下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録 
def check_changeable_place_diagonal_downward(row, column, t):
    changeable_place_list = []
    # 右斜め下方向にマスが少なくてダメ
    if row == 6 or row == 7:
        pass
    elif column == 6 or column == 7:
        pass
    # 以下row, columnが5以下の場合
    elif row <= 5 and column <= 5:
            # t 番手の右斜め下のマスの判定
            if board[row+1][column+1] == OPEN:
                pass
            elif board[row+1][column+1] == t:
                pass
            elif board[row+1][column+1] == opponent_turn:
                changeable_place = [row+1, column+1]
                changeable_place_list.append(changeable_place)
                print("plf:", changeable_place_list)
                # turn 番手から右斜め下方向のマスを判定する範囲を決める
                m = row - column
                # 対角線以下
                if m >= 0:
                    m = 8
                # 対角線より上
                elif m < 0:
                    m = abs(m)
                    m = 8 - m
                # 以下のfor文で、マスの縦列の始まりをt番手の１つ次に設定
                l = column + 1
                # t 番手から２以上離れたマスがある時の判定
                for k in range(row+2, m):
                        l = l+1
                        if board[k][l] == OPEN:
                            break
                        elif board[k][l] == t:
                            for cell in changeable_place_list:
                                board[cell[0]][cell[1]] = t
                        elif board[k][l] == opponent_turn:
                            if k == 7 or l == 7:
                                break
                            else:
                                changeable_place = [k, l]
                                changeable_place_list.append(changeable_place) 
                                print("pls:", changeable_place_list)      
#
# 手番turnが登録されたrow, columnから右斜め上方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_inverse_diagonal_upward(row, column, t):
    changeable_place_list = []
    # 右斜め上方向に残りマスが少なくてダメ
    if row == 0 or row == 1:
        pass
    elif column == 6 or column == 7:
        pass
    # 以下i が2以上, j が5以下の場合
    elif row  >= 2 and column <= 5:
        # t 番手の右斜め上のマスの判定
        if board[row-1][column+1] == OPEN:
            pass
        elif board[row-1][column+1] == t:
            pass
        elif board[row-1][column+1] == opponent_turn:
            changeable_place = [row-1, column+1]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            # t 番手から右斜め上方向に２以上離れたマスを判定する範囲を決める
            m = row + column
            # 対角線以上
            if m <= 7:
                m = 0
            # 対角線より下
            elif m >= 8:
                m = (row + column) - 7
            # 以下のfor文で、マスの縦列の始まりをt番手の１つ次に設定
            l = column + 1
            # t 番手から２以上離れたマスがある時の判定
            for k in range(row-2, m-1, -1):
                l = l + 1
                if board[k][l] == OPEN:
                    break
                elif board[k][l] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t        
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 7:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)      
#
# 手番turnが登録されたrow, columnから左斜め下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録
def check_changeable_place_inverse_diagonal_downward(row, column, t):
    changeable_place_list = []
    # 残りマスが少なくてダメ
    if row == 6 or row == 7:
        pass
    elif column == 0 or column == 1:
        pass
    # 以下i が5以下, j が2以上の場合
    elif row <= 5 and column >= 2:
        # t 番手の左斜め下のマスの判定
        if board[row+1][column-1] == OPEN:
            pass
        elif board[row+1][column-1] == t:
            pass
        elif board[row+1][column-1] == opponent_turn:
            changeable_place = [row+1, column-1]
            changeable_place_list.append(changeable_place)
            print("plf:", changeable_place_list)
            # t 番手から左斜め下方向に２以上離れたマスを判定する範囲を決める
            m = row + column
            # 対角線より下
            if m >= 8:
                m = 7
            # 以下のfor文で、マスの縦列の始まりをt番手の１つ前fに設定
            l = column - 1
            # t 番手から２以上離れたマスがある時の判定
            for k in range(row+2, m+1):
                l = l - 1
                if board[k][l] == OPEN:
                    break
                elif board[k][l] == t:
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t          
                elif board[k][l] == opponent_turn:
                    if k == 7 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)

def is_win():
    '''
    手番 t の勝ちの判定
    '''
    first_count = 0
    second_count = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == FIRST:
                first_count += 1
            elif board[i][j] == SECOND:
                second_count += 1 
    print("○は", first_count)
    print("●は", second_count)
    if first_count > second_count:
        print("白の勝ちです")
        log.append(FIRST)
    elif second_count > first_count:
        print("黒の勝ちです")
        log.append(SECOND)
    elif first_count == second_count:
        print("引き分けです")
        log.append(DRAW)

# 端末への入力を用いて、入力の検査をします. 正しい入力が得られた場合は、ひっくり返せるマスに手番 t を登録します
def play():
    pass_count = 0
    init_turn()
    init_board()
    print(show_board())
    firstlog = []
    secondlog = []
    # 盤面に空きマスがある時に、手番t が置けるマスがあるかを判定して「置けるリスト」を作成
    while True:
        init_list()
        check_board_vertical_upward(turn)
        check_board_vertical_downward(turn)
        check_board_horizontal_left(turn)
        check_board_horizontal_right(turn)
        check_board_diagonal_upward(turn)
        check_board_diagonal_downward(turn)
        check_board_inverse_diagonal_upward(turn)
        check_board_inverse_diagonal_downward(turn)
        print("cpl:", correct_place_list)
        # 手番turnが置けるマスがなく、置けるマスのリストが空
        if len(correct_place_list) == 0: 
            print('Pass')
            pass_count += 1
            # 双方置けるマスがなく、勝敗判定に移る
            if pass_count == 2:
                is_win()
                break
            # 手番側のみ置けるマスがないため、相手に手番を交代する
            # else:
                # change_turn()
        # 手番turnが置けるマスがあるので、手番の入力を促す
        else:
            while True:
                pass_count = 0
                print(show_turn(),"の番です")
                row = int(input("行を入力してください: "))
                column = int(input("列を入力してください: "))
                # [row, column]がcorrect_place_listにあるかどうかをチェックし、あれば手番turnを登録
                square_to_check = [row, column]
                if not square_to_check in correct_place_list:
                    print("そこには置けません")
                else:
                    break
            result = set_board(row, column, turn)
            if turn == FIRST:
                firstlog.append(square_to_check)
            elif turn == SECOND:
                secondlog.append(square_to_check)
            print("firstslog:", firstlog)
            print("secondlog:", secondlog)
            print(result)
            if result == 'OK':
                # 手番turnが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
                check_changeable_place_vertical_upward(row, column, turn)
                check_changeable_place_vertical_downward(row, column, turn)
                check_changeable_place_horizontal_left(row, column, turn)
                check_changeable_place_horizontal_right(row, column, turn)
                check_changeable_place_diagonal_upward(row, column, turn)   
                check_changeable_place_diagonal_downward(row, column, turn)                
                check_changeable_place_inverse_diagonal_upward(row, column, turn)
                check_changeable_place_inverse_diagonal_downward(row, column, turn)

        print(show_board())
        if is_full():
            is_win()
            break
        else:
            change_turn()
    # print("-----------------------------------")
    # if len(log)>0:
    #     replay_log(log)
    # else:
    #     print("棋譜は作成されていません")

# def test():
#     pass_count = 0
#     init_turn()
#     init_board()
#     board[5][3] = 2
#     print(show_board())
#     check_changeable_place_vertical_upward(6, 3, 1)
#     print(show_board())

play()

# test()

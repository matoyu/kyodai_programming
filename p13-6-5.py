#
# オセロゲーム(GUI)
#
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
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
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0], 
         [0,0,0,0,0,0,0,0]]
#
def show_turn_gui():
    '手番をlabel上に表示'
    if turn == FIRST:
        label_text.set("先手の番です")
    elif turn == SECOND:
        label_text.set("後手の番です")
    else:
        label_text.set("手番が不適切です")
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
        show_turn_gui()
    elif turn == SECOND:
        turn = FIRST
        opponent_turn = SECOND
        show_turn_gui()
#
# 盤面を表示するGUI
def show_board_gui():
    '盤面を表す文字列を返す'
    for i in range(8):
        for j in range(8):
            if board[i][j] == OPEN:
                buttons[i][j].configure(image = tk_space_image)
                # buttons[i][j] = tk_space_image
            elif board[i][j] == FIRST:
                buttons[i][j].configure(image = tk_shiroishi_image)
                # buttons[i][j].image = tk_shiroishi_image
            elif board[i][j] == SECOND:
                buttons[i][j].configure(image = tk_kuroishi_image)
                # buttons[i][j].image = tk_kuroishi_image
            # else:
            #     button_texts[i][j].set('?')
#
def init_board():
    for i in range(8):
        for j in range(8):
            board[i][j] = OPEN

def start_board():
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

# 盤面の i, j の位置の値を返す
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
#
def set_board_to_0(i, j):
    # 盤面上のマスである
    if (i>=0) and (i<8) and (j>=0) and (j<8):
        board[i][j] = 0
        return 'OK'
    else:
        return 'nonexistent slot'
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
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
                            # print("cpl:", correct_place_list)
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 7 or l == 0:
                                break
                            else:
                                continue
                    set_board_to_0(i, j)
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)                                                     
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)
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
            # print("plf:", changeable_place_list)
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
                        # print("pls", changeable_place_list) 
                        
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)                   
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)      
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
                # print("plf:", changeable_place_list)
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
                                # print("pls:", changeable_place_list)      
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)      
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
            # print("plf:", changeable_place_list)
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
                        # print("pls:", changeable_place_list)
#
# 勝ちの判定
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
        label_text.set("白の勝ちです")
    elif second_count > first_count:
        label_text.set("黒の勝ちです")
    elif first_count == second_count:
        label_text.set("引き分けです")
#
#START_RESETボタンが押された時の処理
def start_reset(start_reset_button_text, label_text):
    if start_reset_button_text.get() == "START":
        start_reset_button_text.set("RESET")
        start_board()
        show_board_gui()
        turn = FIRST
        show_turn_gui()
        check_board(turn)
        # print("start_reset_list:", correct_place_list)
    elif start_reset_button_text.get() == "RESET": 
        start_reset_button_text.set("START")
        label_text.set("オセロゲーム")
        init_turn()
        init_board()
        show_board_gui()
#
# 盤面を検査して、置けるマスのリストを作成、ラベルに番手を表示またはパス、パス回数と番手を表示
def check_board(turn):
    global correct_place_list
    init_list()
    # print(correct_place_list)
    # print(turn)
    check_board_vertical_upward(turn)
    check_board_vertical_downward(turn)
    check_board_horizontal_left(turn)
    check_board_horizontal_right(turn)
    check_board_diagonal_upward(turn)
    check_board_diagonal_downward(turn)
    check_board_inverse_diagonal_upward(turn)
    check_board_inverse_diagonal_downward(turn)
    # print(correct_place_list)

    # 手番turnが置けるマスがなく、置けるマスのリストが空
    # if len(correct_place_list) == 0: 
    #     pass_count += 1
    #     label_text.set("パス１")
#
def button_clicked(row, column):
    # pass_count = 0
    # while True:
        # row = i
        # column = j
        # [row, column]がcorrect_place_listにあるかどうかをチェックし、あれば手番turnを登録
    square_to_check = [row, column]
    if not square_to_check in correct_place_list:
        label_text.set("そこには置けません")
        return
    # else:
    #         break
    result = set_board(row, column, turn)
    # if turn == FIRST:
    #     firstlog.append(square_to_check)
    # elif turn == SECOND:
    #     secondlog.append(square_to_check)
        # print("firstslog:", firstlog)
        # print("secondlog:", secondlog)
    # print(result)
    if result == 'OK':
        print(row, column)
        # 手番turnが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
        check_changeable_place_vertical_upward(row, column, turn)
        check_changeable_place_vertical_downward(row, column, turn)
        check_changeable_place_horizontal_left(row, column, turn)
        check_changeable_place_horizontal_right(row, column, turn)
        check_changeable_place_diagonal_upward(row, column, turn)   
        check_changeable_place_diagonal_downward(row, column, turn)                
        check_changeable_place_inverse_diagonal_upward(row, column, turn)
        check_changeable_place_inverse_diagonal_downward(row, column, turn)
        show_board_gui()
        # print("a")
        if is_full():
            is_win()
        else:
            # print(turn)
            change_turn()
            # print(turn)
            # print("b")
            check_board(turn)
            # print("c")
            # 置けるマスがない、correct_place_listが空
            if len(correct_place_list) == 0: 
                # pass_count += 1
                messagebox.showinfo('information', '置けるマスがないのでパス１')
                # OKをクリックしてボックスを閉じる
                change_turn()
                check_board(turn)
                # 再び置けるマスがない、correct_place_listが空
                if len(correct_place_list) == 0:
                    # pass_count += 1
                    messagebox.showinfor('information', '置けるますがないのでパス２')
                    # OKをクリックしてボックスを閉じる
                    is_win()
                # 置けるマスがある、correct_place_listに候補がある
                else:
                    show_turn_gui                   
            # 置けるマスがある、correct_place_listに候補がある
            else:
                # pass_count = 0
                show_turn_gui()



    # for i in button_labels:
    #     for j in i:
    #         j.set(' ')
    # init_label()
    # game_over = False

def init_label():
    label_text.set("オセロゲーム")

def resize_image(image, width, height):
    return image.resize((width, height), Image.Resampling.LANCZOS)

# tkinter での画面の構成, ここからGUI
num_buttons_per_row = 8
num_rows = 8
root = tk.Tk()
f = tk.Frame(root)
f.grid()    
#
# オセロ石のイメージを読み込み、サイズを変更
# 白石
original_shiroishi_image = Image.open("オセロ白石.png")
resized_shiroishi_image = resize_image(original_shiroishi_image, 70, 70) 
tk_shiroishi_image = ImageTk.PhotoImage(resized_shiroishi_image)
# 黒石
original_kuroishi_image = Image.open("オセロ黒石.png")
resized_kuroishi_image = resize_image(original_kuroishi_image, 70, 70)
tk_kuroishi_image = ImageTk.PhotoImage(resized_kuroishi_image)
# スペース
original_space_image = Image.open("オセロスペース.png")
resized_space_image = resize_image(original_space_image, 70, 70)
tk_space_image = ImageTk.PhotoImage(resized_space_image)
#
# # StringVarのインスタンスを格納する変数button_labelsのリスト
# # 8行全てのStringVar変数のリスト
# all_button_texts = []
# for i in range(8):
#     # １行８個分のStringVar変数のリスト
#     button_texts = []
#     for j in range(8):
#         button_texts.append(tk.StringVar(f))
#     all_button_texts.append(button_texts)
# print(all_button_labels)
#
# # button上の表示を全てスペースにする
# for i in all_button_texts:
#     for j in i:
#        j.set(' ')
#

buttons = []

# ウィジェットの作成
def create_buttons(f, num_buttons_per_row, num_rows):
    global buttons
    for i in range(num_rows):
        button_row = []
        for j in range(num_buttons_per_row):
            # button_number = 1 * num_buttons_per_row + j + 1
            button = tk.Button(f, image = tk_space_image, command=lambda i=i, j=j: button_clicked(i,j), highlightbackground = '#000000')
            button.grid(row=i+1, column=j)
            button_row.append(button)
        buttons.append(button_row)

create_buttons(f, num_buttons_per_row, num_rows)
#
# ラベル上のテキストを変換するStringVarのインスタンス
label_text = tk.StringVar(f)
label_text.set("オセロゲーム")

# 勝敗を表示するウィジェット
l = tk.Label(f, textvariable=label_text, height = 2, font = ('Helvetica, 28'))
l.grid(row=0, column=0, columnspan=8)

# start_reset_button上のStringVar変数の作成
start_reset_button_text = tk.StringVar(f)
start_reset_button_text.set("START")
# START_RESETボタンの作成とウィジェットの割付
br = tk.Button(f, textvariable=start_reset_button_text, command = lambda:start_reset(start_reset_button_text, label_text), height = 2, width = 3, font = ('Helvetica, 15'))
br.grid(row=9, column=0, columnspan=8)
#
root.mainloop()
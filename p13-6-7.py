#
# オセロゲーム(GUI)対コンピューター強弱あり
#
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import random
import time
#
# 定数の定義

OPEN = 0
FIRST = 1
SECOND = 2
DRAW = 3

# コンピューターのレベルの変数
computer_level = -1

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
log = []
#
def init_log():
    log = []
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
    print("change_turn:", turn, FIRST, SECOND)
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
            # root.update()
                # buttons[i][j].image = tk_kuroishi_image
            # else:
            #     button_texts[i][j].set('?')
#
def play_sound_effect(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

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
# 手番tが置けるマスの判定
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
# 手番tが登録されたrow, columnから8方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録    
#                                              
def check_changeable_place_vertical_upward(row, column, t):
    '手番tが登録されたrow, columnから縦上方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                if board[k][column] == OPEN:
                    break
                # 手番turnが出たら、ひっくり返せるリストのマスに手番turnを登録
                elif board[k][column] == t:
                    print("all vucp", changeable_place_list) 
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break
                elif board[k][column] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)                                                            
#
def check_changeable_place_vertical_downward(row, column, t):
    '手番tが登録されたrow, columnから縦下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                    print("all vdcp", changeable_place_list)
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break
                elif board[k][column] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)
#
def check_changeable_place_horizontal_left(row, column, t):
    ' 手番tが登録されたrow, columnから水平左方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                    print("all hlcp", changeable_place_list)
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break
                elif board[row][k] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls", changeable_place_list)       
#
def check_changeable_place_horizontal_right(row, column, t):
    '手番tが登録されたrow, columnから水平右方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                    print("all hrcp", changeable_place_list)  
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break
                elif board[row][k] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)         
#
def check_changeable_place_diagonal_upward(row, column, t):
    '手番turnが登録されたrow, columnから左斜め上方向にひっくり返せるマスを検査し、相手方のマスに手番tを登録'
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
                    print("all ducp", changeable_place_list) 
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break                       
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)     
#                   
def check_changeable_place_diagonal_downward(row, column, t):
    '手番tが登録されたrow、columnから右斜め下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                            print("all ddcp", changeable_place_list) 
                            for cell in changeable_place_list:
                                board[cell[0]][cell[1]] = t
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 7 or l == 7:
                                break
                            else:
                                changeable_place = [k, l]
                                changeable_place_list.append(changeable_place) 
                                print("pls:", changeable_place_list)     
#
def check_changeable_place_inverse_diagonal_upward(row, column, t):
    '手番turnが登録されたrow, columnから右斜め上方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                    print("all iducp", changeable_place_list)    
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break        
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 7:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)
#
def check_changeable_place_inverse_diagonal_downward(row, column, t):
    '手番turnが登録されたrow, columnから左斜め下方向にひっくり返せるマスを検査し、相手方のマスに手番turnを登録'
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
                    print("all iddcp", changeable_place_list) 
                    for cell in changeable_place_list:
                        board[cell[0]][cell[1]] = t
                    break         
                elif board[k][l] == opponent_turn:
                    if k == 7 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)
#  
# 対戦レベル強めでコンピューターが置ける８方向のマスの数を検査     
#                                             
def check_computer_stronger_vertical_upward(row, column, t):
    '戦レベル強めでコンピューターが置ける縦上方向マスの数を検査'
    computer_get_vertical_upward = 0
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
                if board[k][column] == OPEN:
                    break
                # 手番turnが出たら、ひっくり返せるリストのマスに手番turnを登録
                elif board[k][column] == t:
                    print("all vucp", changeable_place_list)
                    computer_get_vertical_upward = len(changeable_place_list)
                    print(computer_get_vertical_upward)
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break
                elif board[k][column] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)   
    return computer_get_vertical_upward
#
def check_computer_stronger_vertical_downward(row, column, t):
    '対戦レベル強めでコンピューターが置ける縦下方向マスの数を検査'
    computer_get_vertical_downward = 0
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
                    print("all vdcp", changeable_place_list)
                    computer_get_vertical_downward = len(changeable_place_list)
                    print(computer_get_vertical_downward)
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break
                elif board[k][column] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [k, column]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)
    return computer_get_vertical_downward 
# 
def check_computer_stronger_horizontal_left(row, column, t):
    '対戦レベル強めでコンピューターが置ける横左方向マスの数を検査'
    computer_get_horizontal_left = 0
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
                    print("all hlcp", changeable_place_list)
                    computer_get_horizontal_left = len(changeable_place_list)
                    print(computer_get_horizontal_left)
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break
                elif board[row][k] == opponent_turn:
                    if k == 0:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls", changeable_place_list)     
    return computer_get_horizontal_left  
#  
def check_computer_stronger_horizontal_right(row, column, t):
    '対戦レベル強めでコンピューターが置ける横右方向マスの数を検査'
    computer_get_horizontal_right = 0
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
                    print("all hrcp", changeable_place_list) 
                    computer_get_horizontal_right = len(changeable_place_list)
                    print(computer_get_horizontal_right) 
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break
                elif board[row][k] == opponent_turn:
                    if k == 7:
                        break
                    else:
                        changeable_place = [row, k]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)   
    return computer_get_horizontal_right      
#
def check_computer_stronger_diagonal_upward(row, column, t):
    '対戦レベル強めでコンピューターが置ける左斜め上方向のマスの数を検査'
    computer_get_diagonal_upward = 0
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
                    print("all ducp", changeable_place_list) 
                    computer_get_diagonal_upward = len(changeable_place_list)
                    print(computer_get_diagonal_upward) 
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break                       
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)  
                        print("pls:", changeable_place_list)    
    return computer_get_diagonal_upward
# 
def check_computer_stronger_diagonal_downward(row, column, t):
    '対戦レベル強めでコンピューターが置ける右斜め下方向のマスを検査'
    computer_get_diagonal_downward = 0
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
                            print("all ddcp", changeable_place_list) 
                            computer_get_diagonal_downward = len(changeable_place_list)
                            print(computer_get_diagonal_downward) 
                            # for cell in changeable_place_list:
                                # board[cell[0]][cell[1]] = t
                            break
                        elif board[k][l] == opponent_turn:
                            if k == 7 or l == 7:
                                break
                            else:
                                changeable_place = [k, l]
                                changeable_place_list.append(changeable_place) 
                                print("pls:", changeable_place_list)
    return computer_get_diagonal_downward
#
def check_computer_stronger_inverse_diagonal_upward(row, column, t):
    '対戦レベル強めでコンピューターが置ける右斜め上方向のマスを検査'
    computer_get_inverse_diagonal_upward = 0
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
                    print("all iducp", changeable_place_list)    
                    computer_get_inverse_diagonal_upward = len(changeable_place_list)
                    print(computer_get_inverse_diagonal_upward) 
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break        
                elif board[k][l] == opponent_turn:
                    if k == 0 or l == 7:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place) 
                        print("pls:", changeable_place_list)
    return computer_get_inverse_diagonal_upward
#
def check_computer_stronger_inverse_diagonal_downward(row, column, t):
    '対戦レベル強めでコンピューターが置ける左斜め下方向のマスを検査'
    computer_get_inverse_diagonal_downward = 0
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
                    print("all iddcp", changeable_place_list) 
                    computer_get_inverse_diagonal_downward = len(changeable_place_list)
                    print(computer_get_inverse_diagonal_downward) 
                    # for cell in changeable_place_list:
                        # board[cell[0]][cell[1]] = t
                    break         
                elif board[k][l] == opponent_turn:
                    if k == 7 or l == 0:
                        break
                    else:
                        changeable_place = [k, l]
                        changeable_place_list.append(changeable_place)
                        print("pls:", changeable_place_list)
    return computer_get_inverse_diagonal_downward
#                                                                                                               
#
corner_list = []                        
def corner():
    init_corner_list()
    for i in correct_place_list:
        if i[0] == 0 and i[1] == 0:
            corner = [0,0]
            corner_list.append(corner)
        elif i[0] == 0 and i[1] == 7:
            corner = [0,7]
            corner_list.append(corner)
        elif i[0] == 7 and i[1] == 0:
            corner = [7,0]
            corner_list.append(corner)
        elif i[0] == 7 and i[1] == 7:
            corner = [7,7]
            corner_list.append(corner)
    print(corner_list)
#
def init_corner_list():
    corner_list.clear()
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
    white_number = str(first_count)
    black_number = str(second_count)
    if first_count > second_count:
        combined_result = "白は" + white_number + "黒は" + black_number + "で白の勝ちです"
        label_text.set(combined_result)
        play_sound_effect("win.mp3")
    elif second_count > first_count:
        combined_result = "黒は" + black_number + "白は" + white_number + "で黒の勝ちです"
        label_text.set(combined_result)
        play_sound_effect("win.mp3")
    elif first_count == second_count:
        combined_result = "白は" + white_number + "黒は" + black_number + "で引き分けです"
        label_text.set(combined_result)
        play_sound_effect("even.mp3")
#
#先手ボタンが押された時の処理
def start():
    print("人が先手")
    change_sente_text()
    start_board()
    show_board_gui()
    play_sound_effect("place.mp3")
    init_log()
    turn = FIRST
    show_turn_gui()
    check_board(turn)
     # print("start_reset_list:", correct_place_list)
#
# 後手ボタンが押された時の処理
def computer_start():
    print("人が後手")
    change_gote_text()
    global turn
    start_board()
    show_board_gui()
    play_sound_effect("place.mp3")
    init_log()
    turn = FIRST
    show_turn_gui()
    check_board(turn)
    random_list = random.choice(correct_place_list)
    print("Random list", random_list)
    row = random_list[0]
    column = random_list[1]
    # play_sound_effect("place.mp3")
    set_board(row, column,turn)
    # コンピューターの棋譜も記録
    computer_stone_position = [row, column, turn]
    log.append(computer_stone_position)
    print("log", log)
    # 手番1(先手:コンピューター)が置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
    check_changeable_place(row, column, turn)
    root.update()
    root.after(random.randint(2000,5000), show_board_gui())
    play_sound_effect("place.mp3")
    print("手番１のコンピューターになっているか？", turn)
    change_turn() #後手へ 
    print("手番２の人になっているか？", turn)
    check_board(turn)
    show_turn_gui
#
def reset():
    label_text.set("対戦レベルを選んでください")
    init_turn()
    init_board()
    init_corner_list()
    init_log()
    show_board_gui()
    # replay_log(log)
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
    print("Final correct place list:", correct_place_list)
#
# 手番turnが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
def check_changeable_place(row, column, turn):
    check_changeable_place_vertical_upward(row, column, turn)
    check_changeable_place_vertical_downward(row, column, turn)
    check_changeable_place_horizontal_left(row, column, turn)
    check_changeable_place_horizontal_right(row, column, turn)
    check_changeable_place_diagonal_upward(row, column, turn)   
    check_changeable_place_diagonal_downward(row, column, turn)                
    check_changeable_place_inverse_diagonal_upward(row, column, turn)
    check_changeable_place_inverse_diagonal_downward(row, column, turn)
#
def button_clicked(row, column):
    '[row, column]がcorrect_place_listにあるかどうかをチェックし、あれば手番turnを登録'
    play_sound_effect("place.mp3")
    square_to_check = [row, column]
    if not square_to_check in correct_place_list:
        label_text.set("そこには置けません")
        play_sound_effect("error.mp3")
        return
    set_board(row, column, turn)
    print("ここから人か？", turn)
    # 棋譜の記録
    stone_position = [row, column, turn]
    log.append(stone_position)
    print("log", log)
    # 人が置いたマスのrow, columnから縦、横、斜めを再検査し、コンピューターの石を挟むことができればマスに手番turnを登録する
    check_changeable_place(row, column, turn)
    show_board_gui()
    # print("a")
    if is_full():
        is_win()
        print("log", log)
    else:
    # ここからコンピューター
    # print(turn)
        change_turn() # 手番がコンピューターへ
        print("ここからコンピューターか？", turn)
        # print(turn)
        # print("b")
        check_board(turn)
        print("computer:", correct_place_list)
        # コンピューターが置けるマスがない、correct_place_listが空
        if len(correct_place_list) == 0:
            play_sound_effect("pass.mp3")
            root.update()
            messagebox.showinfo('information', '置けるマスがないのでパス１')
            # OKをクリックしてボックスを閉じる
            # コンピューターのパス1を記録
            pass_record = ["pass1"]
            log.append(pass_record)
            change_turn() # 人へ
            check_board(turn)
            # 人も置けるマスがない、correct_place_listが空
            if len(correct_place_list) == 0:
                # pass_count += 1
                play_sound_effect("pass.mp3")
                root.update()
                messagebox.showinfo('information', '置けるマスがないので勝敗を判定します')
                # OKをクリックしてボックスを閉じる
                # 棋譜にPass2を記録
                pass_record = ["pass2"]
                log.append(pass_record)
                # 勝敗判定
                is_win()
                print("log",log)
            # 人が置けるマスがある、correct_place_listに候補がある
            else:
                show_turn_gui()                   
        # コンピューターが置けるマスがある、correct_place_listに候補がある
        else:
            show_turn_gui()
            print("computer arrived", turn)
            if computer_level == 0:
                computer()
            elif computer_level == 1:
                computer_stronger()
#
# 対戦レベル弱めが選ばれた時のコンピューターのプレイ
def computer():
    while True:
        random_list = random.choice(correct_place_list)
        print("Random list", random_list)
        row = random_list[0]
        column = random_list[1]
        set_board(row, column,turn)
        # コンピューターの棋譜も記録
        computer_stone_position = [row, column, turn]
        log.append(computer_stone_position)
        print("log", log)
        # コンピューターが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
        check_changeable_place(row, column, turn)
        root.update()
        root.after(random.randint(2000,5000), show_board_gui())
        play_sound_effect("place.mp3")
        # マスが一杯
        if is_full():
            is_win()
            print("log", log)
            break
        # マスに空きがある
        else:
            print("コンピューターになっているか", turn)
            change_turn() #人へ 
            print("人になっているか？", turn)
            check_board(turn)
            # 人が置くことができるマスがない
            if len(correct_place_list) == 0: 
                root.update()
                messagebox.showinfo('information', "置けるマスがないのでパス１")
                # 棋譜にパス１を記録
                pass_record = ["pass1"]
                log.append(pass_record)
                change_turn() # 再びコンピューターへ
                check_board(turn)
                # コンピューターも置くことができるマスがない
                if len(correct_place_list) == 0: 
                    root.update()
                    messagebox.showinfo('information', "置けるマスがないのでパス2で勝敗を判定します")
                    is_win()
                # コンピューターが置くことができるマスがある
                else:
                    show_turn_gui()         
            # 人が置くことができるマスがある
            else:
                print("人に戻っているか", turn)
                show_turn_gui # 人の番
                break
#
def computer_stronger():
    while True:
        corner()
        # 角に置けるマスがある
        if len(corner_list) != 0:
            random_corner = random.choice(corner_list)
            row = random_corner[0]
            column = random_corner[1]
            set_board(row, column,turn)
            # コンピューターの棋譜も記録
            computer_stone_position = [row, column, turn]
            log.append(computer_stone_position)
            print("log", log)
            # コンピューターが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
            check_changeable_place(row, column, turn)
            root.update()
            root.after(random.randint(2000,5000), show_board_gui())
            play_sound_effect("place.mp3")
            # マスが一杯
            if is_full():
                is_win()
                print("log", log)
                break
            # マスに空きがある
            else:
                print("コンピューターになっているか", turn)
                change_turn() #人へ 
                print("人になっているか？", turn)
                check_board(turn)
                # 人が置くことができるマスがない
                if len(correct_place_list) == 0: 
                    root.update()
                    messagebox.showinfo('information', "置けるマスがないのでパス１")
                    # 棋譜にパス１を記録
                    pass_record = ["pass1"]
                    log.append(pass_record)
                    change_turn() # 再びコンピューターへ
                    check_board(turn)
                    # コンピューターも置くことができるマスがない
                    if len(correct_place_list) == 0: 
                        root.update()
                        messagebox.showinfo('information', "置けるマスがないのでパス2で勝敗を判定します")
                        is_win()
                    # コンピューターが置くことができるマスがある
                    else:
                        show_turn_gui()         
                # 人が置くことができるマスがある
                else:
                    print("人に戻っているか", turn)
                    show_turn_gui # 人の番
                    break
        # 角に置けるマスがない
        else:
            print("角ではないコンピューター強")
            computer_get = 0
            best_choice_list = []
            for i in correct_place_list:
                row = i[0]
                column = i[1]
                # check_computer_stronger(row, column, turn)
                new_computer_get = check_computer_stronger(row, column, turn)
                if new_computer_get > computer_get:
                    best_choice_list.clear()
                    computer_get = new_computer_get
                    best_choice = [row, column, turn]
                    best_choice_list.append(best_choice)
                elif new_computer_get == computer_get:
                    best_choice = [row, column, turn]
                    best_choice_list.append(best_choice)
                else:
                    continue
            print("best choice list", best_choice_list)
            random_best_choice = random.choice(best_choice_list)
            print("randam best choice", random_best_choice)
            set_board(random_best_choice[0], random_best_choice[1], random_best_choice[2])
            # コンピューターの棋譜も記録
            log.append(random_best_choice)
            print("log", log)
            # コンピューターが置いたマスのrow, columnから縦、横、斜めを再検査し、相手の石を挟むことができればマスに手番turnを登録する
            check_changeable_place(random_best_choice[0], random_best_choice[1], random_best_choice[2])
            root.update()
            root.after(random.randint(2000,5000), show_board_gui())
            play_sound_effect("place.mp3")
            # マスが一杯
            if is_full():
                is_win()
                print("log", log)
                break
            # マスに空きがある
            else:
                print("コンピューターになっているか", turn)
                change_turn() #人へ 
                print("人になっているか？", turn)
                check_board(turn)
                # 人が置くことができるマスがない
                if len(correct_place_list) == 0: 
                    root.update()
                    messagebox.showinfo('information', "置けるマスがないのでパス１")
                    # 棋譜にパス１を記録
                    pass_record = ["pass1"]
                    log.append(pass_record)
                    change_turn() # 再びコンピューターへ
                    check_board(turn)
                    # コンピューターも置くことができるマスがない
                    if len(correct_place_list) == 0: 
                        root.update()
                        messagebox.showinfo('information', "置けるマスがないのでパス2で勝敗を判定します")
                        is_win()
                    # コンピューターが置くことができるマスがある
                    else:
                        show_turn_gui()         
                # 人が置くことができるマスがある
                else:
                    print("人に戻っているか", turn)
                    show_turn_gui # 人の番
                    break
#
# 置けるマスのリストの各マスについてひっくり返せるマスの数を検査
def check_computer_stronger(row, column, turn):
    computer_get_sum = 0
    computer_get_sum += check_computer_stronger_vertical_upward(row, column, turn)
    computer_get_sum += check_computer_stronger_vertical_downward(row, column, turn)
    computer_get_sum += check_computer_stronger_horizontal_left(row, column, turn)
    computer_get_sum += check_computer_stronger_horizontal_right(row, column, turn)
    computer_get_sum += check_computer_stronger_diagonal_upward(row, column, turn)
    computer_get_sum += check_computer_stronger_diagonal_downward(row, column, turn)
    computer_get_sum += check_computer_stronger_inverse_diagonal_upward(row, column, turn)
    computer_get_sum += check_computer_stronger_inverse_diagonal_downward(row, column, turn)
    return computer_get_sum
#
def replay_log(log):
    # init_board()
    # init_turn()
    # show_board_gui()
    print("replay_log", log)
    for m in log:
        print(m)
        if len(m) == 3:
            print(m[0], m[1], m[2])
            # set_board(m[0], m[1], m[2])
            # check_changeable_place_vertical_upward(m[0], m[1], m[2])
            # check_changeable_place_vertical_downward(m[0], m[1], m[2])
            # check_changeable_place_horizontal_left(m[0], m[1], m[2])
            # check_changeable_place_horizontal_right(m[0], m[1], m[2])
            # check_changeable_place_diagonal_upward(m[0], m[1], m[2])   
            # check_changeable_place_diagonal_downward(m[0], m[1], m[2])                
            # check_changeable_place_inverse_diagonal_upward(m[0], m[1], m[2])
            # check_changeable_place_inverse_diagonal_downward(m[0], m[1], m[2])
            # show_board_gui()
            button_clicked(m[0], m[1])
        elif len(m) == 1:
            continue
        elif len(m) == 2:
            continue
            # print("RESULT IN LOG: ", m[0], m[1])

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
buttons = []

# ウィジェットの作成
def create_buttons(f, num_buttons_per_row, num_rows):
    global buttons
    for i in range(num_rows):
        button_row = []
        for j in range(num_buttons_per_row):
            # button_number = 1 * num_buttons_per_row + j + 1
            button = tk.Button(f, image = tk_space_image, command=lambda i=i, j=j: button_clicked(i,j), highlightbackground = '#000000')
            button.grid(row=i+2, column=j)
            button_row.append(button)
        buttons.append(button_row)

create_buttons(f, num_buttons_per_row, num_rows)
#
def change_sente_text():
    sente_button.config(text ="先手選択中")
    play_sound_effect("levelchoice.mp3")
    root.update()
    
#
def change_gote_text():
    gote_button.config(text = "後手選択中")
    play_sound_effect("levelchoice.mp3")
    root.update()
#
# 先手ボタン、後手ボタンの作成
sente_button = tk.Button(f,text = "先手", command = start, height = 1, width = 5, font = ('Helvetica, 20'), bg = '#ff0000')
gote_button = tk.Button(f, text = "後手", command = computer_start, height = 1, width = 5, font = ('Helvetica, 20'))
#
sente_button.grid(row=1, column=0, columnspan= 4)
gote_button.grid(row=1, column=4, columnspan=4)
#
# ラベル上のテキストを変換するStringVarのインスタンス
label_text = tk.StringVar(f)
label_text.set("対戦レベルを選んでください")
#
def init_label():
    label_text.set("対戦レベルを選んでください")
#
# 勝敗を表示するウィジェット
l = tk.Label(f, textvariable=label_text, height = 2, font = ('Helvetica, 28'))
l.grid(row=0, column=0, columnspan=8)
#
# RESETボタンの作成とウィジェットの割付
br = tk.Button(f, text="RESET", command = reset, height = 1, width = 3, font = ('Helvetica, 20'))
br.grid(row=10, column=0, columnspan=8)
#
# 対戦レベルの強めが押された時のラベル表示とレベルの保存　strongerはレベル１
def stronger_chosen():
    label_text.set("先手か後手を選んでください")
    global computer_level
    computer_level = 1
    play_sound_effect("levelchoice.mp3")
    root.update()
    
#
# 対戦レベルの弱めが押された時のラベル表示とレベルの保存　weakerはレベル0
def weaker_chosen():
    label_text.set("先手か後手を選んでください")
    global computer_level
    computer_level = 0
    play_sound_effect("levelchoice.mp3")
    root.update()
#
# 対戦コンピューターの対戦レベル表示
computer_level = tk.Label(f, text = "対戦\nレベル", font = ('Helvetica, 25'))
computer_level.grid(row=4, column=8)
#
# コンピューターレベル強のボタン作成
level_strong = tk.Button(f, text = "強め", command = stronger_chosen, font = ('Helvetica, 20'))
level_strong.grid(row=5, column=8)
#
# コンピューターレベル弱のボタン作成
level_weak = tk.Button(f, text = "弱め", command=weaker_chosen, font = ('Helvetica, 20'))
level_weak.grid(row=6, column=8)
#
root.mainloop()
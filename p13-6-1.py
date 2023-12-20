# 
# 三目並べ
#
import tkinter as tk
#
# 定数の定義
#
#
# play() の中で棋譜を作成する（要完成）
#
'三目並べのプログラムです'
OPEN = 0
FIRST = 1
SECOND = 2
DRAW = 3
#
# 恒常的な変数
#
turn = 1
board = [[0,0,0],[0,0,0],[0,0,0]]
game_over = False
#
# テスト用の棋譜
#
log1 = [[0, 0], [1, 1], [1, 0], [2, 0], [0, 2], [0, 1], [2, 1], [2, 2], [1, 2],[DRAW]]
log2 = [[0, 0], [1, 0], [1, 1], [2, 2], [0, 1], [2, 0],[FIRST]]
log3 = [[0, 1], [0, 0], [2, 1], [1, 1], [2, 2], [2, 0], [1, 0], [0, 2],[SECOND]]
#
# 手番関連の関数
#
# #  手番を文字列に
# #
# def show_turn():
#     '手番を示す文字列を返す'
#     if turn == FIRST:
#         return('先手')
#     elif turn == SECOND:
#         return('後手')
#     else:
#         return('手番の値が不適切です')
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
    if turn == FIRST:
        turn = SECOND
    elif turn == SECOND:
        turn = FIRST
#
# 手番関連の関数のテスト
# 
# def test_turn():
#     '手番をテストする'
#     init_turn()
#     print(show_turn(),"の番です")
#     change_turn()
#     print(show_turn(),"の番です")
#     change_turn()
#     print(show_turn(),"の番です")
#
# 盤面関連の関数
#
# 盤面を表示する文字列
#
def show_board():
    '盤面を表す文字列を返す'
    s =  ' : 0 1 2\n---------\n'
    for i in range(3):
        s = s + str(i) + ': '
        for j in range(3):
            cell = ''
            if board[i][j] == OPEN:
                cell = ' '
            elif board[i][j] == FIRST:
                cell = 'o'
            elif board[i][j] == SECOND:
                cell = 'x'
            else:
                cell = '?'
            s = s + cell + ' '
        s = s + '\n'
    return s

# 盤面を表示するGUI
def show_board_gui():
    '盤面を表す文字列を返す'
    for i in range(3):
        for j in range(3):
            if board[i][j] == OPEN:
                button_labels[i][j].set(' ')
            elif board[i][j] == FIRST:
                button_labels[i][j].set('⭕')
            elif board[i][j] == SECOND:
                button_labels[i][j].set('❌')
            else:
                button_labels[i][j].set('?')

# クリック時に動作させる関数
# def click_button():
#     if turn == 1:
#         text.set("o")
#         set_board()
#     else:
#         text.set("x")
#         set_board()
#
# 盤面の初期化
#
def init_board():
    '盤面をすべて空(OPEN)に初期化する'
    for i in range(3):
        for j in range(3):
            board[i][j] = OPEN
#
# 盤面の i, j の位置の値を返す
#
def examine_board(i,j):
    '盤面の i 行 j 行の値を返す'
    return board[i][j]
#
# 盤面の i j に手番を t を登録、状態を文字列で返す
#
def set_board(i, j, t):
    '''
盤面の i j に手番 t を登録、状態を文字列で返す
返す値は
  'ok' 成功
  'Not empty' 空いている場所ではない
  'illegal turn' 手番が正しくない
  'illegal slot' 指定された場所が正しくない
  '''
    if (i>=0) and (i<3) and (j>=0) and (j<3):
        if (t>0) and (t<3):
            if examine_board(i, j) == 0:
                board[i][j] = t
                return 'ok'
            else:
                return 'Not empty'
        else:
            return 'illegal turn'
    else:
        return 'illegal slot'

# 盤面のi, jをボタンから受け取って処理
def button_clicked(i,j):
    global game_over
    if board[i][j] != OPEN:
        label_text.set("Error")
        return
    if game_over:
        return
    set_board(i, j, turn)
    print(show_board())
    show_board_gui()
    if is_draw():
        game_over = True
        label_text.set("引き分け")
    if is_win_actual(turn):
        game_over = True
        if turn == FIRST:
            label_text.set("⭕の勝ち")    
        elif turn == SECOND:
            label_text.set("❌の勝ち")
    change_turn()

# resetボタンで手番と盤面を初期化
def reset():
    global game_over
    init_turn()
    init_board()
    for i in button_labels:
        for j in i:
            j.set(' ')
    init_label()
    game_over = False

def init_label():
    label_text.set("Tic-Tac-Toe")

# tkinter での画面の構成
root = tk.Tk()
f = tk.Frame(root)
f.grid() 

# StringVarのインスタンスを格納する変数button_labelsのリスト
button_labels = [[tk.StringVar(f), tk.StringVar(f), tk.StringVar(f)], [tk.StringVar(f), tk.StringVar(f), tk.StringVar(f)], [tk.StringVar(f), tk.StringVar(f), tk.StringVar(f)]]
for i in button_labels:
    for j in i:
       j.set(' ')

# ウィジェットの作成
b1 = tk.Button(f, textvariable=button_labels[0][0], command=lambda:button_clicked(0,0), height=3, width=3)
b2 = tk.Button(f, textvariable=button_labels[0][1], command=lambda:button_clicked(0,1), height=3, width=3)
b3 = tk.Button(f, textvariable=button_labels[0][2], command=lambda:button_clicked(0,2), height=3, width=3)
b4 = tk.Button(f, textvariable=button_labels[1][0], command=lambda:button_clicked(1,0), height=3, width=3)
b5 = tk.Button(f, textvariable=button_labels[1][1], command=lambda:button_clicked(1,1), height=3, width=3)
b6 = tk.Button(f, textvariable=button_labels[1][2], command=lambda:button_clicked(1,2), height=3, width=3)
b7 = tk.Button(f, textvariable=button_labels[2][0], command=lambda:button_clicked(2,0), height=3, width=3)
b8 = tk.Button(f, textvariable=button_labels[2][1], command=lambda:button_clicked(2,1), height=3, width=3)
b9 = tk.Button(f, textvariable=button_labels[2][2], command=lambda:button_clicked(2,2), height=3, width=3)
br = tk.Button(f, text='Reset',command=reset)

# Grid 型ジオメトリマネージャによるウィジェットの割付
b1.grid(row=1, column=0)
b2.grid(row=1, column=1)
b3.grid(row=1, column=2)
b4.grid(row=2, column=0)
b5.grid(row=2, column=1)
b6.grid(row=2, column=2)
b7.grid(row=3, column=0)
b8.grid(row=3, column=1)
b9.grid(row=3, column=2)
br.grid(row=4, column=0, columnspan=3)

# ラベル上のテキストを変換するStringVarのインスタンス
label_text = tk.StringVar(f)
label_text.set("Tic-Tac-Toe")

# 勝敗を表示するウィジェット
l = tk.Label(f, textvariable=label_text)
l.grid(row=0, column=0, columnspan=3)
#
# 盤面のテスト関数
#
def test_board1():
    '盤面についてのテストプログラムの１つめです'
    init_board()
    print(show_board())
    print(set_board(0,0,1))
    print(show_board())
    print(set_board(1,1,2))
    print(show_board())
    print(set_board(1,1,1))
    print(show_board())
#
# 水平方向での手番 t の勝ちの判定
#
def check_board_horizontal(t):
    '水平方向に手番 t が勝ちであることを判定します'
    for i in range (3):
        if (board[i][0] == t) and (board[i][1] == t) and (board[i][2] == t):
            return True
    return False
#
# 垂直方向での手番 t の勝ちの判定
#
def check_board_vertical(t):
    '垂直方向に手番 t が勝ちであることを判定します'
    for j in range (3):
        if (board[0][j] == t) and (board[1][j] == t) and (board[2][j] == t):
            return True
    return False
#
# 対角方向での手番 t の勝ちの判定
#
def check_board_diagonal(t):
    '対角方向に手番 t が勝ちであることを判定します'
    if (board[0][0] == t) and (board[1][1] == t) and (board[2][2] == t):
        return True
    return False
#
# 逆対角方向での手番 t の勝ちの判定
#
def check_board_inverse_diagonal(t):
    '逆対角方向に手番 t が勝ちであることを判定します'
    if (board[0][2] == t) and (board[1][1] == t) and (board[2][0] == t):
        return True
    return False
#
# 手番 t の勝ちの単純な判定
#
def is_win_simple(t):
    '手番 t が勝ちであることを判定します。相手が勝っていることはチェックしません'
    if check_board_horizontal(t):
        return True
    if check_board_vertical(t):
        return True
    if check_board_diagonal(t):
        return True
    if check_board_inverse_diagonal(t):
        return True
    return False
#
# 相手が勝っていないことを確認しての勝ちの判定
#
def is_win_actual(t):
    '手番 t が勝ちであることを判定します。相手が勝っていないことも確認します'
    if not is_win_simple(t):
        return False
    if t==FIRST:
        if is_win_simple(SECOND):
            return False
    else:
        if is_win_simple(FIRST):
            return False
    return True
#
# 盤面が埋まっていることの判定
# 
def is_full():
    '盤面に空きがないことを確認します'
    for i in range(3):
        for j in range(3):
            if board[i][j] == OPEN:
                return False
    return True
#
# 引き分けの判定
#
def is_draw():
    '盤面が引き分けであることを判定します'
    if is_win_simple(FIRST):
        return False
    if is_win_simple(SECOND):
        return False
    if not is_full():
        return False
    return True
#
# 盤面のテスト関数２つめ、勝ち判定のテスト
#
def test_board2():
    '盤面をテストする関数の２番目'
    init_board()
    board[0][0] = FIRST
    board[1][0] = FIRST
    board[2][0] = FIRST
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    init_board()
    board[0][0] = SECOND
    board[1][0] = SECOND
    board[2][0] = SECOND
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL_FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))

    init_board()
    board[0][0] = FIRST
    board[0][1] = FIRST
    board[0][2] = FIRST
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTAL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    init_board()
    board[0][0] = SECOND
    board[0][1] = SECOND
    board[0][2] = SECOND
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    
    init_board()
    board[0][0] = FIRST
    board[1][1] = FIRST
    board[2][2] = FIRST
    print(show_board())
    print("DIAGONAL FIRST: " , check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGONAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
    init_board()
    board[0][0] = SECOND
    board[1][1] = SECOND
    board[2][2] = SECOND
    print(show_board())
    print("DIAGONAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGONAL SECOND: "  ,check_board_inverse_diagonal(SECOND))

    init_board()
    board[0][2] = FIRST
    board[1][1] = FIRST
    board[2][0] = FIRST
    print(show_board())
    print("DIAGLNAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGLNAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGONAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
    init_board()
    board[0][2] = SECOND
    board[1][1] = SECOND
    board[2][0] = SECOND
    print(show_board())
    print("DIAGONAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_inverse_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGONAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
#
# 盤面のテスト関数３、勝ち、引き分けの判定
# 
def test_board3():
    '盤面をテストする関数の３番目'
    init_board()
    board[0][0] = FIRST
    board[1][0] = FIRST
    board[2][0] = SECOND
    board[0][1] = SECOND
    board[1][1] = SECOND
    board[2][1] = FIRST
    board[0][2] = FIRST
    board[1][2] = FIRST
    board[2][2] = SECOND
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    print("DIAGONAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGLNAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
    print("IS WIN SIMPLE FIRST", is_win_simple(FIRST))
    print("IS WIN SIMPLE SECOND", is_win_simple(SECOND))
    print("IS WIN ACTUAL FIRST", is_win_actual(FIRST))
    print("IS WIN ACTUAL SECOND", is_win_actual(SECOND))
    print("IS FULL", is_full())
    print("IS DRAW", is_draw())

    init_board()
    board[0][0] = FIRST
    board[1][0] = SECOND
    board[2][0] = FIRST
    board[0][1] = SECOND
    board[1][1] = FIRST
    board[2][1] = OPEN
    board[0][2] = FIRST
    board[1][2] = OPEN
    board[2][2] = SECOND
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    print("DIAGONAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGONAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGONAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
    print("IS WIN SIMPLE FIRST", is_win_simple(FIRST))
    print("IS WIN SIMPLE SECOND", is_win_simple(SECOND))
    print("IS WIN ACTUAL FIRST", is_win_actual(FIRST))
    print("IS WIN ACTUAL SECOND", is_win_actual(SECOND))
    print("IS FULL", is_full())
    print("IS DRAW", is_draw())

    init_board()
    board[0][0] = SECOND
    board[1][0] = FIRST
    board[2][0] = SECOND
    board[0][1] = FIRST
    board[1][1] = SECOND
    board[2][1] = FIRST
    board[0][2] = SECOND
    board[1][2] = OPEN
    board[2][2] = FIRST
    print(show_board())
    print("HORIZONTSL FIRST: " ,check_board_horizontal(FIRST))
    print("HORIZONTSL SECOND: ",check_board_horizontal(SECOND))
    print("VERTICAL FIRST: "   ,check_board_vertical(FIRST))
    print("VERTICAL SECOND: "  ,check_board_vertical(SECOND))
    print("DIAGONAL FIRST: " ,check_board_diagonal(FIRST))
    print("DIAGONAL SECOND: ",check_board_diagonal(SECOND))
    print("INV DIAGLNAL FIRST: "   ,check_board_inverse_diagonal(FIRST))
    print("INV DIAGLNAL SECOND: "  ,check_board_inverse_diagonal(SECOND))
    print("IS WIN SIMPLE FIRST", is_win_simple(FIRST))
    print("IS WIN SIMPLE SECOND", is_win_simple(SECOND))
    print("IS WIN ACTUAL FIRST", is_win_actual(FIRST))
    print("IS WIN ACTUAL SECOND", is_win_actual(SECOND))
    print("IS FULL", is_full())
    print("IS DRAW", is_draw())
#
#  ログのリプレイ
# 
def replay_log(log):
    '棋譜 log をたどります。print 文で画面に出力します'
    init_board()
    init_turn()
    print(show_board())
    for m in log:
        if len(m) == 2:
            print(show_turn(),"の番です")
            print(set_board(m[0], m[1], turn))
            print(show_board())
            print("IS WIN", turn, ": ", is_win_actual(turn))
            change_turn()
        else:
            print("RESULT IN LOG:",m[0])
    print("IS WIN FIRST: ", is_win_actual(FIRST))
    print("IS WIN SECOND: ", is_win_actual(SECOND))
    print("IS DRAW: ", is_draw())
#
# ログのテスト
#
def test_log():
    '棋譜をテストします'
    print("LOG1")
    replay_log(log1)
    print("LOG2")
    replay_log(log2)
    print("LOG3")
    replay_log(log3)
#
#   すべてのテスト
#
def test_all():
    'すべてのテストを行います'
    test_turn()
    test_board1()
    test_board2()
    test_board3()
    test_log()
#
# 実際のプレイ
#
# def play():
#     '端末への入出力を用いて実際に三目並べをプレイする関数です'
#     init_turn()
#     init_board()
#     # print(show_board())
# # 棋譜用の空リストを作る。play() の外側でアクセスするなら global 宣言
# #  global log
#     log = []
#     while True:
#         # print(show_turn(),"の番です")
#         while(True):
#             row = int(input("行を入力してください"))
#             column = int(input("列を入力してください: "))
#             sashite = [row, column]
#             print(sashite)
#             result = set_board(row, column, turn)
#             print(result)
#             if result == "ok":
#                 break
#             print("不適切な入力です。再度、入力して下さい")
#         # ここ（内側の while の外）で log に手を追加
#         #
#         # 要追加
#         log.append(sashite)
#         #
#         print(show_board())
#         if is_draw():
#             print("引き分けです")
#             # ここで棋譜に勝敗（引き分け）を追加
#             log.append([DRAW])
#             break
#         if is_win_actual(turn):
#             print(show_turn(), "の勝ちです")
#             # ここで棋譜に勝敗（turn の勝ち）を追加
#             log.append([turn])
#             break
#         change_turn()
#     # ここで棋譜のリプレイ
#     # 現在は log は空なので判定して処理
#     print("-----------------------------------")
#     if len(log)>0:
#         replay_log(log)
#     else:
        # print("棋譜は作成されていません")
if __name__ == '__main__':
    print('三目並べ')

root.mainloop()

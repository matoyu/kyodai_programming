# 
# 三目並べ(GUI)対コンピューター
#
import tkinter as tk
import random
import time
#
# 初期化メソッド
class Sanmokunarabe():
    def __init__(self):
        self.OPEN = 0
        self.FIRST = 1
        self.SECOND = 2
        self.DRAW = 3
        self.turn = 1
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.game_over = False
        self.frame()
        self.root.mainloop()
    #
    '三目並べのプログラムです'
    #
    def init_turn(self):
        '手番を初期化する'
        self.turn = 1
    #
    # 手番の交代
    #
    def change_turn(self):
        '手番を交代する'
        if self.turn == self.FIRST:
            self.turn = self.SECOND
        elif self.turn == self.SECOND:
            self.turn = self.FIRST
    #
    # 盤面関連の関数
    #
    # 盤面を表示する文字列
    #
    def show_board(self):
        '盤面を表す文字列を返す'
        s =  ' : 0 1 2\n---------\n'
        for i in range(3):
            s = s + str(i) + ': '
            for j in range(3):
                cell = ''
            if self.board[i][j] == self.OPEN:
                cell = ' '
            elif self.board[i][j] == self.FIRST:
                cell = 'o'
            elif self.board[i][j] == self.SECOND:
                cell = 'x'
            else:
                cell = '?'
            s = s + cell + ' '
        s = s + '\n'
        return s

    # 盤面を表示するGUI
    def show_board_gui(self):
        '盤面を表す文字列を返す'
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.OPEN:
                    self.button_labels[i][j].set(' ')
                elif self.board[i][j] == self.FIRST:
                    self.button_labels[i][j].set('⭕')
                elif self.board[i][j] == self.SECOND:
                    self.button_labels[i][j].set('❌')
                else:
                    self.button_labels[i][j].set('?')
    #
    # 盤面の初期化
    #
    def init_board(self):
        '盤面をすべて空(OPEN)に初期化する'
        for i in range(3):
            for j in range(3):
                self.board[i][j] = self.OPEN
    #
    # 盤面の i, j の位置の値を返す
    #
    def examine_board(self,i,j):
        '盤面の i 行 j 行の値を返す'
        return self.board[i][j]
    #
    # 盤面の i j に手番を t を登録、状態を文字列で返す
    #
    def set_board(self,i, j, t):
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
                if self.examine_board(i, j) == 0:
                    self.board[i][j] = t
                    return 'ok'
                else:
                    return 'Not empty'
            else:
                return 'illegal turn'
        else:
            return 'illegal slot'
        
    # コンピュータがプレイ
    def computer(self):
        while True:
            i = random.randint(0, 2)
            j = random.randint(0, 2)
            if self.board[i][j] == self.OPEN:
                break
        if self.board[i][j] != self.OPEN:
            self.label_text.set("Error")
            return
        if self.game_over == True:
            return
        self.set_board(i, j, self.turn)
        print(self.show_board())
        self.show_board_gui()
        if self.is_draw():
            self.game_over = True
            self.label_text.set("引き分け")
        if self.is_win_actual(self.turn):
            self.game_over = True
            if self.turn == self.FIRST:
                self.label_text.set("⭕の勝ち")
            elif self.turn == self.SECOND:
                self.label_text.set("❌の勝ち")
        self.change_turn()        

    # 盤面のi, jをボタンから受け取って処理
    def button_clicked(self,i,j):
        if self.board[i][j] != self.OPEN:
            self.label_text.set("Error")
            return
        if self.game_over == True:
            return
        self.set_board(i, j, self.turn)
        print(self.show_board())
        self.show_board_gui()
        if self.is_draw():
            self.game_over = True
            self.label_text.set("引き分け")
        if self.is_win_actual(self.turn):
            self.game_over = True
            if self.turn == self.FIRST:
                self.label_text.set("⭕の勝ち")
            elif self.turn == self.SECOND:
                self.label_text.set("❌の勝ち")
        self.change_turn()
        self.root.after(1000, self.computer)

    # resetボタンで手番と盤面を初期化
    def reset(self):
        self.init_turn()
        self.init_board()
        for i in self.button_labels:
            for j in i:
                j.set(' ')
        self.init_label()
        self.game_over = False

    def init_label(self):
        self.label_text.set("Tic-Tac-Toe")

    # tkinter での画面の構成
    def frame(self):
        self.root = tk.Tk()
        self.f = tk.Frame(self.root)
        self.f.grid() 

        # StringVarのインスタンスを格納する変数button_labelsのリスト
        self.button_labels = [[tk.StringVar(self.f), tk.StringVar(self.f), tk.StringVar(self.f)], [tk.StringVar(self.f), tk.StringVar(self.f), tk.StringVar(self.f)], [tk.StringVar(self.f), tk.StringVar(self.f), tk.StringVar(self.f)]]
        for i in self.button_labels:
            for j in i:
                j.set(' ')

        #   ウィジェットの作成
        b1 = tk.Button(self.f, textvariable=self.button_labels[0][0], command=lambda:self.button_clicked(0,0), height=3, width=3)
        b2 = tk.Button(self.f, textvariable=self.button_labels[0][1], command=lambda:self.button_clicked(0,1), height=3, width=3)
        b3 = tk.Button(self.f, textvariable=self.button_labels[0][2], command=lambda:self.button_clicked(0,2), height=3, width=3)
        b4 = tk.Button(self.f, textvariable=self.button_labels[1][0], command=lambda:self.button_clicked(1,0), height=3, width=3)
        b5 = tk.Button(self.f, textvariable=self.button_labels[1][1], command=lambda:self.button_clicked(1,1), height=3, width=3)
        b6 = tk.Button(self.f, textvariable=self.button_labels[1][2], command=lambda:self.button_clicked(1,2), height=3, width=3)
        b7 = tk.Button(self.f, textvariable=self.button_labels[2][0], command=lambda:self.button_clicked(2,0), height=3, width=3)
        b8 = tk.Button(self.f, textvariable=self.button_labels[2][1], command=lambda:self.button_clicked(2,1), height=3, width=3)
        b9 = tk.Button(self.f, textvariable=self.button_labels[2][2], command=lambda:self.button_clicked(2,2), height=3, width=3)
        br = tk.Button(self.f, text='Reset',command=self.reset)

        #   Grid 型ジオメトリマネージャによるウィジェットの割付
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

        #   ラベル上のテキストを変換するStringVarのインスタンス
        self.label_text = tk.StringVar(self.f)
        self.label_text.set("Tic-Tac-Toe")

        # 勝敗を表示するウィジェット
        l = tk.Label(self.f, textvariable=self.label_text)
        l.grid(row=0, column=0, columnspan=3)
    # 
    # 水平方向での手番 t の勝ちの判定
    #
    def check_board_horizontal(self,t):
        '水平方向に手番 t が勝ちであることを判定します'
        for i in range (3):
            if (self.board[i][0] == t) and (self.board[i][1] == t) and (self.board[i][2] == t):
                return True
        return False
    #
    # 垂直方向での手番 t の勝ちの判定
    #
    def check_board_vertical(self,t):
        '垂直方向に手番 t が勝ちであることを判定します'
        for j in range (3):
            if (self.board[0][j] == t) and (self.board[1][j] == t) and (self.board[2][j] == t):
                return True
        return False
    #
    # 対角方向での手番 t の勝ちの判定
    #
    def check_board_diagonal(self,t):
        '対角方向に手番 t が勝ちであることを判定します'
        if (self.board[0][0] == t) and (self.board[1][1] == t) and (self.board[2][2] == t):
            return True
        return False
    #
    # 逆対角方向での手番 t の勝ちの判定
    #
    def check_board_inverse_diagonal(self,t):
        '逆対角方向に手番 t が勝ちであることを判定します'
        if (self.board[0][2] == t) and (self.board[1][1] == t) and (self.board[2][0] == t):
            return True
        return False
    #
    # 手番 t の勝ちの単純な判定
    #
    def is_win_simple(self,t):
        '手番 t が勝ちであることを判定します。相手が勝っていることはチェックしません'
        if self.check_board_horizontal(t):
            return True
        if self.check_board_vertical(t):
            return True
        if self.check_board_diagonal(t):
            return True
        if self.check_board_inverse_diagonal(t):
            return True
        return False
    #
    # 相手が勝っていないことを確認しての勝ちの判定
    #
    def is_win_actual(self,t):
        '手番 t が勝ちであることを判定します。相手が勝っていないことも確認します'
        if not self.is_win_simple(t):
            return False
        if t==self.FIRST:
            if self.is_win_simple(self.SECOND):
                return False
        else:
            if self.is_win_simple(self.FIRST):
                return False
        return True
    #
    # 盤面が埋まっていることの判定
    # 
    def is_full(self):
        '盤面に空きがないことを確認します'
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == self.OPEN:
                    return False
        return True
    #
    # 引き分けの判定
    #
    def is_draw(self):
        '盤面が引き分けであることを判定します'
        if self.is_win_simple(self.FIRST):
            return False
        if self.is_win_simple(self.SECOND):
            return False
        if not self.is_full():
            return False
        return True
    

if __name__ == '__main__':
    print('三目並べ')
    sanmokunarabe = Sanmokunarabe()
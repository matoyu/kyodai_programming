import tkinter as tk

# 計算機能のための変数とイベント用の関数定義
# Frame のサブクラスを使った実装例

# 2項演算のモデル
# 入力中の数字
current_number = 0
# 第一項
first_term = 0
# 第二項
second_term = 0
# 結果
result = 0

def do_plus():
    "+ キーが押された時の計算動作, 第一項の設定と入力中の数字のクリア"
    global current_number
    global first_term
    first_term = current_number
    current_number = 0

def do_eq():
    # "= キーが押されたときの計算動作, 第二項の設定, 加算の実施, 入力中の数字のクリア"
    global second_term
    global result
    global current_number
    second_term = current_number
    result = first_term + second_term
    current_number = 0
#
# tk.Frame を継承した MyFrameというクラスを作り
# その中でウィジェットやコールバック関数(メソッド)を
# 設定する, tkinter をつかう定番
#
class MyFrame(tk.Frame):
#
#    __init__ はクラスオブジェクトを作る際の初期化メソッド
# アンダースコアは前後それぞれ２つずつ
    def __init__(self, master = None):
        super().__init__(master)
# あとで参照しないウィジェットの作成, ローカル変数
        b1 = tk.Button(self, text='1', command=lambda:self.key(1))  
        b2 = tk.Button(self, text='2', command=lambda:self.key(2))        
        b3 = tk.Button(self, text='3', command=lambda:self.key(3))        
        b4 = tk.Button(self, text='4', command=lambda:self.key(4))        
        b5 = tk.Button(self, text='5', command=lambda:self.key(5))        
        b6 = tk.Button(self, text='6', command=lambda:self.key(6))        
        b7 = tk.Button(self, text='7', command=lambda:self.key(7))        
        b8 = tk.Button(self, text='8', command=lambda:self.key(8))        
        b9 = tk.Button(self, text='9', command=lambda:self.key(9))        
        b0 = tk.Button(self, text='0', command=lambda:self.key(0))        
        bc = tk.Button(self, text='C', command=self.clear)        
        bp = tk.Button(self, text='+', command=self.plus)        
        be = tk.Button(self, text='=', command=self.eq)

# Grid 型ジオメトリマネージャによるウィジェット割付
        b1.grid(row=3, column=0)
        b2.grid(row=3, column=1)
        b3.grid(row=3, column=2)
        b4.grid(row=2, column=0)
        b5.grid(row=2, column=1)
        b6.grid(row=2, column=2)
        b7.grid(row=1, column=0)
        b8.grid(row=1, column=1)
        b9.grid(row=1, column=2)
        b0.grid(row=4, column=0)
        bc.grid(row=1, column=3)
        be.grid(row=4, column=3)
        bp.grid(row=2, column=3)

# 他のメソッドで参照する数値を表示するウィジェット, 
# クラスオブジェクトの変数として作成, 頭に self. がつく
#
        self.e = tk.Entry(self)
        self.e.grid(row=0, column=0, columnspan=4)
# クラスの定義では
# メソッドの最初の引数は self, 中でクラスオブジェクトの変数, 
# メソッドは self をつけて参照
#
    def key(self, n):
        global current_number
        current_number = current_number * 10 + n
        self.show_number(current_number)

    def clear(self):
        global current_number
        current_number = 0
        self.show_number(current_number)

    def plus(self):
        do_plus()
        self.show_number(current_number)

    def eq(self):
        do_eq()
        self.show_number(result)

    def show_number(self, num):
        self.e.delete(0, tk.END)
        self.e.insert(0, str(num))

#
# ここからメインプログラム
#
root = tk.Tk()
f = MyFrame(root)
f.pack()
f.mainloop()
import tkinter as tk

# 初期化メソッド
class Dentaku():
    def __init__(self):
        self.current_number = 0
        self.first_term = 0
        self.second_term = 0
        self.result = 0
        self.frame()
        self.root.mainloop()

    # 計算を実行するメソッド    
    def do_plus(self):
        self.first_term = self.current_number
        self.current_number = 0

    def do_eq(self):
        self.second_term = self.current_number
        self.result = self.first_term + self.second_term
        self.current_number = 0


    # 数字キーのCall Back 関数　key1の内容
    def key1(self):
        self.key(1)

    def key2(self):
        self.key(2)

    def key3(self):
        self.key(3)

    def key4(self):
        self.key(4)         

    def key5(self):
        self.key(5)

    def key6(self):
        self.key(6)

    def key7(self):
        self.key(7)

    def key8(self):
        self.key(8)

    def key9(self):
        self.key(9)

    def key0(self):
        self.key(0)       

    # 数字キーを一括処理する関数  
    def key(self,n):
        self.current_number = self.current_number * 10 + n
        self.show_number(self.current_number)
        
    def clear(self):
        self.current_number = 0
        self.show_number(self.current_number)

    def plus(self):
        self.do_plus()
        self.show_number(self.curent_number)

    def eq(self):
        self.do_eq()
        self.show_number(self.result)    

    def show_number(self, num):
        self.e.delete(0, tk.END)
        self.e.insert(0, str(num))

    # tkinter での画面の構成
    def frame(self):
        self.root = tk.Tk()
        self.f = tk.Frame(self.root)
        self.f.grid()

        #  ウィジェットの作成

        b1 = tk.Button(self.f, text='1', command=self.key1)
        b2 = tk.Button(self.f, text='2', command=self.key2)
        b3 = tk.Button(self.f, text='3', command=self.key3)
        b4 = tk.Button(self.f, text='4', command=self.key4)
        b5 = tk.Button(self.f, text='5', command=self.key5)
        b6 = tk.Button(self.f, text='6', command=self.key6)
        b7 = tk.Button(self.f, text='7', command=self.key7)
        b8 = tk.Button(self.f, text='8', command=self.key8)
        b9 = tk.Button(self.f, text='9', command=self.key9)
        b0 = tk.Button(self.f, text='0', command=self.key0)
        bc = tk.Button(self.f, text='C', command=self.clear)
        bp = tk.Button(self.f, text='+', command=self.plus)
        be = tk.Button(self.f, text='=', command=self.eq)

        # Grid 型ジオメトリマネージャにるウィジェットの割付

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

        self.e = tk.Entry(self.f)
        self.e.grid(row=0, column=0, columnspan=4)
        self.clear()

# ここからメインプログラム
dentaku = Dentaku()

dentaku1 = Dentaku()

dentaku2 = Dentaku()


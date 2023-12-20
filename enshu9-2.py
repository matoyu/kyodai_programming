import tkinter as tk
import tkmacosx as mactk

# 計算機能のための変数とイベント用の関数定義

# 2 項演算のモデル
# 入力中の数字
current_number = 0
# 第一項
first_term = 0
# 第二項
second_term = 0
# 結果
result = 0
# 第一項の保存
next_operation = "nothing"

def do_divide():
    "/ キーが押された時の計算動作, 第一項の設定と入力中の数字のクリア"
    global current_number
    global first_term
    first_term = current_number
    current_number = 0
    global next_operation
    next_operation = "divide"

def do_divide_eq():
    "= キーが押されたときの計算動作, 第二項の設定, 徐算の実施, 入力中の数字のクリア"
    global second_term
    global result
    global current_number
    second_term = current_number
    if second_term == 0:
        e.delete(0, tk.END)
        e.insert(0, 'Error')
    else:    
        result = first_term // second_term
        show_number(result)
        current_number = 0

def do_times():
    "/ キーが押された時の計算動作, 第一項の設定と入力中の数字のクリア"
    global current_number
    global first_term
    first_term = current_number
    current_number = 0
    global next_operation
    next_operation = "times"

def do_times_eq():
    "= キーが押されたときの計算動作, 第二項の設定, 乗算の実施, 入力中の数字のクリア"
    global second_term
    global result
    global current_number
    second_term = current_number
    result = first_term * second_term
    current_number = 0

def do_minus():
    "- キーが押された時の計算動作, 第一項の設定と入力中の数字のクリア"
    global current_number
    global first_term
    first_term = current_number
    current_number = 0
    global next_operation
    next_operation = "minus"

def do_minus_eq():
    "= キーが押されたときの計算動作, 第二項の設定, 減算の実施, 入力中の数字のクリア"
    global second_term
    global result
    global current_number
    second_term = current_number
    result = first_term - second_term
    current_number = 0

def do_plus():
    "+ キーが押された時の計算動作, 第一項の設定と入力中の数字のクリア"
    global current_number
    global first_term
    first_term = current_number
    current_number = 0
    global next_operation
    next_operation = "plus"

def do_plus_eq():
    "= キーが押されたときの計算動作, 第二項の設定, 加算の実施, 入力中の数字のクリア"
    global second_term
    global result
    global current_number
    second_term = current_number
    result = first_term + second_term
    current_number = 0

# 数字キーを一括処理する関数
def key(n):
    global current_number
    current_number = current_number * 10 + n
    show_number(current_number)

def clear():
    global current_number
    current_number = 0
    show_number(current_number)

def divide():
    do_divide()

def divide_eq():
    do_divide_eq()

def times():
    do_times()

def times_eq():
    do_times_eq()
    show_number(result)
 
def minus():
    do_minus()

def minus_eq():
    do_minus_eq()
    show_number(result)

def plus():
    do_plus()

def plus_eq():
    do_plus_eq()
    show_number(result)

def show_number(num):
    e.delete(0, tk.END)
    e.insert(0, str(num)) 

# tkinter での画面の構成

root = tk.Tk()
f = tk.Frame(root)
f.configure(background = '#ffffc0')
f.grid()

def calculation():
    # 加減乗除の計算
    if next_operation == "divide":
        divide_eq()
    elif next_operation == "times":
        times_eq()
    elif next_operation == "minus":
        minus_eq()
    elif next_operation == "plus":
        plus_eq()

# ウィジェットの作成
# tk.Buttonの代わりにtk
b1 = mactk.Button(f, text='1', command=lambda:key(1))
b2 = mactk.Button(f, text='2', command=lambda:key(2))
b3 = mactk.Button(f, text='3', command=lambda:key(3))
b4 = mactk.Button(f, text='4', command=lambda:key(4))
b5 = mactk.Button(f, text='5', command=lambda:key(5))
b6 = mactk.Button(f, text='6', command=lambda:key(6))
b7 = mactk.Button(f, text='7', command=lambda:key(7))
b8 = mactk.Button(f, text='8', command=lambda:key(8))
b9 = mactk.Button(f, text='9', command=lambda:key(9))
b0 = mactk.Button(f, text='0', command=lambda:key(0))
number_key = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b0]
for i in number_key:
    i.configure(background = '#ffffff', width=80, borderless=True, font = ('Helvetica', 14))
    # i["size"] = 2
bc = mactk.Button(f, text='C', command=clear)
bc.configure(background = '#ff0000', borderless=True, font = ('Helvetica', 14))
bd = mactk.Button(f, text='/', command=divide)
bd.configure(background = '#00ff00', borderless=True, font = ('Helvetica', 14))
bt = mactk.Button(f, text='*', command=times)
bt.configure(background = '#00ff00', borderless=True, font = ('Helvetica', 14))
bm = mactk.Button(f, text='-', command=minus)
bm.configure(background = '#00ff00', borderless=True, font = ('Helvetica', 14))
bp = mactk.Button(f, text='+', command=plus)
bp.configure(background = '#00ff00', borderless=True, font = ('Helvetica', 14))
be = mactk.Button(f, text='=', command=calculation)
be.configure(background = '#00ff00', borderless=True, font = ('Helvetica', 14))

# Grid 型ジオメトリマネージャによるウィジェットの割付

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
bc.grid(row=4, column=1)
be.grid(row=4, column=2)
bd.grid(row=1, column=3)
bt.grid(row=2, column=3)
bm.grid(row=3, column=3)
bp.grid(row=4, column=3)

# 数値を表示するウィジェット
e = tk.Entry(f, font = ('Helvetica', 14))
e.grid(row=0, column=0, columnspan=4)
clear()

# ここから GUI がスタート
root.mainloop()
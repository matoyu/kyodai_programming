import tkinter as tk
import tkinter.filedialog
import math
#
# tkinter の filedialog だけを利用する例
#
# root ウインドウはwithdraw() メソッドを読んで隠す
root = tk.Tk()
root.withdraw()
#
# 書き出し用の filedialog を読んでファイル名を得る
#
filename = tkinter.filedialog.asksaveasfilename()
#
# tkinter は終了する
#
root.destroy()
#
# ファイル名がもらえなければ終了
#
if filename:
    pass
else:
    print("No file specified")
    exit()
#
# 正弦波の重ね合わせで鋸波を近似する
# 
# w = sin(t) + sin(3t)/3 + sin(5t)/5 + sin(7t)/7 ...

# 2周期分, 全体は1000 ステップで, 高周波５番目まで
# 
cycles = 2
steps = 1000
harmonics = 5
# ファイルが開けないときのエラー対応
try:
# ファイルを開く
    with open(filename,'w') as file:
        for i in range(steps):
            angle_in_degree = 360*cycles*i/steps
            angle = math.radians(angle_in_degree)
            s = str(angle_in_degree)
            w = 0
            for j in range(1,harmonics*2+1):
                if j%2 == 1:
                    w += math.sin(angle*j)/j
                    s = s+", "+ str(w)
                else:
                    pass
        #    print(s)
            file.write(s+"\n")
        print("Writing to file "+ filename + " is finished")
except IOError:
    print("Unable to open file")
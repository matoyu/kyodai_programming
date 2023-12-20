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
# w = sin(t) + sin(2t)/2 + sine(3t)/3 + sin(4t)/4 ...

# 2周期分, 全体は1000 ステップで, 高周波５番目まで
# 
cycles = 2
steps = 1000
harmonics = 5
# ファイルが開けないときのエラー対応
try:
# ファイルを開く
    with open(filename,'w') as file:
        all_list = []
        for i in range(steps):
            list = []
            angle_in_degree = 360*cycles*i/steps
            angle = math.radians(angle_in_degree)
            # s = str(angle_in_degree)
            w = 0
            for j in range(1,harmonics+1):
                w += math.sin(angle*j)/j
                list.append(w)
                # s = s+", "+ str(w)
             #    print(s)
            # file.write(s+"\n")
            all_list.append(list)
            # print(all_list)
        
        csv = ""
        for list in all_list:
            for item in list:
                csv = csv + str(item) + ","
            csv += "\n"
            # csv = csv+"\n"
        file.write(csv)
        print("Writing to file "+ filename + " is finished")
except IOError:
    print("Unable to open file")




# import tkinter as tk
# import tkinter.filedialog
# import math
# #
# # tkinter の filedialog だけを利用する例
# #
# # root ウインドウはwithdraw() メソッドを読んで隠す
# root = tk.Tk()
# root.withdraw()
# #
# # 書き出し用の filedialog を読んでファイル名を得る
# #
# filename = tkinter.filedialog.asksaveasfilename()
# #
# # tkinter は終了する
# #
# root.destroy()
# #
# # ファイル名がもらえなければ終了
# #
# if filename:
#     pass
# else:
#     print("No file specified")
#     exit()
# #
# # 正弦波の重ね合わせで鋸波を近似する
# # 
# # w = sin(t) + sin(3t)/3 + sin(5t)/5 + sin(7t)/7 ...

# # 2周期分, 全体は1000 ステップで, 高周波５番目まで
# # 
# cycles = 2
# steps = 1000
# harmonics = 5
# # ファイルが開けないときのエラー対応
# try:
#     # ファイルを開く
#     with open(filename,'w') as file:
#         # 2π/1000ごとの角度の空リストを作る
#         angle_list = []
#         # 角度リストの各要素について演算した結果を入れる空リストを５個作る
#         result_list = []
#         for l in range(1, harmonics+1):
#             # result_list[l] = []
#             result_list.append([])

#         # 角度の1000の要素をリストに入れる
#         for i in range(steps):
#             angle_in_degree = 360*cycles*i/steps
#             angle = math.radians(angle_in_degree)
#             angle_list.append(angle)

#             # リストの各要素について演算をし、結果をリストに入れる
#             w = 0
#             # for k in range(len(angle_list)):
#             #     w += math.sin(angle_list[0])
#             #     w += math.sin(angle_list[1]*3/3)
#             #     w += math.sin(angle_list[2]*5/5)
#             #     w += math.sin(angle_list[3]*7/7)
#             #     w += math.sin(angle_list[4]*9/9)

#             for j in range(1,harmonics*2+1):
#                 if j%2 == 1:
#                     w += math.sin(angle*j)/j
#                     result_list[j].append(w)
#                 else:
#                     pass

#         # 角度リストと５個の演算リストを含む全体リストを作る
#         whole_list = [angle_list, result_list[l]]

#         # print(a)
#         file.write(a)
#         print("Writing to file "+ filename + " is finished")
# except IOError:
#     print("Unable to open file")
from turtle import *
import random
# 乱数を使うので randam モジュールもインポート

# 実行を停止するための変数 (フラッグ)
stop_flag = False

# マウスがクリックされた時の関数、引数 x. y をとるように
# しないといけないが、使わない
# 実行停止フラグを True にする

def clicked(x, y):
    global stop_flag
    stop_flag = True

# マウスがクリックされた時の動作を指定、clicked 関数を
# 呼び出す
#
onscreenclick(clicked)

speed(0)
while(not stop_flag):
    # -90 度から 90 度の範囲でランダムに向きを変える
    left(random. randint(-90, 90))
    forward(10)
    # タートルの位置が原点から一定の距離を越えれば、戻る
    if position()[0]**2+position()[1]**2 > 200**2:
            forward(-10)

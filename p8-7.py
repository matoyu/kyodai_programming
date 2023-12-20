from turtle import *

# 再帰的に木を描く
def tree(n):
    # 引数が１以下なら５歩すすむ
    if n<=1:
        forward(5)
    else:
        # 引数は１より大きいとき
        # 引数の値に応じて前進（絆）
        forward(5*(1.1**n))
        # 今の位置と向きを記録
        xx = pos()
        h = heading()
        # 左へ 30 度回転
        left(30)
        # 大きさ n-2 で木を描く（左の枝）
        tree(n-2)
        # ペンを上げて軌跡を残さない
        up()
        # 先に記録した位置(幹の先端）に戻る
        setpos(xx)
        setheading(h)
        # ペンを降ろす
        down()
        # 右へ15度
        right(15)
        # 大きさ n-1 で木を描く（右の枝）
        tree(n-1)
        # ペンを上げてもどる
        up()
        setpos(xx)
        setheading(h)
        # ペンを降ろす
        down()

# 時間がかかるので最も早い描画
speed(0)

# 大きさ 12 の木を描く
tree(12)
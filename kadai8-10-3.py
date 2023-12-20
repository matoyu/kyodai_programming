from turtle import *


def come(x, y):
    t = Turtle()

    # x, yにturtleをまず移動させる。
    t.penup()
    t.goto(x, y)
    t.pendown()

    # turtleの速度を最速(0)にする
    t.speed(0)
    t.color('red')
    t.fillcolor('red')
    t.begin_fill()
    for j in range(5):
        t.left(72)
        for i in range(180):
            t.forward(2)
            t.left(2)
    t.end_fill()


# これは, 画面がクリックされたらクリックされた位置を(x, y)として
# come(x, y)が呼ばれるというおまじない
onscreenclick(come)

done()

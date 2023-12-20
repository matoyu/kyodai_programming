from turtle import *
def come():
    t = Turtle()
    t.color('red')
    t.fillcolor('red')
    t.begin_fill()
    for j in range(5):   
        t.left(72)
        for i in range(180):
            t.forward(2)
            t.left(2)
    t.end_fill()
onscreenclick(come())

done()
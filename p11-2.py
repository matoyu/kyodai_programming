# クラスの練習
class MyClass():
    # 以下はクラス変数
    a = "マイクラス"
    __b = 0

    # 以下は生成する際に呼ばれる関数, mydata の初期値を
    # 引数で与える
    def __init__(self, data):
        # __number はインスタンスに与える通し番号
        self.__number = MyClass.__b
        self.mydata = data
        print("MyClass Object is created, number: ", self.__number)
        # クラス変数を１増やす
        MyClass.__b += 1

        # 通し番号を表示するメソッド
    def show_number(self):
        print(self.__number)
#
# ここからメインプログラム
#
if __name__ =="__main__":
    print("Myclass のクラス変数 a: ",MyClass.a)

    instance1 = MyClass(1)
    instance2 = MyClass(10)

    instance1.show_number()
    instance2.show_number()

    print("mydata of instance1: ", instance1.mydata)
    print("mydata of instance2: ", instance2.mydata)
    instance1.mydata += 1
    instance2.mydata += 2
    print("mydata of instance1: ", instance1.mydata)
    print("mydata of instance2: ", instance2.mydata)

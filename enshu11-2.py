class Dentaku():
    def __init__(self):
        self.first_term = 0
        self.second_term = 0
        self.result = 0
        self.operation = 0


    def do_operation(self):
        if self.operation == "+":
            self.result = self.first_term + self.second_term
        elif self.operation == "-":
            self.result = self.first_term - self.second_term
        elif self.operation == "*":
            self.result = self.first_term * self.second_term
        elif self.operation == "//":
            self.result = self.first_term // self.second_term

#ここからメインプログラム
dentaku = Dentaku()
kenzandentaku = Dentaku()
while True:
    f = int(input("First term "))
    dentaku.first_term = f
    o = input("Operation ")
    dentaku.operation = o
    s = int(input("Second term "))
    dentaku.second_term = s
    dentaku.do_operation()
    r = dentaku.result
    kenzandentaku.first_term = r
    kenzandentaku.second_term = s
    kenzandentaku.operation = "-"
    kenzandentaku.do_operation()
    kr = kenzandentaku.result
    
    print("Result ", r)
    print("KenzanResult",kr)

    if kr == f:
        print("OK")
    else: 
        print("False")

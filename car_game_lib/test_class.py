class TestClass:

    def __init__(self):
        self.fun = self.printToto

    def setFun(self,fun):
        self.fun = fun
    
    def execute(self,args):
        self.fun(*args)

    def printToto(self):
        print('Toto')

    def printTata(self):
        print('Tata')

    def printMsg(self,msg):
        print(msg)
    

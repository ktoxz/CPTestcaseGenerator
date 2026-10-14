class Solve:

    def __init__(self) -> None:
        self.dauVao = [];
        self.traLoi = [];

    def vao(self) -> None:
        self.dauVao = [int(item) for item in input()];
        self.traLoi = [int(item) for item in input()];

    def check(self) -> bool:
        for i in range(len(self.dauVao)):
            if(self.dauVao[i] != self.traLoi[i]): return False;
        return True;
    
    def lam(self) -> None:
        self.dauVao.sort()
        if(self.dauVao[0] == 0):
            for i in range(1,len(self.dauVao)):
                if(self.dauVao[i] != 0):
                    tmp = self.dauVao[0];
                    self.dauVao[0] = self.dauVao[1];
                    self.dauVao[1] = tmp;
                    break;
        if(self.check() == True): print("OK");
        else: print("WRONG_ANSWER");
                    
    
    def ra(self) -> None:
        pass;


def main():
    p = Solve();
    p.vao();
    p.lam();
    p.ra();

main();
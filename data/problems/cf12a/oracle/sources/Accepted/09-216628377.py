class Solve:
    
    def __init__(self) -> None:
        self.dauVao = [];

    def vao(self) -> None:
        self.dauVao = [input() for _ in range(3)];

    def lam(self) -> None:
        tmp = 0;
        for i in range(3):
            if(self.dauVao[0][i] != self.dauVao[2][2 - i]): tmp += 1;
        if(self.dauVao[1][0] != self.dauVao[1][2]): tmp += 1;
        if(tmp > 0): print("NO");
        else: print("YES");

    def ra(self) -> None:
        pass;

def main():
    p = Solve();
    p.vao();
    p.lam();
    p.ra();

main();
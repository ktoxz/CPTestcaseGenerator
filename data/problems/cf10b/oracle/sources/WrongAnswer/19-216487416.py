class Solve:

    def __init__(self):
        self.N = 0;
        self.K = 0;
        self.dauVao = [];
        self.trungTam = 0;
        self.bangKetQua = [[]];
    
    def vao(self):
        (self.N, self.K) = map(int, input().split());
        self.dauVao = [int(item) for item in input().split()];
        self.trungTam = (self.K + 1) // 2;
        self.bangKetQua = [[0,0]];
        self.bangKetQua += [[self.K, 0] for _ in range(self.K)];
    
    def lam(self):
        for item in self.dauVao:
            x, y, diem = 0, 0, float("inf");
            for i in range(1,self.K + 1):
                # Nếu phần trung tâm vẫn chưa được đặt ghế
                if(self.bangKetQua[i][0] == self.K):
                    #Công thức tính số điểm đạt được
                    #Chứng minh từ công thức cấp số cộng 
                    #Số ở giữa của hàng sẽ có giá trị nhỏ nhất
                    tmp = abs(i - self.trungTam) * item + (item // 2) * ((item + 1) // 2); 
                    #Tìm số điểm nhỏ nhất có thể đạt được
                    if(diem > tmp):
                        diem = tmp;
                        y = i;
                        x = self.trungTam - item // 2;
                else:
                    #Nếu phần ghế được phân nằm ở nửa bên trái điểm trung tâm
                    if(item <= self.bangKetQua[i][0]):
                        tmp = abs(i - self.trungTam) * item + (self.trungTam - 2 * self.bangKetQua[i][0] + item) * item // 2;
                        if(diem > tmp):
                            diem = tmp;
                            y = i;
                            x = self.bangKetQua[i][0] - item + 1;
                    #Nếu phần ghế được phân nằm phía bên phải
                    elif(item <= self.bangKetQua[i][1]):
                        tmp = abs(i - self.trungTam) * item + (self.trungTam - 2 * self.bangKetQua[i][1] + item) * item // 2;
                        if(diem > tmp):
                            diem = tmp;
                            y = i;
                            x = self.K - self.bangKetQua[i][1] + item;
            if(diem < float("inf")):
                print(y, x , x + item - 1);
                if(self.bangKetQua[y][0] == self.K):
                    self.bangKetQua[y] = [(self.K - item) // 2, (self.K - item + 1) // 2];
                elif(item <= self.bangKetQua[y][0]): self.bangKetQua[y][0] -= item;
                else: self.bangKetQua[y][1] -= item;
            else:
                print("-1");


def main():
    p = Solve();
    p.vao();
    p.lam();

main();
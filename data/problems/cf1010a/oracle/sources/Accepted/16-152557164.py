# @Chukamin ZZU_TRAIN

def main():
    n = int(input())
    m = int(input())
    s = m
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    def cal(n, m, s, a, b):
        if b[0] <= 1.00:
            return -1
        k = s / (b[0] - 1)
        s += k
        for i in range(n - 1, 0, -1):
            if a[i] <= 1.00:
                return -1
            k = s / (a[i] - 1)
            s += k
            if b[i] <= 1.00:
                return -1
            k = s / (b[i] - 1)
            s += k       
        if a[0] <= 1.00:
            return -1
        k = s / (a[0] - 1)
        s += k
        return s - m
    ans = cal(n, m, s, a, b)
    if ans != -1:
        print('{:.8f}'.format(ans))
    else:
        print(-1)
            
if __name__ == '__main__':
    main()
from math import log

def solve(k,n):
    if n < k :
        print('NO')
    if not n % k:
        print('YES')
        print(int(log(n,k))-1)
        return
    print('NO')

    

def main():
    # vars = list(map(int, input().split(" ")))
    k= int(input())
    n = int(input())

    # s = input()
    # a = list(map(int, input().split(" ")))
    # b = list(map(int, input().split(" ")))
    # c = list(map(int, input().split(" ")))
    # res = []
    # for _ in range(n):
    #     arr = list(map(int, input().split(" ")))
    #     res.append(saveThePrisoner(*arr))
    # print(*res,sep='\n')
    solve(k,n)


main()
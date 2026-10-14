import sys
import threading
input = sys.stdin.readline
def main():
    n = list(input())
    memo = {}
    def dp(idx, number ):

        if idx == len(n):
            return 0

        if idx in memo:
            return memo[idx]

        ans = 0
        num = 0 
        for i in range(idx, len(n)):
            cur = int(n[i])
            num = num * 10 + cur
            ans  = max(dp(i+1 , num) , ans)
        
        
        memo[idx] =  ans + int(number % 3 == 0) 
        return memo[idx]

    print(dp(0,0))

if __name__ == '__main__':
    sys.setrecursionlimit(1 << 30)
    threading.stack_size(1 << 27)

    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()
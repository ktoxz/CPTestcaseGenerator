import sys
import math
import bisect

def solve(A):
    n = len(A)
    #print('A: %s' % str(A))
    B = [0] * n
    for i in range(n):
        if i == 0:
            B[i] = A[i]
        else:
            if A[i] == 1:
                B[i] = B[i-1] + 1
            else:
                B[i] = B[i-1] + 1 + (i + 1) * (A[i] - 1)
    #print('B: %s' % str(B))
    return B[-1]

def main():
    n = int(input())
    A = list(map(int, input().split()))
    ans = solve(A)
    print(ans)

if __name__ == "__main__":
    main()
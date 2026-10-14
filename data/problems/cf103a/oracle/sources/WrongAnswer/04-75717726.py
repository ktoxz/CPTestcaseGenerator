import sys
import math
import bisect

class PrefixSum:
    n = None
    A = None
    def __init__(self, A):
        self.n = len(A)
        self.A = A.copy()
        for i in range(1, self.n):
            self.A[i] += self.A[i-1]
    def query_prefix_sum_value(self, x):
        return self.A[x]
    def query_sum_value(self, x, y):
        ans = self.query_prefix_sum_value(y)
        if x:
            ans -= self.query_prefix_sum_value(x - 1)
        return ans
    def unwind(self):
        A = [0] * self.n
        for i in range(self.n):
            A[i] = self.query_sum_value(i, i)
        return A

def solve(A):
    n = len(A)
    prefix = PrefixSum(A)
    '''
    print('A: %s' % str(A))
    print('prefix: %s' % (str(prefix.unwind())))
    '''
    B = [0] * n
    for i in range(n):
        if i == 0:
            B[i] = A[i]
        else:
            if A[i] == 1:
                B[i] = B[i-1] + 1
            else:
                B[i] = B[i-1] + 1 + prefix.query_sum_value(0, i - 1) * (A[i] - 1)
    return B[-1]

def main():
    n = int(input())
    A = list(map(int, input().split()))
    ans = solve(A)
    print(ans)

if __name__ == "__main__":
    main()
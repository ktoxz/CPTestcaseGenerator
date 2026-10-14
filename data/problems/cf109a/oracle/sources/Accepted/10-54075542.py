# https://codeforces.com/problemset/problem/109/A

import sys
import math


def main():
    # sys.stdin = open('E:\\Sublime\\in.txt', 'r')
    # sys.stdout = open('E:\\Sublime\\out.txt', 'w')
    # sys.stderr = open('E:\\Sublime\\err.txt', 'w')

    n = int(sys.stdin.readline().strip())
    a, b = n//7, n % 7
    c, d = b//4, b % 4

    print(-1if a < d else'4'*(c+2*d)+'7'*(a-d))


if __name__ == '__main__':
    main()

# hajj
#  　　　　　　 ＿＿
# 　　　　　／＞　　フ
# 　　　　　| 　_　 _ l
# 　 　　　／` ミ＿xノ
# 　　 　 /　　　 　 |
# 　　　 /　 ヽ　　 ﾉ
# 　 　 │　　|　|　|
# 　／￣|　　 |　|　|
# 　| (￣ヽ＿_ヽ_)__)
# 　＼二つ
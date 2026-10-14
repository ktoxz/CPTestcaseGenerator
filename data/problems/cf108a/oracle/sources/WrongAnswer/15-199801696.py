def st():return str(input())
def ls():return list(map(int, input().split()))
def mx(a):return max(a)
def it():return int(input())
def mn(a):return min(a)
def yes():return print('YES')
def no():return print('NO')
def re(a):return range(a)
def pr(a):return print(a)
def prs(a):return print(str(a))
def mapa():return map(int, input().split())

s = [int(i) for i in input().split(':')]
m = []
v=[]

if s[0] == 0 and s[1] > 0:
    pr('01:10')
elif s[0] == 1 and s[1] >= 10:
    pr('02:20')
elif s[0] == 2 and s[1] >= 20:
    pr('03:30')
elif s[0] == 3 and s[1] >= 30:
    pr('04:40')
elif s[0] == 4 and s[1]  >= 40:
    pr('05:50')
elif (s[0] > 5 and s[0] < 10):
    pr('10:01')
elif s[0] == 10 and s[1] >= 1:
    pr('06:60')
elif s[0] == 11 and s[1] >= 11:
    pr('12:21')
elif s[0] == 12 and s[1] >= 21:
    print('13:31')
elif s[0] == 13 and s[1] >= 31:
    print('14:41')
elif s[0] == 14 and s[1] >= 41:
    print('15:51')
elif s[0] >= 15 and s[0] <= 21:
    print('21:12')
elif s[0] == 21 and s[1] >= 12:
    print('22:22')
elif s[0] == 22 and s[1] >= 22:
    pr('23:23')
elif s[0] == 23 and s[1] >= 32:
    pr('00:00')
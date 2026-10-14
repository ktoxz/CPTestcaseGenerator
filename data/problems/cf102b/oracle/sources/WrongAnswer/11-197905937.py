n = input()
s = [int(i) for i in list(n)]
summ = sum(s)
cnt = 1
if n == '1':
    print(1)
else:
    while summ > 9:
        a = summ
        cnt += 1
        b = [int(i) for i in list(str(a))]
        summ = sum(b)
    print(cnt)
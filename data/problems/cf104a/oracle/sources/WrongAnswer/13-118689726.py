n = int(input())
s = n-10
if s>0:
    if 1<=s<=9 or s==11:
        print(4)
    elif s==10:
        print(15)
else:
    print(0)
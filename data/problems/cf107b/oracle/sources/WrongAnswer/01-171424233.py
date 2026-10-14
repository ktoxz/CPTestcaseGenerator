a=list(map(int, input().split()))
b =list(map(int, input().split()))
if a[0]==b[0]+b[1]:
    print("1")
if a[0]>b[0]+b[1]:
    print('-1')
if a[0]<b[0]+b[1]:
    print(b[0]/a[0])
q = int(input())
l = int(input())
if(l%q==0):
    print("YES")
    ans = q
    count =0
    for i in range(1,32):
        if(l==ans):
            break
        else:
            ans = ans**i
            count = i
    print(count-1)
else:
    print("NO")
tramp=input()
a,b=map(str, input().split())
pack=["6", "7", "8", "9", "T", "J", "Q", "K","A"]
if a[1]==tramp and b[1]!=tramp:
    print("YES")
elif (a[1]==tramp and b[1]==tramp) or (a[1]!=tramp and b[1]!=tramp):
    if pack.index(a[0]) > pack.index(b[0]):
        print("YES")
    else:
        print("NO")
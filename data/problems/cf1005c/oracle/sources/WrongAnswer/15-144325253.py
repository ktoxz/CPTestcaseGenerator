from collections import  Counter
def f(a):
    pw=[2**i for i in range(2,31)]
    bad=0
    cnt=Counter(a)
    for i in a:
        fl=False
        for p in pw:
            res=p-i
            if cnt.get(res,None)!=None:
                if res==i:
                    if cnt[i]==2:
                        fl=True
                        break
                else:
                    fl=True
                    break
        if not fl:
            bad+=1
    return bad


n=input()
a=[*map(int,input().strip().split())]
print(f(a))
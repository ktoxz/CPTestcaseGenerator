n=(input())
ans=(input())
n1=str(n)
n1=list(n1)
if len(str(n))!=len(str(ans)):
    print('WRONG_ANSWER')
elif n==0:
    print('OK' if n==ans else 'WRONG_ANSWER')
elif '0' not in n1:
    ans1=''.join(sorted(n1))
    if (ans1)==ans:
        print('OK')
    else:
        print('WRONG_ANSWER')
else:
    ans1=sorted(n1)
    c=ans1.count('0')
    ans1=[i for i in ans1 if i!='0']
    for i in range(c):
        ans1.insert(1,'0')
    ans1=''.join(ans1)
    if (ans1)==ans:
        print('OK')
    else:
        print('WRONG_ANSWER')
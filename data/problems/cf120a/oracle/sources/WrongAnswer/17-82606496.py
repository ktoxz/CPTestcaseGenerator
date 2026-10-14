import sys
sys.stdin = open('input.txt','r')
sys.stdout=open('output.txt','w')
s= str(input())
n= int(input())
if s=='front' and n==1:
    ans='L'
elif s=='front' and n==2:
    ans='R'
elif s=='black' and n==1:
    ans='R'
else:
    ans='L'
print(ans)
def rank(c):
    s="6789TJQKA"
    return s.find(c)
t=input()
s=input()
s1, s2=s.split(sep=" ")
if s1[1]==t and s2[1]!=t:
    print('YES')
elif s1[1]==s2[1] and rank(s1[0])>=rank(s2[0]):
    print('YES')
else:
    print('NO')
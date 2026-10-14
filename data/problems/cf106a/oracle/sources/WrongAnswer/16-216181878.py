t = str(input())
s1, s2 = map(str,input().split())
t = "6789TJQKA"
if s1[1] == s2[1]:
	print("YES" if t.find(s1[0]) > t.find(s2[0]) else "NO")
else:
	print("YES" if s1[1] == t else "NO")
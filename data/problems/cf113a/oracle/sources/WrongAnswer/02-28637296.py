s = input()
d = 2
i = 1
for each in s.split():
    if each.endswith("lios") or each.endswith("liala") or each.endswith("etr") or each.endswith("etra") or each.endswith("initis") or each.endswith("inites"):
        d = 1
    else:
        d = 0
while i < (len(s)-1):
    if(s[i] == " " and s[i+1] == " "):
        d = 0
    i += 1
if d == 1:
    print("YES")
elif d == 0:
    print("NO")
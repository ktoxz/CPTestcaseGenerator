n = input().split(':')
h = int(n[0])
m = int(n[1])
def check(h,m):
    h = str(h)
    m = str(m)
    if h == m [::-1]:
        return True
    return False
        
for i in range(100):  
    m += 1
    if m ==60:
        m = 0
        h += 1
    if h == 24:
        h = 0
    if check(h,m):
        break
res =""
h = str(h)
m = str(m)
if len(h) ==1:
    res = res +'0' + str(h) + ':'
else:
    res = res +  str(h) + ":"
if len(m) ==1:
    res = res + '0' +str(m)
else:
    res = res + str(m)
print(res)
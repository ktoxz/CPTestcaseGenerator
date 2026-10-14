n = int(input())
m = int(input())
toff = list(map(int, input().split()))
land = list(map(int, input().split()))
con = toff + land
coff = 1
for i in range(len(con)):
    coff *= (1-(1/con[i]))
try:
    print(m*((1/coff)-1))
except:
    print(-1)
a, b = map(int,input().split())
pri = list(map(int,input().split()))
pri.sort()
li = []
new = []
new.sort()
high = 0
low = 0
for x in range(b):
	k = input()
	if k not in li:
		li.append(k)
		new.append(1)
	else:new[li.index(k)] += 1
for x in range(len(new)):
	high += new[-(x + 1)] * pri[-(x + 1)]
	low += new[-(x + 1)] * pri[x]
print(low,high)
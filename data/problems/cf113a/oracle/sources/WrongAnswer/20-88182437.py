li = list(input().split())

for i in li :
	x = i[::-1]
	flag = 0
	if len(x)>=3 :
		if x[0:3] == "rte":
			flag = 1
	if len(x)>=4 :
		if x[0:4] == "arte" or x[0:4] == "soil":
			flag = 1
	if len(x)>=5 :
		if x[0:5] == "alail" :
			flag = 1
	if len(x)>=6 :
		if x[0:6] == "sitini" or x[0:6] == "setini":
			flag = 1
	if flag==0:
		print("NO")
		exit(0)
	
print("YES")
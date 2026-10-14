n = input()
value1 = int(n[1])
value2 = int(n[3])
ans = n
if value1 < 5:
	forward = 0
	
	if value1 >= value2:
		if int(n[1]) == int(n[3]):
			if int(n[4]) >= int(n[0]):
				forward = 1
			else:
				forward = 0
				ans = ans[:4] + ans[0]
		else:
			ans = ans[:3] + ans[1] + ans[0]
	else:
		forward = 1
	if value1 == 3 and int(n[0]) == 2:
		if int(n[3]) >= 3 and int(n[4])>=2:
			ans = "00:00"
			forward = 0
	if forward == 1:
		add = int(ans[1]) + 1
		ans = ans[:1] + str(add) + ans[2:3] + str(add) + ans[:1]
else:
	add = int(ans[0])+1
	ans = str(add) + "0:0" + str(add)
print(ans)
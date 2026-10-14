r1 = input()
r2 = input()
r3 = input()
matrix = [r1,r2,r3]
if matrix[0][0] == matrix[2][2]:
	flag = 0
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == matrix[2-i][2-j]:
				pass
			else:
				flag = 1
				break	
		if flag == 1:
			break
	if flag == 0 and matrix[0][0] == matrix[1][1] and matrix[0][0] == a[2][2]:
		print("YES")
		exit()			
if matrix[0][0] == matrix[2][0]:
	flag = 0
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == matrix[2-i][j]:
				pass
			else:
				flag = 1
				break
		if flag == 1:
			break
	if flag == 0 and matrix[1][1] == matrix[1][0] and matrix[1][1] == matrix[2][0]:
		print("YES")
		exit()
if matrix[0][0] == matrix[0][2]:
	flag = 0
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == matrix[i][2-j]:
				pass
			else:
				flag = 1
				break
		if flag == 1:
			break
	if flag == 0 and matrix[0][1] == matrix[1][1] and matrix[1][1] == matrix[2][1]:
		print("YES")
		exit()
if matrix[0][2] == matrix[2][0]:
	flag = 0
	for i in range(3):
		for j in range(3):
			if matrix[i][j] == matrix[j][i]:
				pass
			else:
				flag = 1
				break
		if flag == 1:
			break
	if flag == 0 and matrix[0][0] == matrix[1][1] and matrix[1][1] == matrix[2][2]:
		print("YES")
		exit()
print("NO")
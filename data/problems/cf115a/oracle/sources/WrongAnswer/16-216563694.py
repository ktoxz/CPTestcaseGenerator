n = int(input())
employees = []
mx, cnt = 0, 0
for i in range(n):
    s = int(input())
    if s not in employees or s==-1:
        employees.append(s)
for j in range(len(employees)):
    if employees[j]==-1:
        cnt = 0 
    cnt += 1
    if mx < cnt:
        mx = cnt 

print(mx)
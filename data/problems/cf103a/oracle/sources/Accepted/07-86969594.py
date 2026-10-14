n = int(input())
a = [int(each) for each in input().split()]
# print(n)
# print(a)
res = 0
for i in range(n):
    #前边正确的一次不用考虑，直接加一就行，剩下的所有答案过一遍前边的东西
    if a[i] == 1:
        res += 1
    else:
        # res += (i + 1) * a[i]
        res += (i + 1) * (a[i] - 1) + 1

print(res)
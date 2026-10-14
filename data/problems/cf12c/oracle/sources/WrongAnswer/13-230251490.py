n,k = map(int,input().split())
arr = list(map(int,input().split()))
arr.sort()
arr2 = []
for _ in range(k):
    fruit = input()
    arr2.append(fruit)
arr3 = set(arr2)
min_ =0
i = 0
while i <len(arr3):
    min_ += arr[i]
    i +=1
j = len(arr)-1
maxx_ = 0
while j > (len(arr)-1-len(arr3)):
    maxx_ += arr[j]
    j -=1
if len(arr3)<k:
    print(min_ + arr[0],maxx_ + arr[-1])
else:
    print(min_ , maxx_)
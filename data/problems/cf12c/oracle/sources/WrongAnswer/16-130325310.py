#loser707
n,m=map(int,input().split())
price=list(map(int,input().split()))
price_sorted_from_min=sorted(price)
price_sorted_from_max=price_sorted_from_min[::-1]
print(price_sorted_from_min,price_sorted_from_max)
fruits=[]
for i in range(m):
    f=input()
    fruits.append(f)
fruits_count=[]
for i in fruits:
    fruits_count.append((fruits.count(i),i))
fruits_count.sort(reverse=True)
fr=[]
for (x,y) in fruits_count:
    fr.append(y)
fruits_set=[]
for i in range(len(fr)):
    if fr[i] not in fr[i+1:]:
        fruits_set.append(fr[i])
print(fruits_set)
ans_min=0
ans_max=0
for x,y in zip(fruits_set, price_sorted_from_min):
    ans_min=ans_min+y*fruits.count(x)
for x,y in zip(fruits_set, price_sorted_from_max):
    ans_max=ans_max+y*fruits.count(x)
print(ans_min,ans_max)
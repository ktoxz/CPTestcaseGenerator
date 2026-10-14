n=int(input())
c=n-10
d=0
hearts=[1,11,2,3,4,5,6,7,8,9,10,10,10,10]
diamonds=[1,11,2,3,4,5,6,7,8,9,10,10,10,10]
clubs=[1,11,2,3,4,5,6,7,8,9,10,10,10,10]
spades=[1,11,2,3,4,5,6,7,8,9,10,10,10]
for i in range(len(hearts)):
    if hearts[i]==c:
        d+=1
for i in range(len(diamonds)):
    if diamonds[i]==c:
        d+=1
for i in range(len(clubs)):
    if clubs[i]==c:
        d+=1
for i in range(len(spades)):
    if spades[i]==c:
        d+=1
print(d)
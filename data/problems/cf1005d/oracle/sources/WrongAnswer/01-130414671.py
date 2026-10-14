st = input()

count = 0
summ = 0

fin=0
for i in st:
    summ+=int(i)
    count+=1
    if summ%3==0 or int(i)%3==0:
        fin +=1
        summ=0
        count=0
print(fin)
# Thu Sep 30 2021 23:46:05 GMT+0300 (Москва, стандартное время)
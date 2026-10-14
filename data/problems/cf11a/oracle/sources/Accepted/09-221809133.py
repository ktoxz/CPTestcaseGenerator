n=list(map(int,input().split()))
d=list(map(int,input().split()))
prevval,nextval='',''
currentmove,totalmove=0,0
for index,value in enumerate(d):
    if index != len(d) - 1:
        nextval = d[index + 1]
    if index != 0:
        prevval=d[index-1]
        if value<=prevval:#or (value<=nextval and index != len(d) - 1):
            currentmove = abs(int((prevval - value) / n[1])) + 1
            totalmove=totalmove+currentmove
            d[index]=(value if value < prevval else prevval) +(currentmove*n[1])
            #print(currentmove, totalmove,d[index])
print(totalmove)
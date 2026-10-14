nos = input()
po = 0 
while True:
    if len(nos) == 1:
        print(po)
        break
    else:
        nos = str(sum(list(map(int,list(nos)))))
        po+=1
entrada = int(input())

num4 = entrada // 4
num7 = entrada // 7

soma = 0
list = []
qntDigits4 = 0
i = 0

bol = False
while i < num4 + 1:
    soma = i*4
    if(i != 0):
        qntDigits4 +=1
    
    qntDigits7 = 0
    if(soma == entrada):
        print(qntDigits4)
        print(qntDigits7)
        list.append(qntDigits4)
        list.append(qntDigits7)
        bol = True
        break
    for j in range(num7 + 1):
        soma += j * 7
        if(j != 0):
            qntDigits7 += 1
        if(soma == entrada):
            list.append(qntDigits4)
            list.append(qntDigits7)
            print(f'{qntDigits4} a')
            print(qntDigits7)
            bol = True
            break
    i+=1
    if(bol):
        break

if(len(list) == 0):
    print(-1)
else:
    print(list[0]* '4', end='')
    print(list[1]* '7')
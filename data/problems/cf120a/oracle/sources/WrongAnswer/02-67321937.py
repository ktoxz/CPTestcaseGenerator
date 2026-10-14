with open('input.txt', 'r') as i:
    with open('output.txt', 'w') as o:
        t1 = i.readline()
        t2 = i.readline()
        print(t1, t2, sep='', end='')
        if (t1 == 'front\n' and t2 == '1') or (t1 == 'back' and t2 == '2'):
            o.write('L')
        else:
            o.write('R')


# Sat Dec 21 2019 11:20:12 GMT+0300 (MSK)
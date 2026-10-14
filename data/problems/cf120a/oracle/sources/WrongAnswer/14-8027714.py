f = open('input.txt')
g = open('output.txt','w')
x = f.readline()
y = f.readline()
if x == 'front':
    if y == '1':
        g.write('L')
    else:
        g.write ('R')
else:
    if y == '1':
        g.write ('R')
    else:
        g.write ('L')
g.close()    
f.close()
f = open('input.txt', 'r')
s = []
for line in f:
    s.append(line)
g = open('output.txt', 'w')
if s[0] == 'front' and s[1] == '1' or s[0] == 'back' and s[1] == '2':
    g.write('L')
else:
    g.write('R')
f.close()
g.close()
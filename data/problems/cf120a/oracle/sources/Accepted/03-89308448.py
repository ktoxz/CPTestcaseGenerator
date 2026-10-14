fin=open('input.txt')
fout=open('output.txt','w')
s=fin.read()
s=s.split()
a=s[0]
n=int(s[1])
if (a=='front' and n==1) or (a=='back' and n==2):
    fout.write('L')
else:
    fout.write('R')
fin.close()
fout.close()
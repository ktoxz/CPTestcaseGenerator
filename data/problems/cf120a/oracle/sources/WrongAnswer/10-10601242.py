f = open("input.txt")             # 返回一个文件对象  
a=f.readline()
a=a[0]
b=f.readline()
b=b[0]
f.close()

if a=='f' and b=='1':
    s='L'
elif a=='f' and b=='2':
    s='R'
elif a=='b' and b=='1':
    s='L'
elif a=='b' and b=='2':
    s='R'

f = open('output.txt', 'w')
f.writelines(s)
f.close()
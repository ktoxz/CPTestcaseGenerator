s = input()
n = int(input())
x = len(s)

if x<=n:
    print(0,"\n")
else:
    dic = {}
    for i in s:
        dic[i] = dic.get(i,0) + 1
    dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}
    c = 0
    m = []
    for i,j in dic.items():
        c+=j
        
        if c>n:
            m.append(i)
            
        else:
            s = s.replace(i,"")
    
    print(len(m))
    print(s)
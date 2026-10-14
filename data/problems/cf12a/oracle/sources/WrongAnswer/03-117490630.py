k=[]
n=3
for i in range(3):
     k.append(input())
m=True
for i in range(2):
     for j in range(3):
          if i!=1:
               if (k[i][j]=="X" and k[n-i-1][n-j-1]=="X") or (k[i][j]=="." and k[n-i-1][n-j-1]=="."):
                    continue
               else:
                    print("NO")
                    m=False
                    break
          else:
               if (k[i][j]=="X" and k[i][n-j-1]=="X") or (k[i][j]=="." and k[i][n-j-1]=="."):
                    continue
               else:
                    print("NO")
                    m=False
                    break
if m:
     print("YES")
[n,k]=[int(x) for x in input().split()];
xc=(k//2)+1;
req=[int(x) for x in input().split()];

ava=[[xc,xc] for x in range(k+1)];
for m in req:
    mindis=10**10;
    x=None;
    yl=None;
    yr=None;
    for i in range(1,k+1):
        dis=m*abs((i-xc))
        if ava[i][0]==ava[i][1]:
            if m%2:
                dis+=(m//2)*((m//2)+1);
                colst=xc-(m//2);
                colend=xc+(m//2);
            else:
                dis+=(m//2)*(m//2);
                colst=xc-(m//2);
                colend=xc+(m//2)-1;
        else:
            if m>ava[i][0] and m>k-ava[i][1]+1:
                continue;
            elif m>ava[i][0] and m<=k-ava[i][1]+1:
                dis+=((ava[i][1]-xc)*m)+((m-1)*m//2);
                colst=ava[i][1];
                colend=ava[i][1]+m-1;
            else:
                if xc-ava[i][0]<=ava[i][1]-xc:
                    dis+=((xc-ava[i][0])*m)+((m-1)*m//2);
                    colst=ava[i][0]-m+1;
                    colend=ava[i][0];
                else:
                    dis+=((ava[i][1]-xc)*m)+((m-1)*m//2);
                    colst=ava[i][1];
                    colend=ava[i][1]+m-1;
                    
        if dis<mindis:
            mindis=dis;
            x=i;
            yl=colst;
            yr=colend;
    if x==None:
        print(-1);
    else:
        print(x,yl,yr);
        ava[x][0]=min(ava[x][0],yl-1);
        ava[x][1]=max(ava[x][1],yr+1);
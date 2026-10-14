#include<cstdio>
int x[110][5],n,ans=0x7FFFFFFF,t;
int main(){
    scanf("%d",&n);
    for(int i=1;i<=n;++i)
        scanf("%d%d%d%d",&x[i][0],&x[i][1],&x[i][2],&x[i][3]);
    for(int i=1;i<=n;++i)
        for(int j=1;j<=n;++j)
            if(x[j][0]>x[i][0]&&x[j][1]>x[i][1]&&x[j][2]>x[i][2])
                x[i][4]=1;
    for(int i=1;i<=n;++i)
        if(x[i][4]==0)
            if(x[i][3]<ans){
                ans=x[i][3];
                t=i;
            }
    printf("%d\n",t);
    return 0;
}
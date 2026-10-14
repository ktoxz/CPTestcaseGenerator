#include <stdio.h>
int main(){
    int n,m,h,i,v,sum=0,ex;
    scanf("%d%d%d",&n,&m,&h);
    for(i=1;i<=m;++i){
        scanf("%d",&v);
        sum+=v;
        if(i==h) ex=v;
    }
    if(sum<n){
        printf("-1.0\n");
        return 0;
    }
    --n;
    int nu=sum-1,uu=nu-n;
    int nl=sum-ex+1;
    double res=1;
    for(i=nu;i>=nl;--i,--uu){
        res*=(double)uu/(double)i;
    }
    printf("%.15lf\n",1.0-res);
    return 0;
}
#include <stdio.h>

int n,m;
long long ans;

int main()
{
    int i,x,d;

    scanf("%d%d",&n,&m);
    for(i=1;i<=m;i++)
    {
        scanf("%d%d",&x,&d);
        ans += x * n;
        if(d > 0) ans += 1LL * (n-1) * n / 2 * d;
        else if(n & 1) ans += 1LL * (n/2) * (n/2+1) * d;
        else ans += (1LL * (n/2) * (n/2+1) / 2 + 1LL * (n/2-1) * (n/2) / 2) * d;
    }

    printf("%.9f",1.0*ans/n);
    return 0;
}
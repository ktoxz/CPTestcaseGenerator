#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;

#define LL long long
int n,m,h,sh;
LL sum;

int main()
{
    int i,num;
    while (scanf("%d %d %d",&n,&m,&h)!=EOF)
    {
        sum=0;
        for (i=1;i<=m;i++)
        {
            scanf("%d",&num);
            sum=sum+(LL)num;
            if (i==h) sh=num;
        }

        if (sum < n)
        {
            printf("-1.0\n");
            continue;
        }

        if (sum-sh<n-1)
        {
            printf("1.0\n");
            continue;
        }

        if (sh==1)
        {
            printf("0.0\n");
            continue;
        }
        double ans=1;
        for (i=1;i<=n-1;i++)
        {
            ans*=(double)(sum-sh-(i-1))/(sum-i);
        }
        printf("%.16f\n",1-ans);
    }
    return 0;
}
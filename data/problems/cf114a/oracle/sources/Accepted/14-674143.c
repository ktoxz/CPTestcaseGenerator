#include <stdio.h>

int main()
{
    int k,l,i;
    long long t;

    scanf("%d %d",&k,&l);


    for(i=0,t=k;t<l;i++,t*=k);

    if (t==l)
        printf("YES\n%d\n",i);
    else
        printf("NO");

    return 0;
}
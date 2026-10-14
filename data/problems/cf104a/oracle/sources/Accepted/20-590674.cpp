#include <stdio.h>
int main()
{
    int a,b;
    while(~scanf("%d",&a))
    {
        a-=10;
        if(a<1 || a>11)
        {
            printf("0\n");
            continue;
        }
        if(a==10)
        {
            printf("15\n");
            continue;
        }
        else
        {
            printf("4\n");
        }
    }
}
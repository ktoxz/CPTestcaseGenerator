#include <stdio.h>
int main()
{
    int n, m, n1;
    scanf("%d:%d", &n, &m);
    n1=10*(n%10);
    n1+=(n/10);
    if(n==0)
        printf("01:10");
    else
    {
        for(int i=0; i<1; i++)
        {
            if(n==1)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                    printf("02:20");
                break;
            }
            if(n==2)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                    printf("03:30");
                break;
            }
            if(n==3)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                    printf("04:40");
                break;
            }
            if(n==4)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("05:50");
                break;
            }
            
            if(n==5)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("10:01");
                break;
            }
            if(n==6)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("10:01");
                break;
            }
            if(n==7)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("10:01");
                break;
            }
            if(n==8)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("10:01");
                break;
            }
            if(n==9)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("10:01");
                break;
            }
            if(n==10)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("11:11");
                break;
            }
            if(n==11)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("12:21");
                break;
            }
            if(n==12)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("13:31");
                break;
            }
            if(n==13)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("14:41");
                break;
            }
            if(n==14)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("15:51");
                break;
            }
            if(n==15)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("20:02");
                break;
            }
            if(n==16)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("20:02");
                break;
            }
            if(n==17)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("20:02");
                break;
            }
            if(n==18)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("20:02");
                break;
            }
            if(n==19)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("20:02");
                break;
            }
            if(n==20)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("%.2d:%.2d", n+1, n1+10);
                break;
            }
            if(n==21)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("%.2d:%.2d", n+1, n1+10);
                break;
            }
            if(n==22)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("%.2d:%.2d", n+1, n1+10);
                break;
            }
            if(n==23)
            {
                if(n1>m&&n1<60)
                    printf("%.2d:%.2d", n, n1);
                else
                printf("00:00");
                break;
            }
        }
    }
    return 0;
}
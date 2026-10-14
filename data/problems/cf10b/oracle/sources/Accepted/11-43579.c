#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MAXN 105
#define INFINITY 2000000000

int main ()
{
    static char a[MAXN][MAXN];
    static int s[MAXN][MAXN];
    memset(a,0,sizeof(a));
    memset(s,0,sizeof(s));
    int T, N;
    scanf("%d %d",&T,&N);
    int C = (N+1)/2;
    int i, j;
    for (i = 1; i <= N; i++)
    {
        for (j = 1; j <= N; j++)
        {
            int temp = abs(i-C) + abs(j-C);
            s[i][j] = temp + s[i-1][j] + s[i][j-1] - s[i-1][j-1];
        }
    }
    int iT;
    for (iT = 0; iT < T; iT++)
    {
        int M;
        scanf("%d",&M);
        int res = INFINITY;
        int x = 0;
        int yl = 0;
        for (i = 1; i <= N; i++)
        {
            int last = 0;
            for (j = 1; j <= N; j++)
            {
                if (a[i][j]) last = j;
                else
                {
                    if ((j - last) >= M)
                    {
                        int first = last;
                        if ((j - M) > first) first = j - M;
                        int temp = s[i][j] - s[i-1][j] - s[i][first] + s[i-1][first];
                        if (temp < res)
                        {
                            res = temp;
                            x = i;
                            yl = first+1;
                        }
                    }
                }
            }
        }
        if (res == INFINITY) printf("-1\n");
        else
        {
            printf("%d %d %d\n",x,yl,yl+M-1);
            for (j = yl; j < (yl+M); j++) a[x][j] = 1;
        }
    }
    return 0;
}
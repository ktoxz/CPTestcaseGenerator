#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


int main(void)
{
    int min, n, m, i, x, y, z, k = 0, j;
    int  ans[500][3], a[1000], b[1000], d[1000];
    scanf("%d%d", &n, &m);
    for(i = 0; i < n; i++){
        a[i] = -1;
        b[i] = -1;
    }
    for(i = 0; i < m; i++){
        scanf("%d%d%d", &x, &y, &z);
        x--;
        y--;
        a[y] = x;
        b[x] = y;
        d[x] = z;
    }
    for(i = 0; i < n; i++){
        if (a[i] == -1){
            j = b[i];
            min = d[i];
            while (j != -1 && b[j] != -1){
                if (d[j] < min){
                    min = d[j];
                }
                j = b[j];
            }
            if (j != -1){
                ans[k][0] = i + 1;
                ans[k][1] = j + 1;
                ans[k][2] = min;
                k++;
            }

        }
    }
    printf("%d\n", k);
    for (i = 0; i < k; i++){
        printf("%d %d %d\n", ans[i][0], ans[i][1], ans[i][2]);
    }
    return 0;
}
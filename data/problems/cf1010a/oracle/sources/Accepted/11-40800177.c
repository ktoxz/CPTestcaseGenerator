#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    int count[2000] ={0};
    int arr[1000] ={0}; 
    int n,m,i;
    scanf("%d %d",&n,&m);
    double a[n];
    double b[n];
    for(i=0;i<n;i++){
        scanf("%lf",&a[i]);
    }
    for(i=0;i<n;i++){
        scanf("%lf",&b[i]);
    }
    double low,high;
    double mid;
    low = 0;
    high = 3000000000.000000000;
    while(high-low > 0.0000001){
        
        mid = (low+high)/2;
        int flag = 1;
        double w = m;
        w=w+mid;
        for(i=0;i<n;i++){
            if(i==0){
                w=w-w/a[i];
                if(w<m) flag = 0;
            }
            else{
                w = w - w/b[i];
                if(w<m) flag = 0;
                w = w - w/a[i];
                if(w<m) flag = 0;
            }
        }
        w = w - w/b[0];
        if(w<m) flag = 0;
        //printf("%lf %d\n",mid,flag);
        if(flag==1){
            high = mid;
        }
        else{
            if(mid > 1000000000){
                printf("-1\n");
                return 0;
            }
            low = mid;
        }
    }
    printf("%lf\n",mid);
}
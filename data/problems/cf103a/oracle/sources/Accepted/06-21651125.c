#include<stdio.h>

int main (){long long int  n,question[100],i,j,clicks=0;while((scanf("%lld",&n))==1){clicks=0;for(i=0;i<n;i++){scanf("%lld",&question[i]);clicks=clicks+question[i];if(i!=0)clicks=clicks+((question[i]-1)*i);}printf("%lld\n",clicks);}return 0;}
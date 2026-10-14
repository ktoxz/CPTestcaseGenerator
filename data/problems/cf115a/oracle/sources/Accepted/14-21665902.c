#include<stdio.h>

int main()

{

int n,a[2001],k,i,m=1,j;

scanf("%d",&n);

for(i=1;i<=n;i++)

scanf("%d",&a[i]);

for(i=1;i<=n;i++)

{   

k=1;

j=i;

while(a[j]>0)

{

j=a[j];

k++;

}

if(k>m)

m=k;

}

printf("%d",m);

}
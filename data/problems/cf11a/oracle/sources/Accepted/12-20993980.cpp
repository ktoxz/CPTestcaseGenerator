#include<stdio.h>

int main()

{

long long int a[3000],n,d,k=0,i,c;

scanf("%lld%lld",&n,&d);

for(i=0;i<n;i++)

{

scanf("%lld",&a[i]);

if((a[i-1]>=a[i])&&(i>0))

{

c=((a[i-1]-a[i])/d)+1;

k=k+c;

a[i]=a[i]+c*d;

}}

printf("%lld",k);

return 0;

}
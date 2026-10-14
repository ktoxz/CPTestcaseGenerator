#include<stdio.h>

int main()
{
  int n,d;
  int a[2005];
  int i,j,k,min,diff,tmp,tmp2;
  scanf("%d%d",&n,&d);
  for(i=0;i<n;i++)
    scanf("%d",&a[i]);
  min=0;
  
  for(i=1;i<n;i++)
   if(a[i-1]>=a[i]){
     if(a[i-1]==a[i]){min=min+1;a[i]=a[i]+d;}
     else {diff=a[i-1]-a[i];tmp=diff/d;tmp2=diff%d;if(tmp2!=0) tmp2=1; min=min+tmp+tmp2;a[i]+=tmp*d+tmp2*d;if(a[i]==a[i-1]) {min=min+1;a[i]+=d;} }
   }
  
  printf("%d\n",min);

return 0;
}
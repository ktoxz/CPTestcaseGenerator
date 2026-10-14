#include<iostream>
#include<cstdio>
#include<vector>
using namespace std;
int main()
{
 vector<int> x(100);
 int n,a[100][4];
 scanf("%d",&n);
 int i,j,f,mini;
 for(i=0;i<n;i++)
 {
  scanf("%d%d%d%d",&a[i][0],&a[i][1],&a[i][2],&a[i][3]);
 }
 for(i=0;i<n;i++)
 {
  f=0;
  for(j=0;j<n;j++)
  {
   if((i!=j)&&(a[i][0]<a[j][0])&&(a[i][1]<a[j][1])&&(a[i][2]<a[j][2])&&(a[i][3]<a[j][3]))
   {
    f=1;
    break;
   }
  }
  if(f==1)
  x[i]=1;
 }
 mini=-1;
 int mini1;
 for(i=0;i<n;i++)
 {
  if(x[i]==0)
  { 
   if((mini==-1)||(mini>a[i][3]))
   {
    mini=a[i][3];
    mini1=i;
   }
  }
 }
 cout<<mini1+1<<"\n";
 return(0);
}
#include<bits/stdc++.h>
using namespace std;
int n,m,org;
int a[10005];
double func(int x,double s)
{
	double a1=s-n+1;
	int i;
	double res=1.0;
	for(i=0;;i++)
	{
		res=res*a1/(a1+n-1);
		if(a1==s-x-n+2)
		break;
		a1--;
		
		
	}
	return res;
}
int main()
{	int i,j;
	double sum=0.0;
	scanf("%d%d%d",&n,&m,&org);
	for(i=0;i<m;i++)
	{
		scanf("%d",&a[i]);
		sum+=a[i];
	}
	a[org-1]-=1;
	sum--;
	if(sum<n-1)
	{
		printf("%d\n",-1);
	}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	else
	
	if(a[org-1]==0)
	printf("%d\n",0);
	else
	if(sum-a[org-1]<n-1)
	{
		printf("%d\n",1);
	}
	else
	printf("%lf\n",1-func(a[org-1],sum));
	
}
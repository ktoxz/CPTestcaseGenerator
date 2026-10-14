#include<bits/stdc++.h>
using namespace std;
int n,k,x,y;
int main()
{
	scanf("%d%d",&n,&k);y=k;
	for(int i=1;i<=n;i++)scanf("%d",&x),x%=k,y=__gcd(x,y);
	printf("%d\n",k/y);
	for(int i=0;i<k/y;i++)printf("%d ",i*y);puts("");
	return 0;
}
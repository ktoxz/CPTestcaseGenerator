#include<bits/stdc++.h>
using namespace std;
const int maxn=120000+10;
map<int,int>ma;
int num[maxn];
int main()
{
	int n;
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		scanf("%d",&num[i]);
		ma[num[i]]++;
	}
	int ans=0;
	for(int i=1;i<=n;i++)
	{
		int fla=0;
		ma[num[i]]--;
		for(int j=0;(((long long)1)<<j)<=2*1e9;j++)
		{	
			if((1<<j)<=num[i])continue;
			if(ma[(1<<j)-num[i]])fla=1;
		}
		ans+=fla;
		ma[num[i]]++;
	}
	cout<<n-ans<<endl;
   	return 0;
}
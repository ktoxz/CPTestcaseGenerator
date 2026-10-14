//#include <bits/stdc++.h>
#include <iostream>
#include <vector>
#include <list>
using namespace std;
typedef unsigned long long ull;
typedef long long int ll;
typedef vector<long long int> vi;
typedef pair<int, int> ii;
typedef vector<ii> vii;
int visit[100009],check[100009];
vector<int > a[100009];
void bfs(int x)
{
	int flag;
	visit[x]=1;
	list<int> q;
	q.push_back(x);
	while(!q.empty())
	{
		x=q.front();
		q.pop_front();
		flag=0;
		for(int i=0;i<a[x].size();i++)
		{
			if(visit[a[x][i]]==0)
			{
				flag=1;
				q.push_back(a[x][i]);
				visit[a[x][i]]=1;
				check[a[x][i]]=check[x]+1;
			}
		}
	}
}
int main()
{
	ios_base::sync_with_stdio(0);cin.tie(NULL);cout.tie(NULL);
	int n,u,t[2005]={0},i,j=0,v,f=0,h[2005]={0},cnt=0;
	cin>>n;
	for(i=1;i<=n;i++)
	{
		cin>>u; 
		if(u==-1)
			t[j]=i,j++;
		a[u].push_back(i);
		//a[i].push_back(u);
	}
	for(i=0;i<j;i++)
	{
		//cout<<t[i]<<" ";
		if(t[i]!=0)
			bfs(t[i]);
	}
	//cout<<endl;
	for(i=1;i<=n;i++)
	{
		//cout<<check[i]<<" ";
		if(check[i]==0)
			h[check[i]]++;
		if(check[i]!=0)
			h[check[i]]++;
		//visit[i]=0;
		//check[i]=0;		
		a[i].clear();
	}
	for(i=0;i<=n;i++)
	{
		if(h[i]!=0)
			cnt++;
	}
	cout<<cnt;
	return 0;
}
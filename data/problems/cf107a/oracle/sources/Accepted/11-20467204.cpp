// Shalin

#include <bits/stdc++.h>

#include <stdio.h>

#include <string.h>

#include <stdlib.h>

#include <math.h>

#include <limits.h>

using namespace std;

#define si(x) scanf("%d",&x)

#define slli(x) scanf("%lld",&x);

#define sc(x) scanf("%c",&x);

#define ss(x) scanf("%s",x);

#define sd(x) scanf("%lf",&x);

#define bitcount __builtin_popcount

#define gcd __gcd

#define llu long long unsigned int

#define lli long long int

#define fi first

#define se second

#define pb push_back

#define mod 1000000007

#define mp make_pair

#define vi vector<int>

#define vlli vector<long long int>

#define pii pair<int,int>

int last,mini=1e9;

vector<pii> adj[1010];

vector<bool> visited(1010,0),in(1010,0),out(1010,0);

void dfs(int src)

{

	int i,j,k,len=adj[src].size();

	visited[src]=1;

	if(len==0 and in[src]==1 and out[src]==0)

		last=src;

	for(i=0;i<len;i++)

	{

		if(visited[adj[src][i].fi]==0)

		{

			mini=min(mini,adj[src][i].se);

			dfs(adj[src][i].fi);

		}

	}

}

int main()

{

	//freopen("input.txt","r",stdin);

    //freopen("output.txt","w",stdout);

	int n,p,i,j,k;si(n);si(p);

	for(i=0;i<p;i++)

	{

		int a,b,d;

		si(a);si(b);si(d);

		adj[a].pb(mp(b,d));

		in[b]=1;out[a]=1;

	}	

	vector< pair< pair<int,int>, int> > ans;

	for(i=1;i<=n;i++)

	{

		if(in[i]==0 and out[i]==1 and visited[i]==0)

		{

			last=0;

			mini=1e9;

			dfs(i);

			if(last!=0)

				ans.pb(mp(mp(i,last),mini));

		}

	}

	sort(ans.begin(),ans.end());

	int sz=ans.size();

	cout<<sz<<endl;

	for(i=0;i<sz;i++)

		cout<<ans[i].fi.fi<<" "<<ans[i].fi.se<<" "<<ans[i].se<<endl;

	return 0;

}
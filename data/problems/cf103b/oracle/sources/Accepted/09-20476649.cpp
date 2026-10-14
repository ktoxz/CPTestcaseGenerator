#include<bits/stdc++.h>

using namespace std;

typedef long long int ll;

vector<ll>v[100009];

ll cnt=0,l=0,p=1;

ll z=0,y=0,q=0;

ll visit[100009]={0};

ll visit1[100009]={0};

void dfs(int x)

{

	visit[x]=1;

	for(int i=0;i<v[x].size();i++)

	{

		

		if(visit[v[x][i]]==0) 

		{

			cnt++;

		//	cout<<cnt<<" ";

		

			dfs(v[x][i]);

		}

	}

}

/*void dfs1(int x,int q)

{

	visit1[x]=1;

	q++;

	for(int i=0;i<v[x].size();i++)

	{

		if(visit1[v[x][i]]==0)

		{

			

			

			if(q>y)

			{

				y=q;

		//	cout<<y<<" "<<v[x][i]<<endl;

			}

			dfs1(v[x][i],q);

		}

	}

}*/

int main()

{ios_base::sync_with_stdio(0);



	ll i,j,k,n,m,l=0;

	cin>>n>>m;

	

	for(i=0;i<m;i++)

	{

		cin>>j>>k;

		v[j].push_back(k);

		v[k].push_back(j);

	}

	if(m!=n)

	{

		cout<<"NO";

		return 0;

	}

/*	for(i=1;i<=n;i++)

	{

	/*	if(visit[i]==0)

		{

			l++;

			cout<<l<<" ";

			dfs(i);

		}

		if(l>1)

		{

			cout<<"NO";

			return 0;

		}

	}*/

	dfs(i);

	//cout<<cnt;

	if(cnt==n-1)

	cout<<"FHTAGN!";

	else

	cout<<"NO";

}
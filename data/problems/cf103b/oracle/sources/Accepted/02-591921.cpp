#include <iostream>
#include <fstream>
#include <vector>
#include <deque>

using namespace std;

#define tr(i, x) for (typeof(x.begin()) i = x.begin(); i != x.end(); ++ i)
#define pb push_back
#define MaxiN 105

int N, M;
int Deg[MaxiN];
bool Vis[MaxiN];
vector <int> Adj[MaxiN];

bool Check()
{
	if (N != M)
		return 0;
	if (N < 3)
		return 0;
	for (int i = 1; i <= M; ++ i)
	{
		int X, Y;
		scanf("%d%d", &X, &Y);
		Adj[X].pb(Y);
		Adj[Y].pb(X);
		++ Deg[X];
		++ Deg[Y];
	}
	deque <int> Q;
	for (int i = 1; i <= N; ++ i)
		if (Deg[i] == 1)
			Q.pb(i);
	while (!Q.empty())
	{
		int Cur = Q.front();
		Q.pop_front();
		Vis[Cur] = 1;
		-- Deg[Cur];
		tr (it, Adj[Cur])
			if (!Vis[*it] && -- Deg[*it] == 1)
				Q.pb(*it);
	}
	for (int i = 1; i <= N; ++ i)
		if (Deg[i] > 0)
		{
			int l = 0;
			for (int j = i; Deg[j] > 0; ++ l)
			{
				Deg[j] = 0;
				Vis[j] = 1;
				tr (it, Adj[j])
					if (Deg[*it] > 0)
					{
						j = *it;
						break;
					}
			}
			if (l < 3)
				return 0;
			break;
		}
	for (int i = 1; i <= N; ++ i)
		if (!Vis[i])
			return 0;
	return 1;
}

int main()
{
	scanf("%d%d", &N, &M);
	puts(Check() ? "FHTAGN!" : "NO");
}
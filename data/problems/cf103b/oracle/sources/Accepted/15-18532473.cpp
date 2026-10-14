/*

 * 103BCthulhu.cpp

 *

 *  Created on: Jun 16, 2016

 *      Author: Hazem

 *	Feedback:

 *		-

 *		-

 *		-

 */



#include <iostream>

#include <string>

#include <set>

#include <map>

#include <stack>

#include <queue>

#include <vector>

#include <utility>

#include <iomanip>

#include <sstream>

#include <bitset>

#include <cstdlib>

#include <iterator>

#include <algorithm>

/// C Header Files

#include <cstdio>

#include <cctype>

#include <cmath>

#include <math.h>

#include <ctime>

#include <cstring>

#include <unordered_set>



using namespace std;



typedef pair<int, int> pii;

typedef pair<int, pii> piii;



#define SET(a)                memset( a, -1,    sizeof a )

#define CLR(a)                memset( a,  0,    sizeof a )

#define MEM(a,val)            memset( a,  val,  sizeof(a) )

#define pb                    push_back

#define all(x)                (x).begin(), (x).end()

#define sz(a)                 int((a).size())

#define ff                    first

#define ss                    second

#define mp                    make_pair

#define nl                    "\n"



vector<int> adj[101];

int vis[1000];

int level[1000];

int n, m;

int cycles;

int csz;

int viscyc[1000];

void detect(int cur, int par, int k) {

	vis[cur] = 1;

	level[cur] = k;

	for (int i = 0; i < adj[cur].size(); i++) {

//		cout<<" "<<cur<<" "<<i<<endl;

		if(adj[cur][i] == -1)

			continue;

		if (vis[adj[cur][i]] && adj[cur][i] != par) {

//			cout<<cur<<" "<<adj[cur][i]<<endl;

			cycles++;

			for(int x = 0; x < adj[adj[cur][i]].size(); x++)

				adj[adj[cur][i]][x] = (adj[adj[cur][i]][x] == cur)?  -1 : adj[adj[cur][i]][x];

			csz = level[cur] - level[adj[cur][i]] + 1;

		}

		if (!vis[adj[cur][i]]) {

			detect(adj[cur][i], cur, k + 1);

		}

	}



}

int main() {

	ios_base::sync_with_stdio(false);

	cin.tie(0);

	cout.tie(0);

	cin >> n >> m;

	while (m--) {

		int u, v;

		cin >> u >> v;

		adj[u].pb(v);

		adj[v].pb(u);

	}

	stack<int> s;

	detect(1, 0, 1);

	for (int i = 1; i <= n; i++)

		if (!vis[i]) {

			cout << "NO" << endl;

			return 0;

		}

	(cycles == 1 && csz >= 3) ? cout << "FHTAGN!" << nl : cout << "NO" << nl;

	return 0;

}
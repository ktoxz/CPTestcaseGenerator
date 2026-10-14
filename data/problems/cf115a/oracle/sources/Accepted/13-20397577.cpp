#include <bits/stdc++.h>

using namespace std;

 

#define fr first

#define sc second

#define null NULL

#define mp make_pair

#define pb push_back

#define LN(A) strlen(A)

#define SZ(A) int(A.size())

#define All(A) A.begin(), A.end()

#define rAll(A) A.rbegin(), A.rend()



typedef long long ll;

typedef vector<int> vi;

typedef pair<int, int> ii;

const double EPS = 1e-15, PI = acos(-1);

const int MOD = int(1e9) + 7, MX = int(1e6) + 1;



int N, G[2001][2001], P[10010], vis[10010];



int dfs(int pr) {

  int cnt = 1;

  for(int i = 1; i <= N; i++)

    if(G[pr][i]) cnt = max(cnt, 1 + dfs(i));

  return cnt;

}



void solve() {

  scanf("%d", &N);

  memset(P, -1, sizeof P);

  for(int i = 1; i <= N; i++) {

    scanf("%d", &P[i]);

    if(P[i] != -1) G[P[i]][i] = 1;

  }

  int ans = 0;

  for(int i = 1; i <= N; i++) 

    if(P[i] == -1) ans = max(ans, dfs(i));

  printf("%d\n", ans);

}



int main() {

#ifndef ONLINE_JUDGE

  freopen("in.txt", "r", stdin);

  // freopen("out.txt", "w", stdout);

#else

  // freopen("killer.in", "r", stdin);

#endif

  solve();

}
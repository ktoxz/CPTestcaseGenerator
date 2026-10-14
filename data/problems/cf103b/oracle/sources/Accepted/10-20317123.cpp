#include <bits/stdc++.h>

using namespace std;

void in(){

    ios_base::sync_with_stdio(0);

    cin.tie(NULL);

    #ifndef ONLINE_JUDGE

    freopen("in.txt","r",stdin);

    #endif

}

#define rep(a, b, c) for(ll (a) = (b); (a) <= (c); ++(a))

#define ALL(v) (v.begin(),v.end())

#define rev(a, b, c) for(ll (a) = (b); (a) >= (c); --(a))

#define clr(a, b) memset((a), (b), sizeof(a))

#define pb push_back

#define mp make_pair

#define fi first

#define se second

typedef long long ll;

typedef pair<ll, ll> pll;

typedef vector<pll> vll;

const ll inf =LLONG_MAX/2;

const ll MX = 101;

vector<int>g[MX];

int src;

bool vis[MX];

void dfs(int cur){

    vis[cur] = true;

    for(int x : g[cur]){

        if(vis[x]) continue;

        dfs(x);

    }

}

int main()

{

    in();

    int u,v,n,m;

    cin>>n>>m;

    rep(i,0,m-1){

    cin>>u>>v;

    u--;v--;

    g[u].pb(v);

    g[v].pb(u);

    }

    if(m == 0){

         cout<<"NO\n";

         return 0;

    }

    dfs(u);

    bool f = 0;

    rep(i,0,n-1)if(!vis[i])f = 1;

    if(m != n)f= 1;

    if(f)cout<<"NO\n";

    else cout<<"FHTAGN!\n";

    return 0;

}
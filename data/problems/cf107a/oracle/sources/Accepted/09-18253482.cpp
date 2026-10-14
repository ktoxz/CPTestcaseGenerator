#include <bits/stdc++.h>

#define f first

#define s second

#define ll long long

#define mp make_pair

#define pb push_back

#define sqr(x) (x)*(x)



using namespace std;



double eps = 1e-9;

const int INF = 1e9+7;

const int MAXN = int (3e5+7);



int n, p, mini, last, a[1007], u[1007];

pair <int, int> g[1007];

vector < pair < pair <int, int>, int > > v;



void dfs(int v) {

	u[v] = 1;

	last = v;

	if(g[v].f != 0) {

		mini = min(mini, g[v].s);

		dfs(g[v].f);

	}

}



int main () { 

   	//freopen("input.in", "r", stdin);

   	//freopen("output.txt", "w", stdout);  

    

    cin >> n >> p;

    if(p == n) {

    	cout << 0;

    	return 0;

    }

    for(int i = 0; i < p; i ++) {

    	int x, y, d;

    	cin >> x >> y >> d;

    	a[y] = 1;

    	g[x] = mp(y, d);

    }

    for(int i = 1; i <= n; i ++) {

    	if(!a[i]) {

    		mini = INF;

    		dfs(i);

    		if(mini != INF)

    			v.pb(mp(mp(i, last), mini));

    	}

    }

    cout << v.size() << endl;

    for(int i = 0; i < v.size(); i ++) {

    	cout << v[i].f.f << " " << v[i].f.s << " " << v[i].s << endl;

    }

    return 0;

}
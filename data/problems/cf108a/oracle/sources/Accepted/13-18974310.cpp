#include <bits/stdc++.h>

using namespace std;



typedef long long ll;

typedef long double ld;

typedef pair<double,double> dd;

typedef pair<ll,ll> pll;

typedef pair<string,int> psi;

typedef pair<int,int> ii;

typedef vector<int> vi;

typedef vector<ll> vll;

typedef vector<pll> vpll;

typedef vector<vector<int> > vvi;

typedef vector<vector<ll> > vvll;

typedef vector<vector<ii> > vvip;

typedef vector<ii> vii;

#define pb push_back

#define F first

#define S second

#define MOD 1000000007

#define NA -1

#define ALL(v) v.begin(),v.end()

#define mp make_pair

#define rep(i, n) for (int (i) = 0; (i) < (n); (i) ++)

#define rep1(i, n) for (int (i) = 1; (i) <= (n); (i) ++)

#define FOR(i, a, b) for (int (i) = (a); (i) <= (b); (i)++)

#define db(x) {cout << #x << " = " << (x) << endl;}

#define dba(a, x, y) {cout<<#a<<" :";FOR(i123,x,y)cout<<setw(4)<<(a)[i123];cout<<endl;}

#define foreach(e, x) for (__typeof(x.begin()) e = x.begin(); e != x.end(); e++)

#define clr(x) memset(x,0,sizeof(x));

#define sz(x) int((x).size())

#define endl '\n'

const int INF = INT_MAX;

const ll INFL = LLONG_MAX;

//const ld PI = acos(-1);

#define PI acos(-1)

#define re return 

typedef pair<pll,ll> ppll;

int dx[] = {1, -1, 0, 0};

int dy[] = {0, 0, 1, -1};



int n;

int m;



int f (int x) {

	int a = x / 60, b = x % 60;

	re (a / 10 == b % 10) && (a % 10 == b / 10);

}



int main () {

	int a, b;

	scanf ("%d:%d", &a, &b);	

	int s = (a * 60 + b + 1) % 1440;

	while (!f (s)) s = (s + 1) % 1440;

	printf ("%02d:%02d\n", s / 60, s % 60);

	return 0;

}
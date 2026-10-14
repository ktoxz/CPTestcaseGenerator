#include<iostream>
#include <fstream>
#include <iomanip>
#include<algorithm>
#include<string>
#include<random>
#include<vector>
#include<list>
#include<set>
#include<math.h>
#include<map>
#include<complex>

#define Ri0			for(int i=0;i<n;i++)
#define Ri1			for(int i=1;i<=n;i++)
#define lli          long long int
#define pb          push_back
#define pii         pair<lli,lli>
#define vi          vector< lli>
#define iii			tuple<lli,lli,lli>
#define ST			get<0>
#define ND			get<1>
#define RD			get<2>
#define TH			get<3>
#define pi			3.141592653589793238462
#define double      long double
#define CHECK_BIT(var,pos) ((var) & (1<<(pos)))
#define ABC			26
using namespace std;

typedef complex<double>	com;

unsigned GCD(unsigned u, unsigned v) {
	unsigned r;
	while (v != 0) {
		r = u % v;
		u = v;
		v = r;
	}
	return u;
}

struct DSU
{
	vi deg;
	vi par;
	lli sum;
	DSU() {}
	DSU(lli n)
	{
		deg.resize(n, 0);
		par.resize(n, -1);
		sum = n;
	}
	lli find(lli x)
	{
		if (par[x] == -1) return x;
		return par[x] = find(par[x]);
	}
	void uni(lli x, lli y)
	{
		x = find(x); y = find(y);
		if ((x != -1 || y != -1) && x == y) return;
		sum--;
		if (deg[x] < deg[y]) par[x] = y;
		else {
			deg[x] += (deg[x] == deg[y]);
			par[y] = x;
		}
	}
};



lli mod = 998244353, inf = 4e18;
lli sum = 0;
lli tmp3 = 0, tmp = 0, tmp2 = 0, comb = 1;
vector<lli> arr, check,st;
lli n, m = 0, q;
lli maxi = 0, mini = inf;
string s2, s;
vector<vi> g;
lli high = 0;
char c;
multiset<lli> h;

lli rec(lli n, lli m)
{
	if (n <= 0) return inf;
	if (m == 0)
	{
		return 0;
	}
	if (arr[m - 1] == 0) return 0;
	lli ans=inf,fin=0;
	for (int i = 1; i <= arr[m - 1]; i++)
	{
		ans = min(arr[m - 1] / i, rec(n - i, m - 1));
		fin = max(ans, fin);
		if (n == 4)
		{
			lli x = 5;
		}
	}
	return fin;
}

int main()
{
	ios::sync_with_stdio(false), cin.tie(nullptr);
	lli k;
	cin >> n >> k;
	arr.resize(k,0);
	lli g;
	for (int i = 0; i < n; i++)
	{
		cin >> tmp;
		arr[tmp % k]=1;
		//if(arr[tmp % k]) g = tmp % k;
	}
	g = k;
	for (int i = 1; i < k; i++)
	{
		if (arr[i] == 1) g = GCD(g, i);
	}
	//if()
	cout << k / g << endl;
	for (int i = 0; i < k; i += g) cout << i << ' ';
	return 0;
}
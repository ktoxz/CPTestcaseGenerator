#include <string>
#include <cctype>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <cstring>
#include <stack>
#include <bitset>
#include <iostream>
#include <sstream>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <cstdlib>
#include <cstdio>
#include <queue>
#include <stack>
#include <functional>
#include <utility>
#include <iomanip>
#include <ctime>
using namespace std;
#define SZ(a) (int)(a).size()
#define FOR(i,a,b) for (int i=(a); i<=(b); ++i)
#define REP(i,n) for (int i=0; i<(n); ++i)
#define ALL(c) c.begin(), c.end()
#define CLR(c,n) memset(c,n,sizeof(c))
#define TR(container, it) for(typeof(container.begin()) it = container.begin(); it != container.end(); it++)
#define CONTAIN(container, it) (container.find(it)!=container.end())
const int INF=0x3F3F3F3F;
template <class T> inline T& checkmin(T& a, T b) {if (b<a) a=b;}
template <class T> inline T& checkmax(T& a, T b) {if (b>a) a=b;}
typedef long long LL;
typedef vector<int> VI;
typedef vector<VI> VII;
typedef vector<string> VS;
typedef pair<int,int> PII;

int n, m, h, s[1024];
const int N=100000;
long double f[N+1];
long double c(int x, int y) {return f[x]-f[y]-f[x-y];}
int main() {
	f[0]=0;
	FOR(i,1,N) f[i]=f[i-1]+logl(i);
	cin>>n>>m>>h; FOR(i,1,m) cin>>s[i];
	int tot=accumulate(s,s+m+1,0);
	if (tot<n) cout << -1 << endl;
	else if (s[h]==1||n==1) cout << 0 << endl;
	else if (tot-s[h]<n-1) cout << 1 << endl;
	else {
		printf("%.7lf\n", 1-(double)expl(c(tot-s[h],n-1)-c(tot-1,n-1)));
	}

}
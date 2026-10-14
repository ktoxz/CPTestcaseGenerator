#include <vector> 
#include <list> 
#include <map> 
#include <set> 
#include <deque> 
#include <queue> 
#include <stack> 
#include <bitset> 
#include <algorithm> 
#include <functional> 
#include <numeric> 
#include <utility> 
#include <complex> 
#include <sstream> 
#include <iostream> 
#include <iomanip> 
#include <cstdio> 
#include <cmath> 
#include <cstdlib> 
#include <cstring> 
#include <ctime> 
#include <cassert> 
using namespace std;

#define SZ(X) ((int)(X.size()))
#define PB(X) push_back(X)
#define two(X) (1<<(X))
#define MP make_pair
#define FILL(a, b) memset(a, b, sizeof(a))
#define ALL(X) (X).begin(), (X).end()
#define IT iterator
#define COUNT(x) (__builtin_popcount(x))
#define fab(i,a,b) for(int i=(a);i<=(b);++i)
#define fba(i,b,a) for(int i=(b);i>=(a);--i)
#define fec(i,a)   for(typeof(a.end())i=a.begin();i!=a.end();++i)

typedef long long LL;
typedef vector < int > VI;
typedef vector < double > VD;
typedef pair< int, int > PII;
typedef set < int > SI;
const double pi = acos(-1.0);
const int inf = 1000000000LL;

int res, n, now(0);

int main()
{
	//freopen("a.in", "r", stdin);
	//freopen("a.out", "w", stdout);

	cin>> n;
	if(!n)cout<< 0<< endl;else
	{
		if(n < 0) n = -n;
		for(res = 1; ; res++)
		{
			LL t = (LL)res * (res + 1) / 2;
			if(t - n >= 0 && !((t-n)&1))
			break;
		}

		cout<< res<< endl;
	}

	return 0;
}
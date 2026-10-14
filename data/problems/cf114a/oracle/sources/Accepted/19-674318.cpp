#include <cassert>
#include <cctype>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <algorithm>
#include <bitset>
#include <deque>
#include <iostream>
#include <iomanip>
#include <list>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <utility>
#include <vector>

using namespace std;

typedef long long ll;
//typedef __int64 ll;
typedef long double ld;
typedef pair <int, int> pii;
typedef vector <int> vi;
typedef vector <string> vs;

const int INF = (int) 1E9;
const ll LINF = (ll) 4E18;

const ld PI = acos(-1.0);
const ld EPS = 1E-11;

#define FOR(i, a, b) for (i = (a); i <= (b); i++)
#define FORD(i, a, b) for (i = (a); i >= (b); i--)
#define REP(i, a) for (i = 0; i < (a); i++)
#define REPD(i, a) for (i = (a) - 1; i >= 0; i--)
#define FIT(it, v) for (typeof((v).begin())it = (v).begin(); it != (v).end(); ++it)
#define FITD(it, v) for (typeof((v).rbegin())it = (v).rbegin(); it != (v).rend(); ++it)

#define VAR(a, b) typeof(b) a(b)
#define ALL(v) (v).begin(), (v).end()
#define SET(a, x) memset((a), (x), sizeof(a))
#define SIZE(a) ((int)(a).size())

#define EXIST(a, b) (find(ALL(a), (b)) != (a).end())
#define SORT(x) sort(ALL(x))
#define GSORT(x) sort(ALL(x), greater<typeof(*((x).begin()))>())
#define UNIQUE(v) SORT(v); (v).resize(unique(ALL(v)) - (v).begin())
#define ENUM(v) FIT(it, (v)) cout << *it << " "; cout << endl

#define CL clear
#define PF push_front
#define PB push_back
#define MP make_pair
#define F first
#define S second

#define TWO(x) (1<<(X))

template<typename T> T gcd(T a, T b) { return (b == 0) ? abs(a) : gcd(b, a % b); }
template<typename T> inline T lcm(T a, T b) { return a / gcd(a, b) * b; }
template<typename T> inline T mod(T a, T b) { a %= b; if (a < 0) a += b; return a; }
template<typename T> inline T sqr(T x) { return x * x; }
template<typename T> inline T gmax(T a, T b) { return (a > b ? a : b); }
template<typename T> inline T gmin(T a, T b) { return (a < b ? a : b); }

template<typename T> inline string toString(T x) { ostringstream oss; oss << x; return oss.str(); }
inline ll toInt(const string& st) { istringstream iss(st); ll x; iss >> x; return x; }
inline ld toDouble(const string& st) { istringstream iss(st); ld x; iss >> x; return x; }

int main()
{
    ll a,b;
    cin>>a>>b;
    ll ta=a;
    ll res=0;
    while(true)
    {
        if(a>=b)break;
        a*=ta;
        res++;
    }
    if(a==b)cout<<"YES"<<"\n"<<res<<endl;
    else cout<<"NO"<<endl;

    return 0;
}
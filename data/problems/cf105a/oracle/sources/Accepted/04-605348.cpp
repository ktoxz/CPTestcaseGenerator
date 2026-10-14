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
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
using namespace std;

// Constants
const int INF = 0X3F3F3F3F;
const double PI = acos(-1.0);//3.1415926535897932384626433832795;
const double EPS = 1e-9;
const int days[] = {31,28,31,30,31,30,31,31,30,31,30,31};
const int dx[] = {-1,0,1,0},dy[] = {0,1,0,-1}; //4 direction
//const int dx[] = {-1,-1,-1,0,1,1,1,0},dy[] = {-1,0,1,1,1,0,-1,-1}; //8 direction
//const int dx[] = {2,1,-1,-2,-2,-1,1,2},dy[] = {1,2,2,1,-1,-2,-2,-1}; //Knight direction
//const int dx[] = {0,1,1,0,-1,-1},dy[] = {1,1,0,-1,-1,0}; //Hexagonal direction(col x row y)

// Deinfe
#define PB push_back
#define MP make_pair
#define SZ size()
#define V vector
#define A first
#define B second

#define FOR(i,s,e) for(int i=(s);i<=(int)(e);++i)
#define FORD(i,s,e) for(int i=(s);i>=(int)(e);--i)
#define REP(i,n) for(int i=0;i<(int)(n);++i)
#define REPD(i,n) for(int i=(n)-1;i>=0;--i)
#define FIT(it,x) for(typeof((x).begin()) it = (x).begin();it != (x).end();it++)
#define FITD(it,x) for(typeof((x).rbegin()) it = (x).rbegin();it != (x).rend();it++)

#define LET(a,b) typeof(b) a(b)
#define ALL(x) (x).begin(),(x).end()
#define CLR(x) memset((x),0,sizeof(x))
#define SET(a,b) memset((a),b,sizeof(a))
#define EXIST(a,b) (find(all(a),b)!=a.end())
#define SORT(x) sort(ALL(x))
#define GSORT(x) sort(ALL(x),greater<typeof((x).begin())>())
#define gsort(a,b) sort(a,b,greater<typeof(*a)>())
#define DEBUG(x) cerr << #x << ":" << x << '@' << endl
#define PRV(v) REP(vi,v.size()) cout << v[vi] << ' ';cout << endl

inline int sgn(double x) { return x < -EPS ? -1 : x > EPS ? 1 : 0; }
template<class T> inline T sqr(const T& x) { return x * x; }
template<class T> inline int toint(const T& x){ stringstream ss; ss << x; int r; ss >> r; return r; } 
template<class T> inline int todouble(const T& x){ stringstream ss; ss << x; double r; ss >> r; return r; } 
template<class T> inline string tostr(const T& x) { ostringstream os(""); os << x; return os.str(); }
template<class T> inline istream& operator << (istream& is, const T& a) { is.putback(a); return is; }
inline string tolower(string s){ REP(i,s.SZ) s[i] = tolower(s[i]); return s; }
inline string toupper(string s){ REP(i,s.SZ) s[i] = toupper(s[i]); return s; }
template<class T> void stov(string s,vector<T> &vi){vi.clear();istringstream sin(s);for(T v;sin>>v;vi.push_bakc(v));}//NOTES:stov(
template<class T> void vtos(vector<T> vi,string &s){ostringstream sout;for (int i=0;i<vi.size();i++){if(i>0)sout<<' ';sout<<vi[i];}s=sout.str();}

// Math
template<class T> inline T gcd(T a,T b)//NOTES:gcd(
{if(a<0)return gcd(-a,b);if(b<0)return gcd(a,-b);return (b==0)?a:gcd(b,a%b);}
template<class T> inline T lcm(T a,T b)//NOTES:lcm(
{ if(a<0)return lcm(-a,b);if(b<0)return lcm(a,-b);return a*(b/gcd(a,b));}
template<class T> inline vector<pair<T,int> > factorize(T n)//NOTES:factorize(
{vector<pair<T,int> > R;for (T i=2;n>1;){if (n%i==0){int C=0;for (;n%i==0;C++,n/=i);
R.push_back(make_pair(i,C));}i++;if (i>n/i) i=n;}if (n>1) R.push_back(make_pair(n,1));return R;}
template<class T> inline bool isprime(T n)//NOTES:isPrimeNumber(
{if(n<2)return false;for (T i=2;i*i<=n;i++) if (n%i==0) return false;return true;}
template<class T> inline T phi(T n)//NOTES:phi(
{vector<pair<T,int> > R=factorize(n);T r=n;for (int i=0;i<R.size();i++)r=r/R[i].first*(R[i].first-1);return r;}

// Types
typedef long long LL;
typedef double DB;
typedef stringstream SS;
typedef set < int > SI;
typedef pair < int, int > PII;
typedef vector < int > VI;
typedef vector < VI > VVI;
typedef vector < LL > VLL;
typedef vector < string > VS;
typedef vector < PII > VPII;
typedef map < string, int > MSI;
typedef map < int, int > MII;
typedef map < LL, int > MLLI;
typedef priority_queue<int> pq;
typedef priority_queue<int, vector<int>, greater<int> > pqg;

const int MAXN = 10086;
int a[MAXN];
vector<int> v;
map<string, int> mp;
int main() {
    int n, m;
    double k;
    while (scanf("%d%d%lf", &n, &m, &k) != EOF) {
        int value;
        mp.clear();
        string s;
        int kk = (int)(k * 100 + 0.5);
        for (int i = 0; i < n; i++) {
            cin >> s >> value;
            int v = value * kk;
            if (v >= 10000) {
                mp[s] = v;
            }
        }
        for (int i = 0; i < m; i++) {
            cin >> s;
            if (!mp.count(s)) {
                mp[s] = 0;
            }
        }
        cout << mp.size() << endl;
        for (map<string, int>::iterator it = mp.begin(); it != mp.end(); it++) {
            cout << it->first << ' ' << it->second / 100 << endl;
        }
    }
}
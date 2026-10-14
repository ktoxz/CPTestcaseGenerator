#include <iostream>
#include <cstdlib>
#include <cstdio>
#include <cstring>
#include <ctime>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <vector>
#include <list>
#include <utility>
#include <bitset>

using namespace std;

#define MP make_pair
#define FI first
#define SE second
#define PB push_back
#define PF push_front
#define E 2.7182818284590451

#define SET(a,x) memset(a,x,sizeof(a));
#define FOR(i,a,b) for (int i=a;i<=b;i++)
#define FORD(i,a,b) for (int i=a;i>=b;i--)
#define REP(i,n) for (int i=0;i<n;i++)
#define REPD(i,n) for (int i=n-1;i>=0;i--)
#define FIT(i,c) for (typeof((c).begin()) i=(c).begin();i!=(c).end();i++)
#define FITD(i,c) for (typeof((c).rbegin()) i=(c).rbegin();i!=(c).rend();i++)
#define ALL(c) (c).begin(),(c).end()
#define SIZE(c) (int)(c).size()

template<typename T> T gcd(T a, T b){return(a>b?(gcd(b,a)):(a==0?b:(gcd(b%a,a))));};
template<typename T> inline T lcm(T a, T b){return a*b/gcd(a,b);};
template<typename T> inline T sqr(T a){return a*a;};
template<typename T> inline T gmax(T a, T b){return(a>b?a:b);};
template<typename T> inline T gmin(T a, T b){return(a<b?a:b);};

typedef long long LL;
typedef pair<int, int> II;
typedef vector<int> VI;
typedef vector<string> VS;
typedef vector<pair<int, int> > VII;

inline double rad(double a){return(double)a*M_PI/180;}
inline double round(double x){return(x-floor(x)>=0.5?ceil(x):floor(x));}
pair<int,int> extended_euclid(pair<int,int> ss){
    if (ss.SE==0) return MP(1,0);
    pair<int,int> temp=extended_euclid(MP(ss.SE,ss.FI%ss.SE));
    return MP(temp.SE,temp.FI-temp.SE*(ss.FI/ss.SE));
}

const int maxn=0;
const int maxm=0;
const double eps=1e-9;
const int BASE=0;

map<string,double> ss;
int n,m;
double k;
int y;
vector<pair<string,double> > res;
void enter(){
    cin>>n>>m>>k;
    string s;
    double e;
    FOR(i,1,n){
        cin>>s>>e;
        e*=k;
        e=floor(e+1e-9);
        if (e<100) continue;
        ss[s]=e;
    }
    map<string,double>::iterator it;
    FOR(i,1,m){
        cin>>s;
        it=ss.find(s);
        if (it==ss.end()){
            ss[s]=0;
        }
    }
    FIT(it,ss){
        res.PB(*it);
    }
    sort(ALL(res));
}
void solve(){
    cout<<SIZE(res)<<endl;
    REP(i,SIZE(res)) cout<<res[i].FI<<" "<<floor(res[i].SE+1e-9)<<endl;
}
int main(){
    //freopen("input.txt","r",stdin);
    //freopen("output.txt","w",stdout);
    enter();
    solve();
    //cout<<endl<<clock()<<" ms";
    return 0;
}
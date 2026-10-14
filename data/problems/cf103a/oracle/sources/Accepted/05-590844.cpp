#include <iostream>
#include <string>
#include <map>
#include <queue>
#include <stack>
#include <algorithm>
#include <list>
#include <set>
#include <cmath>
#include <cstring>
#include <stdio.h>
#include <string.h>
#include <sstream>
#include <stdlib.h>
#include <vector>
#include <iomanip>

using namespace std;

#ifdef __GNUC__
typedef long long ll;typedef unsigned long long ull;
#else
typedef __int64 ll;  typedef unsigned __int64 ull;
#endif

#define INF 1<<28
#define SIZE 100
#define PI 3.141592653590
#define REP(i,n) for (i=0;i<n;i++)
#define REPE(i,n) for (i=0;i<=n;i++)
#define REV(i,n) for (i=n;i>=0;i--)
#define FOR(i,p,k) for (i=p; i<k;i++)
#define FORE(i,a,b) for (int i=a; i<=b; i++)
#define FOREACH(it,x) for(__typeof((x).begin()) it=(x.begin()); it!=(x).end(); ++it)

#define bug(x)    cout<< "->" <<#x<<": "<<x<<endl
#define Sort(x) sort(x.begin(),x.end())
#define Reverse(x) reverse(x.begin(),x.end())
#define MP(a,b) make_pair(a,b)
#define Clear(x,with) memset(x,with,sizeof(x))
#define Copy(c,r)   memcpy(c,r,sizeof(r))
#define SZ(x) (int)x.size()
#define length(x) (int)x.length()
#define All(x) x.begin(),x.end()
#define pb push_back
#define popcount(i) __builtin_popcount(i)
#define gcd(a,b)    __gcd(a,b)
#define lcm(a,b)    (a*(b/gcd(a,b)))
#define fs first
#define sc second
#define two(X) (1<<(X))
#define twoL(X) (((int64)(1))<<(X))
#define contain(S,X) (((S)&two(X))!=0)
#define containL(S,X) (((S)&twoL(X))!=0)
#define maximum(v) *max_element(All(v))
#define minimum(v) *min_element(All(v))
#define CS c_str()
#define CL clear()
#define findx(a,x) (find(All(a),x)-a.begin())
#define ERR 1e-7
#define Unique(v) sort((v).begin(),(v).end()),v.erase(unique(v.begin(),v.end()),v.end())

typedef pair<int,int> pii;
typedef pair<double,double> pdd;
typedef vector<int> vi;
typedef vector<double>vd;
typedef vector<ll>vll;
typedef vector<string> vs;
typedef vector<vi>vvi;
typedef vector<vll>vvll;
typedef vector<vd>vvd;
typedef vector<pii>vpii;
typedef map<string,int> msi;
typedef map<int,int>mii;
typedef map<pii,int>mpi;

template<class T> inline T euclide(T a,T b,T &x,T &y)
    {if(a<0){T d=euclide(-a,b,x,y);x=-x;return d;}
    if(b<0){T d=euclide(a,-b,x,y);y=-y;return d;}
    if(b==0){x=1;y=0;return a;}else{T d=euclide(b,a%b,x,y);T t=x;x=y;y=t-(a/b)*y;return d;}}
template<class T> inline void checkmin(T &a,T b){if(b<a) a=b;}
template<class T> inline void checkmax(T &a,T b){if(b>a) a=b;}
template<class T> T Abs(T x) {return x > 0 ? x : -x;}
template<class T> inline T sqr(T x){return x*x;}
template<class T> inline bool isPrime(T n){if(n<=1)return false;for (T i=2;i*i<=n;i++) if (n%i==0) return false;return true;}
template<class T> inline T Mod(T n,T m) {return (n%m+m)%m;} //For Positive Negative No.
template<class T> string toString(T n){ostringstream oss;oss<<n;oss.flush();return oss.str();}
int toInt(string s){int r=0;istringstream sin(s);sin>>r;return r;}
ll toLl(string s){ll r=0;istringstream sin(s); sin>>r; return r;}
template<class T> void debug(const T& e){cout<<e<<endl;}
template<class T1,class T2> void debug(const T1& e1,const T2& e2){cout<<e1<<"\t"<<e2<<endl;}
template<class T1,class T2,class T3> void debug(const T1& e1,const T2& e2,const T3& e3){cout<<e1<<"\t"<<e2<<"\t"<<e3<<endl;}
template<class T1,class T2,class T3,class T4> void debug(const T1& e1,const T2& e2,const T3& e3,const T4& e4){cout<<e1<<"\t"<<e2<<"\t"<<e3<<"\t"<<e4<<endl;}
template<class T1,class T2,class T3,class T4,class T5> void debug(const T1& e1,const T2& e2,const T3& e3,const T4& e4,const T5& e5){cout<<e1<<"\t"<<e2<<"\t"<<e3<<"\t"<<e4<<"\t"<<e5<<endl;}
template<class T> void debug(vector<T>& e){int i;REP(i,SZ(e)) cout<<e[i]<<" ";cout<<endl;}
template<class T> void debug(vector< basic_string<T> >& e){int i,j;REP(i,SZ(e)) {REP(j,SZ(e[i])) cout<<e[i][j];cout<<endl;} cout<<endl;}
template<class T> void debug(vector< vector<T> >& e,int row,int col){int i,j;REP(i,row) {REP(j,col) cout<<e[i][j]<<"\t";cout<<endl;} cout<<endl;}
template<class T> void debug(T e[SIZE][SIZE],int row,int col){int i,j;REP(i,row) {REP(j,col) cout<<e[i][j]<<" ";cout<<endl;}}

ll Pow(int B,int P){	ll R=1;	while(P>0)	{if(P%2==1)	R=(R*B);P/=2;B=(B*B);}return R;} //compute b^p
int BigMod(ll B,ll P,ll M){	ll R=1;	while(P>0)	{if(P%2==1){R=(R*B)%M;}P/=2;B=(B*B)%M;}	return (int)R;} //compute b^p%m
//struct pq{    int cost,node;bool operator<(const pq &b)const{return cost>b.cost;}};// Min Priority Queue
//bool comp(pq a,pq b){    return a.cost < b.cost;}   //Asc Sort by cost

//int dx[]={1,0,-1,0};int dy[]={0,1,0,-1}; //4 Direction
//int dx[]={1,1,0,-1,-1,-1,0,1};int dy[]={0,1,1,1,0,-1,-1,-1};//8 direction
//int dx[]={2,1,-1,-2,-2,-1,1,2};int dy[]={1,2,2,1,-1,-2,-2,-1};//Knight Direction
//int dx[6]={2,1,-1,-2,-1,1};int dy[6]={0,1,1,0,-1,-1}; //Hexagonal Direction


int main()
{
    int i,j,Case=1,test,N;
    long long a[110],res;
    
    
    while(scanf("%d",&N)==1)
    {
        for(i=0;i<N;i++)
        {
            cin>>a[i];
        }
        
        res=0;
        for(i=0;i<N;i++)
        {
            res+=((a[i]-1)*(i+1))+1;
        }
        
        cout<<res<<endl;
    }

    return 0;
}
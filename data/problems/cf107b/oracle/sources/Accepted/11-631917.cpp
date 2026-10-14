/*
 * Bidhan  <mail2bidhan@gmail.com>
 */
 
using namespace std;

#include <algorithm>
#include <bitset>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <list>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <vector>

#define rep(i,n) for(__typeof(n) i=0; i<(n); i++)
#define foreach(i,n) for(__typeof((n).begin())i =(x).begin();i!=(x).end();i++)
#define inf (1<<30)
#define linf (i64(1)<<61)
#define eps 1e-9
#define pb push_back
#define clr clear()
#define all(x) x.begin(),x.end()
#define sz(x) (int)x.size()
#define rev reverse
#define mem(x,val) memset((x),(val),sizeof(x));
#define read(x) freopen(x,"r",stdin);
#define rite(x) freopen(x,"w",stdout);
#define on(bit,pos) ((bit)|(__typeof(bit))1<<(pos-1))
#define off(bit,pos) ((bit)& ~((__typeof(bit))1<<(pos-1)))
#define check(bit,pos) ((bit)==((bit)|(__typeof(bit))1<<(pos-1)))

typedef long long i64;
typedef unsigned long long ui64;
typedef string st;
typedef double dbl;
typedef vector<int> vi;
typedef vector<st> vs;
typedef map<int,int> mii;
typedef map<st,int> msi;
typedef map<int,st> mis;
typedef set<int> si;
typedef set<st> ss;

dbl round(double x, int precision){return floor(x*pow(10.0,(double)precision)+0.5)/pow(10.0,(double)precision);}
st itoa(i64 a){if(!a)return "0";st ret;for(i64 i=a; i>0; i=i/10) ret+=((i%10)+48);rev(all(ret));return ret;}
int toi(st s){int r=0;istringstream sin(s);sin>>r;return r;}
i64 toi64(st s){i64 r=0;istringstream sin(s);sin>>r;return r;}
dbl tod(st s){double r=0;istringstream sin(s);sin>>r;return r;}
vs token(st a,st b){const char *q=a.c_str();while(count(all(b),*q)) q++;vs oot;while(*q){const char *e=q;while(*e&&!count(all(b),*e)) e++;oot.pb(st(q,e));q=e;while(count(all(b),*q))q++;}return oot;}

template<class T> inline T gcd(T a,T b) {if(a<0)return gcd(-a,b);if(b<0)return gcd(a,-b);return (b==0)?a:gcd(b,a%b);}
template<class T> inline T lcm(T a,T b) {if(a<0)return lcm(-a,b);if(b<0)return lcm(a,-b);return a*(b/gcd(a,b));}
template<class T> inline T sqr(T x){return x*x;}
template<class T> inline T power(T x,T p){if(!p) return 1;return x*power(x,p-1);}

const int mx=105;

int n,m,h;
int lft,rte,tot;

bool vis[mx][mx][mx][2];
dbl dp[mx][mx][mx][2];

dbl call(int nisi,int my,int othr,bool one)
{
    if( nisi== n) return one;
    
    if( !vis[nisi][my][othr][one])
    {
        vis[nisi][my][othr][one]=true;
        dbl lp= dbl(lft-my)/dbl(tot-my-othr);
        dbl rp=dbl(rte-othr)/dbl(tot-my-othr);
        
        dbl aa=0;
        if(my<lft) aa=lp*call(nisi+1,my+1,othr,1);
        dbl bb=0;
        if(othr<rte) bb=rp*call(nisi+1,my,othr+1,one);
        return dp[nisi][my][othr][one]=aa+bb;
    }
    return dp[nisi][my][othr][one];
}
int main()
{
    int jog=0;
    while( cin>> n>>m >>h)
    {
        for(int i=1; i<=m; i++)
        {
            int tt; scanf("%d",&tt);
            if(i==h) lft=tt-1;
            else rte+=tt;
            
            jog+=tt;
        }
        
        if(jog<n) { puts("-1.0"); return 0; }
        tot=lft+rte;
        n--;
        //cout << lft <<" "<<rte<<endl;
        printf("%.15lf\n",call(0,0,0,0));//<<endl;
    }
    return 0;
}
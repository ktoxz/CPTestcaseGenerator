//#pragma warning (disable: 4786)
//#pragma comment (linker, "/STACK:0x800000")

#include<cstdio>
#include<cstring>
#include<cstdlib>
#include<cctype>
#include<cmath>
#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<queue>
#include<map>
#include<algorithm>
#include<set>
#include<sstream>
#include<stack>
#define maxim 100
#define LLD long long int
#define LLU long long unsigned 
#define pi acos(-1.0)
#define inf 100010000
#define CLR(a) memset(a,0,sizeof(a))
#define SET(a) memset(a,-1,sizeof(a))
#define pb push_back
#define sz(a) ((int)a.size())
#define all(a) a.begin(),a.end()
#define eps 1e-9
#define rep(i,init,n) for(i=init;i<n;i++)
#define rem(i,init,n) for(i=init;i>n;i--)
#define area(x1,y1,x2,y2,x3,y3) ( x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2) )
#define sqr(x) ((x)*(x))
#define distSqr(x1,y1,x2,y2) ( sqr(x1-x2) + sqr(y1-y2) )
#define spDist(lat1,long1,lat2,long2,r) ( r * acos( sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(long1-long2) ) )
#define isEq(a,b) (fabs(a-b)<eps)
#define STR string
#define LF double
#define IT iterator
#define VI vector<int>
#define VLLD vector<LLD>
#define VS vector<STR>
#define VLF vector<LF>
#define MII map<int,int>
#define MIB map<int,bool>
#define MSI map<STR,int>
#define MSB map<STR,bool>
#define MSS map<STR,STR>
#define M2dII map<int,map<int,int> >
#define QI queue<int>
#define SI stack<int>
#define PII pair< int, int >
#define PPI pair< PII, int >
#define freq first
#define val second
#define VPII vector<PII>
#define MP make_pair

#define chkB(a,k) (bool)(a[k>>5] & (1<<(k&31)))
#define setB0(a,k) (a[k>>5] &= ~(1<<(k&31)))
#define setB1(a,k) (a[k>>5] |= (1<<(k&31)))

#define SD(a) scanf("%d",&a)
#define SHD(a) scanf("%hd",&a)
#define SLLD(a) scanf("%lld",&a)
#define SLLU(a) scanf("%llu",&a)
#define SF(a) scanf("%f",&a)
#define SLF(a) scanf("%lf",&a)
#define SC(a) scanf("%c",&a)
#define SS(a) scanf("%s",a)

#define foreach(i, c) for( __typeof( (c).begin() ) i = (c).begin(); i != (c).end(); ++i )

int diru[] = {-1,-1,-1,0,0,1,1,1};
int dirv[] = {-1,0,1,-1,1,-1,0,1};

using namespace std;

template< class T > T sq(T n) { return n*n; }
template< class T > T gcd(T a, T b) { return (b != 0 ? gcd<T>(b, a%b) : a); }
template< class T > T lcm(T a, T b) { return (a / gcd<T>(a, b) * b); }
template< class T > bool inside(T a, T b, T c) { return a<=b && b<=c; }
template< class T > void setmax(T &a, T b) { if(a < b) a = b; }
template< class T > void setmin(T &a, T b) { if(b < a) a = b; }
template< class T > T power(T N,T P){  return (P==0)?  1: N*power(N,P-1); }
char in[100010] ;

bool com( PII a, PII b )
{
    return ( a.freq<b.freq || (  a.freq==b.freq && a.val<b.val )  );
}
PII S[40] ;
int main()
{
    int n,T,t=1,m,i,j,k,x;
    //freopen("in.txt","r",stdin);
    //freopen("out.txt","w",stdout);
    //scanf("%d",&T);
    //for(t=1;t<=T;t++)
    while(scanf("%s",in)==1)
    //SS(in);
    //cin>>in ;
    {
        SD(k) ;
        int cnt[30] = {0} ;
        //rep(i,0,26)   cnt[i]=0 ;
        int l =strlen(in) ;
        int ans = 0 ;
        rep(i,0,l)
        {
            cnt[in[i]-'a'] ++ ;
            if(cnt[in[i]-'a']==1)   ans++;
        }
        //printf("%d\n",ans) ;
        
        rep(i,0,26)
        {
            S[i].val = i ;
            S[i].freq = cnt[i] ;
        }
        stable_sort(S,S+26,com) ;
        
        rep(i,0,26)
        {
            if(S[i].freq)
            {
                x = S[i].freq ;
                if( x>k )   break ;
                k-=x ;
                ans--;
                cnt[S[i].val] = -1 ;
            }
        }
        printf("%d\n",ans) ;
        rep(i,0,l)
        {
            if( cnt[in[i]-'a']!=-1 )    
            {
                putchar(in[i]) ;
            }
            
        }
        puts("") ;
            //scanf("%d",&m);
        //printf("Case %d: ",t);
    }
    return 0;
}
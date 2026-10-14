//                                ببِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيم



/*

Abu Rayhan Ahmad

Bangladesh University of Business & Technology(BUBT)

CSE,29th Intake,Section-05

*/

                //*If You Have a Good Personality,You Don't Need To Describe Yourself*\\





#include<bits/stdc++.h>

#include<iostream>

#include<cstdio>

#include<list>

#include<string>

#include<cstring>

#include<sstream>

#include<cctype>

#include<string.h>

#include<algorithm>

#include<cmath>

#include<stack>

#include<fstream>

#include<cstdlib>

#include<vector>

#include<map>

#include<set>

#include<utility>

#include<iomanip>

#include<queue>

#include<deque>

#include<iterator>

#include<assert.h>

#include<bitset>

#include<climits>

#include<ctime>

#include<complex>



using namespace std;



#define SET(a) memset(a,-1,sizeof(a))

#define ALL(a) a.begin(),a.end()

#define CLR(a) memset(a,0,sizeof(a))

#define PB push_back

#define PI acos(-1.0)

#define MP(a,b) make_pair(a,b)

#define PII pair<int,int>

#define PCC pair<char,char>

#define PIC pair<int,char>

#define PCI pair<char,int>

#define VS vector<string>

#define VI vector<int>

#define VC vector<char>

#define max3(a,b,c) max(a,max(b,c))

#define min3(a,b,c) min(a,min(b,c))

#define READ freopen("input.txt", "r", stdin)

#define WRITE freopen("output.txt", "w", stdout)

#define LL long long

#define FOR(i,a,b) for(int i=a;i<=b;i++)

#define RFOR(i,a,b) for(int i=a;i>=b;i--)

#define For(i,a) for(int i=0;i<a;i++)



#define S(a) scanf("%d",&a)

#define S2(a,b) scanf("%d%d",&a,&b)

#define S3(a,b,c) scanf("%d%d%d",&a,&b,&c)

#define SLL(a) scanf("%lld",&a)

#define SLL2(a,b) scanf("%lld%lld",&a,&b)

#define SLL3(a,b,c) scanf("%lld%lld%lld",&a,&b,&c)

#define SS(a) scanf("%s",a)

#define SC(a) scanf("%c",&a)

#define SD(a) scanf("%lf",&a)

#define P(a) printf("%d",a)

#define PLL(a) printf("%lld",a)

#define PD(a) printf("%lf",a)

#define PC(a) printf("%c",a)

#define PS(a) printf("%s",a)

#define KS printf("Case %d: ",kk++)

#define KN printf("Case %d:\n",kk++)

#define KH printf("Case #%d: ",kk++)

#define NL printf("\n")

#define DB cout<<"done"<<endl;

#define YES() cout<<"YES\n";

#define NO() cout<<"NO\n";

#define Yes() cout<<"Yes\n";

#define No() cout<<"No\n";

#define EPS 1e-9

#define MOD 1000000007

#define INF INT_MAX/3

#define MX 100010



template<typename T>inline string tostring(T a){ostringstream os("");os << a;return os.str();}

template<typename T>inline LL tolong(T a){LL res;istringstream os(a);os>>res;return res;}

template<typename T>inline VI parse(T str){VI res;int s;istringstream os(str);while(os>>s)res.PB(s);return res;}

template< class T > inline T _sqrt(T x) { return (T) sqrt( (double) x); }

template< class T > inline T _bigmod(T n,T m) {T ans=1,mult=n%MOD; while(m){ if(m & 1) ans=(ans*mult)%MOD; m>>=1; mult=(mult*mult)%MOD; } ans%=MOD; return ans;}

template< class T > inline T _modinv(T x) {return _bigmod(x,(T) MOD-2)%MOD;}

inline int LEN(string a) {return a.length();}

inline int LEN(char a[]) {return strlen(a);}

template<class T> inline T _gcd(T a, T b){return (b.chk()==0) ? a : _gcd(b, a % b);}

template< class T > inline T _lcm(T x,T y) { return x*y/_gcd(x,y);}



//int dx[]={1,0,-1,0};int dy[]={0,1,0,-1}; //4 Direction

//int dx[]={1,1,0,-1,-1,-1,0,1};int dy[]={0,1,1,1,0,-1,-1,-1};//8 direction

//int dx[]={2,1,-1,-2,-2,-1,1,2};int dy[]={1,2,2,1,-1,-2,-2,-1};//Knight Direction

//int dx[6]={2,1,-1,-2,-1,1};int dy[6]={0,1,1,0,-1,-1}; //Hexagonal Direction

bool compare(const pair<float,string>&i, const pair<float,string>&j)

{

    return i.first > j.first;

}

int in_c() { int c; for (; (c = getchar()) <= ' '; ) { if (!~c) throw ~0; } return c; }

const int mx = 1e5 + 7;

int EQ(double d) {

    if ( fabs(d) < EPS ) return 0;

    return d > EPS ? 1 : -1 ;

}

int main()

{

LL N,P1,P2,P3,T1,T2;

SLL3(N,P1,P2);

SLL3(P3,T1,T2);

LL L[1000],R[1000];

For(i,N)

{

    SLL2(L[i],R[i]);

}

LL ans=0;

For(i,N)

{

    ans+=(R[i]-L[i])*P1;

}

For(i,N-1)

{

    LL diff=L[i+1]-R[i];

    if(diff>(T1+T2)) ans+=(diff-T1-T2)*P3,diff=T1+T2;

    if(diff>T1) ans+=(diff-T1)*P2,diff=T1;

    ans+=diff*P1;

}

cout<<ans<<endl;

    return 0;

}
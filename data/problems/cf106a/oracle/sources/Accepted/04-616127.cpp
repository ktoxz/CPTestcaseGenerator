/**

  Author: Zafar Ahmad
  Reg.No: 2008331028
        SUST

**/

#include <algorithm>
#include <bitset>
#include <climits>
#include <cmath>
#include <complex>
#include <cstddef>
#include <cstdio>
#include <ctime>
#include <functional>
#include <iostream>
#include <iterator>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <utility>
#include <vector>
#include <ctype.h>
#include <memory.h>
#include <stdlib.h>
#include <string.h>

using namespace std;

#ifdef __GNUC__
typedef long long ll;typedef unsigned long long ull;
#else
typedef __int64 ll;  typedef unsigned __int64 ull;
#endif

#define REP(i,n)    for(i=0;i<n;i++)
#define REV(i,n)    for(i=n;i>=0;i--)
#define FOR(i,x,y)  for(i=x;i<=y;i++)

#define acu(x)      accumulate(x.begin(),x.end(),0)
#define EQ(a,b)     (fabs(a-b)<ERR)
#define max(a,b)    (a>b?a:b)
#define maximum(v)  *max_element(all(v))
#define mem(x,with) memset(x,(with),sizeof(x))
#define min(a,b)    (a<b?a:b)
#define minimum(v)  *min_element(all(v))
#define MP(X,Y)     make_pair(X,Y)
#define popcount(x) __builtin_popcount(x)
#define Reverse(x)  reverse(x.begin(),x.end())
#define Sort(x)     sort(x.begin(),x.end())
#define SZ(x)       (int)x.size()
#define UN(v)       sort((v).begin(),(v).end()),v.erase(unique(v.begin(),v.end()),v.end())

#define CROSS(a,b,c,d)  ((b.x-a.x)*(d.y-c.y) - (d.x-c.x)*(b.y-a.y))
#define DOT(a,b,c,d)    ((b.x-a.x)*(d.x-c.x) + (b.y-a.y)*(d.y-c.y))
#define two(x)      (1<<x)
#define twoL(X)     (((ll)(1))<<(X))

#define all(x)      (x).begin(), (x).end()
#define bug(x)      cout<< "->" <<#x<<": "<<x<<endl
#define CLR(x)      x.clear()
#define iter(c)     __typeof((c).begin())
#define MARK(n)     printf("MARK %d  LINE: %d\n",n,__LINE__);
#define tr(c, i)    for (iter(c) i = (c).begin(); i != (c).end(); ++i)

#define PB          push_back
#define PF          push_front
#define fs          first
#define sc          second

#define ERR         1e-9
#define oo          (1<<28)
#define SIZE        1000000
const double PI=acos(-1.0);

typedef pair<int,int>   pii;
typedef pair<double,double> pdd;
typedef vector<int>     vi;
typedef vector<double>  vd;
typedef vector<ll>      vll;
typedef vector<string>  vs;
typedef vector<vi>      vii;
typedef vector<vll>     vvll;
typedef vector<vd>      vvd;
typedef vector<pii>     vpii;
typedef map<string,int> msi;
typedef map<int,int>    mii;
typedef map<pii,int>    mpi;
typedef list<int>       li;
typedef istringstream   iss;

/** Printing **/
template<class T> void out(const vector<T> &a) { cout<<"array: "; for (int i=0;i<SZ(a);i++) cout<<a[i]<<" "; cout<<endl; cout.flush(); }
void binprint(int mask,int n)/**print a number in binary format with n length**/
  {int i;string s="";do{s+=(mask%2+'0');mask/=2;}while(mask);Reverse(s);s=string(max(n-SZ(s),0),'0')+s;for(i=SZ(s)-n;i<SZ(s);i++) printf("%c",s[i]);printf("\n");}
void ASCII_Chart() /**ASCII Chart**/
  {int i,j,k;printf("ASCII Chart:(30-129)\n");FOR(i,30,50){REP(j,5){k=i+j*20;printf("%3d---> '%c'   ",k,k);}printf("\n");}}

/**  MATH   **/
template<class T> inline T gcd(T a,T b) {if(a<0)return gcd(-a,b);if(b<0)return gcd(a,-b);return (b==0)?a:gcd(b,a%b);}
template<class T> inline T lcm(T a,T b) {if(a<0)return lcm(-a,b);if(b<0)return lcm(a,-b);return a*(b/gcd(a,b));}
template<class T> T Abs(T x) {return x > 0 ? x : -x;}
template<class T> inline T sqr(T x){return x*x;}/** NOTES:sqr **/
template<class T> inline T Mod(T n,T m) {return (n%m+m)%m;} /** For Positive Negative No. **/
int BigMod(ll B,ll P,ll M) /** compute b^p%m **/
  { ll R=1;	while(P>0)	{if(P%2==1){R=(R*B)%M;}P/=2;B=(B*B)%M;}	return (int)R;}
ll mulmod(ll a,ll b,ll c) /**calculates (a*b)%c taking into account that a*b might overflow **/
  { ll x = 0,y=a%c; while(b>0){ if(b%2 == 1){x=(x+y)%c;} y=(y*2)%c;b/= 2;}return x%c;}
ll mpow(ll x,ll k) { if( k==0) return 1; ll r=mpow(x,k/2); return k%2?(r*r*x):(r*r); }                 // Power Calculation function

/** Genarator **/
template<class T> inline vector<pair<T,int> > factorize(T n)/** NOTES:factorize( **/
  {vector<pair<T,int> > R;for (T i=2;n>1;){if (n%i==0){int C=0;for (;n%i==0;C++,n/=i);R.push_back(make_pair(i,C));}
   i++;if (i>n/i) i=n;}if (n>1) R.push_back(make_pair(n,1));return R;}
vector<string> SubstringGenerate(string str)/** Substring Generator **/
  {int i,j,len;vs store;len=SZ(str);REP(i,len) FOR(j,i,len)store.PB(str.substr(i,j-i+1));return store;}

/** Dicission **/
template<class T> inline bool isPrime(T n){if(n<=1)return false;for (T i=2;i*i<=n;i++) if (n%i==0) return false;return true;}
bool IsVowel(char ch){ch=tolower(ch);if(ch=='a' || ch=='e' || ch=='i' || ch=='o' || ch=='u')return true;return false;}
bool isUpperCase(char c){return c>='A' && c<='Z';}
bool isLowerCase(char c){return c>='a' && c<='z';}
bool isLetter(char c){return c>='A' && c<='Z' || c>='a' && c<='z';}//NOTES:isLetter(
bool isDigit(char c){return c>='0' && c<='9';}//NOTES:isDigit(

/** Conversion **/
double deg2rad(double x){ return (PI*x)/180.0; }
double rad2deg(double x){ return (180.0*x)/PI; }
template<class T> string toString(T n)/** NOTES:int,double is converted to string **/
  {ostringstream oss;oss<<n;oss.flush();return oss.str();}
int toInt(string s){int r=0;istringstream sin(s);sin>>r;return r;} /** String to Int **/
ll toLl(string s){ll r=0;istringstream sin(s); sin>>r; return r;}  /** String to Int **/
double toDouble(string s){double r=0;istringstream sin(s);sin>>r;return r;} /**NOTES:toDouble(**/
template<typename T> static void splitstr(const string &s, vector<T> &out)/**String TO vector**/
  { istringstream in(s);out.clear();copy(istream_iterator<T>(in), istream_iterator<T>(), back_inserter(out));}

/**For debugging **/
template<class T> void debug(T e){cout<<e<<endl;}
template<class T1,class T2> void debug(T1 e1,T2 e2){cout<<e1<<"\t"<<e2<<endl;}
template<class T1,class T2,class T3> void debug(T1 e1,T2 e2,T3 e3){cout<<e1<<"\t"<<e2<<"\t"<<e3<<endl;}
template<class T1,class T2,class T3,class T4> void debug(T1 e1,T2 e2,T3 e3,T4 e4){cout<<e1<<"\t"<<e2<<"\t"<<e3<<"\t"<<e4<<endl;}
template<class T1,class T2,class T3,class T4,class T5> void debug(T1 e1,T2 e2,T3 e3,T4 e4,T5 e5){cout<<e1<<"\t"<<e2<<"\t"<<e3<<"\t"<<e4<<"\t"<<e5<<endl;}
template<class T> void debug(vector<T> e){int i;REP(i,SZ(e)) cout<<e[i]<<" ";cout<<endl;}
template<class T> void debug(vector<T> e,int n){int i;REP(i,n) cout<<e[i]<<" ";cout<<endl;}
template<class T> void debug(vector< basic_string<T> > e){int i,j;REP(i,SZ(e)) {REP(j,SZ(e[i])) cout<<e[i][j];cout<<endl;} cout<<endl;}
template<class T> void debug(vector< basic_string<T> > e,int row,int col){int i,j;REP(i,row) {REP(j,col) cout<<e[i][j];cout<<endl;} cout<<endl;}
template<class T> void debug(vector< vector<T> > e,int row,int col){int i,j;REP(i,row) {REP(j,col) cout<<e[i][j]<<"\t";cout<<endl;} cout<<endl;}
template<class T> void debug(T e[SIZE][SIZE],int row,int col){int i,j;REP(i,row) {REP(j,col) cout<<e[i][j]<<" ";cout<<endl;}}
template<class T> void debug(T e[],int row){int i;REP(i,row) cout<<e[i]<<" ";cout<<endl;}

//struct pq{    int cost,node;bool operator<(const pq &b)const{return cost>b.cost;}};// Min Priority Queue
//typedef struct{int x,y;}P;P pvt;
//typedef struct{int x,y;}man;man PArray[1000];
//bool com(man a,man b){ if(a.x==b.x) return a.y<b.y; return a.x<b.x;}

/** max sizes in TC : [16000000] , [4000][4000] , [250][250][250] **/
/** max loop in TC  : n^2 =>> 42000 **/

//int month[]={31,28,31,30,31,30,31,31,30,31,30,31};  //Not Leap Year
//int dx[]={1,0,-1,0};int dy[]={0,1,0,-1}; //4 Direction
//int dx[]={1,1,0,-1,-1,-1,0,1};int dy[]={0,1,1,1,0,-1,-1,-1};//8 direction
//int dx[]={2,1,-1,-2,-2,-1,1,2};int dy[]={1,2,2,1,-1,-2,-2,-1};//Knight Direction
//int dx[]={2,1,-1,-2,-1,1};int dy[]={0,1,1,0,-1,-1}; //Hexagonal Direction

int main()
{
    //freopen("A.in","r",stdin);
    //freopen("A.out","w",stdout);
    //ios_base::sync_with_stdio(false);
    char ch;
    string s1,s2;
    map<char,int>mp;
    int i;
    bool f=0;

    cin>>ch;
    cin>>s1>>s2;

    FOR(i,6,9)
        mp[i+'0']=i;
    mp['T']=10;
    mp['J']=11;
    mp['Q']=12;
    mp['K']=13;
    mp['A']=14;
    //T", "J", "Q", "K" and "A"

    if(s1[1]==s2[1])
    {
        if(mp[s1[0]]>mp[s2[0]])
            f=1;
    }
    else
    {
        if(s1[1]==ch)
            f=1;
    }
    if(f)
        cout<<"YES"<<endl;
    else
        cout<<"NO"<<endl;

    return 0;
}
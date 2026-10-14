#include <bits/stdc++.h>
using namespace std;
#define For(i,a,b) for(int i=a;i<=b;i++)
#define FOr(i,a,b) for(int i=a;i<b;i++)
#define FOR(i,a,b) for(int i=a;i>=b;i--)
#define fi first
#define se second
#define pb push_back
#define mp make_pair
#define Heap priority_queue
template <typename T> inline void read(T &x){
    char c;bool nega=0;
    while((!isdigit(c=getchar()))&&c!='-');
    if(c=='-'){
        nega=1;c=getchar();
    }x=c-48;
    while(isdigit(c=getchar()))x=x*10+c-48;
    if(nega)x=-x;
}
template <typename T> inline void wrip(T x){
    if(x>=10)wrip(x/10);
    putchar(x%10+48);
}
template <typename T> inline void write(T x){
    if(x<0){
        putchar('-');x=-x;
    }wrip(x);
}
template <typename T> inline void writesp(T x){
    write(x);putchar(' ');
}
template <typename T> inline void writeln(T x){
    write(x);putchar('\n');
}
typedef long long ll;
typedef long double ld;
typedef pair<int,int> pii;
const ll base=1e9+7;
const ll oo=1e15;
int getbit(int i,int j){return (i>>(j-1))&1;}
#define fname "m"
const int N=2e5+5;
int n;
ld m,k,tg,res,ans,a[N],b[N];
char ch;
int main(){

    //freopen(fname".inp","r",stdin);
    //freopen(fname".out","w",stdout);
    cin>>n>>m;
    m=m*1e6;
    For(i,1,n){
        cin>>a[i];
    }
    For(i,1,n){
        cin>>b[i];
    }
    ld l=m,r=1e17;
    res=LLONG_MAX;
    ans=-1;
    For(t,1,60){
        ld mid=(l+r)/2;
        k=mid;
        For(i,1,n){
            tg=k/a[i];
            k=k-tg;
            if(i<n)tg=k/b[i+1];
            else tg=k/b[1];
            k=k-tg;
        }
        if(k>=m){
            if(k<res){
                res=k;
                ans=mid;
            }
            r=mid;
        }else l=mid;
    }
    if(ans==-1)cout<<-1;
    else{
        ans=ans-m;
        cout<<setprecision(6)<<fixed<<ans/1e6;
    }
}
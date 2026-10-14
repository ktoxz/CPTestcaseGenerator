#include <bits/stdc++.h>
 
#define set(p) memset(p,-1,sizeof(p))
#define clr(p) memset(p,0,sizeof(p))
#define ll long long int
#define llu unsigned long long int
#define si(n)                   scanf("%d",&n)
#define sf(n)                   scanf("%lf",&n)
#define ss(n)                                   scanf("%s",n)
#define rep(i,a,n) for(i=(a);i<(n);i++)
#define pii pair<int,int>
#define pb(x) push_back(x)
#define v(x) vector<x>

using namespace std;
 
ll gcd(ll a,ll b)
{
 ll r, i;
  while(b!=0){
    r = a % b;
    a = b;
    b = r;
  }
  return a;
}
 
 
ll power(ll x,ll y)
{
    ll temp,ty,my;
    ll mod;
    mod=1000000007;
    if( y == 0)
        return 1;
    temp = power(x, y/2);
    ty=(temp%mod)*(temp%mod);
    if (y%2 == 0)
    {
        return ty%mod;
    }
    else
    {
        my=(x%mod)*(ty%mod);
        return my%mod;
    }
}

ll mycbrt(ll n)
{

    ll start = 0;
    ll end = 1000000LL;

    ll ans = -1;
 
    while(start<=end)
    {
        ll mid = (start + end)/2;
        
        if ((mid*mid*mid) > n)
            end = mid-1;
        else if((mid*mid*mid) == n){
            ans = mid;
            break;
        }else{
            start = mid+1;
        }
    }

    if(n==1){
        ans = 1;
    }
    return ans;
}

void SieveOfEratosthenes(int n)
{
    bool prime[n+1];
    memset(prime, true, sizeof(prime));
    for (int p=2; p*p<=n; p++)
    {
        if (prime[p] == true)
        {
            for (int i=p*2; i<=n; i += p)
                prime[i] = false;
        }
    }
    for (int p=2; p<=n; p++)
       if (prime[p])
          cout << p << " ";
}
 
struct abhi
{
       ll val1;
       ll val2;
       ll po;
};
 
struct abhi brr[1000001];
 
bool cmp(struct abhi x,struct abhi y)
{
    if(x.val1==y.val1)
        return x.val2<y.val2;
    return x.val1<y.val1;
}

//for custom priority queue priority_queue< Abhi, vector<Abhi>, Compare)

// struct Compare
// {
//     bool operator()(const Abhi &p1, const Abhi  &p2){
//         return p1.first < p2.first;
//     }
// };
 
 
void fastscan(int &number)
{
    bool negative = false;
    register int c;
 
    number = 0;
    c = getchar();
    if (c=='-')
    {
        negative = true;
        c = getchar();
    }
    for (; (c>47 && c<58); c=getchar())
        number = number *10 + c - 48;
    if (negative)
        number *= -1;
}

// ll mod = 1000000007;
 
ll ar[1000010];
ll dp[1000010];
ll dpc[1000010];


vector<ll> A;
ll height[400005];

ll pre[35];

// vector<point> set1;
// vector<point> set2;

 // vector<ll> bc[2011];

// vector< pair<ll,ll> > bc;


int main(){

    // ios_base::sync_with_stdio(false);
    // cin.tie(NULL);

    ll n,m,i,d,j,k;
    cin>>n>>m;

    ll tot = 0;
    // rep(i,0,n){
    //     cin>>ar[i];
    //     tot = tot + ar[i];
    // }

    ll ko = (n*(n-1))/2;
    ll po ;

    if(n%2==1){
        ll hf = n/2;
        po = hf*(hf+1);
    }else{
        ll hf = n/2;
        po = hf*(hf+1);
        po = po - hf;
    }

    rep(i,0,m){
        ll a,d;
        cin>>a>>d;

        tot = tot + (a*n);
        if(d>=0){
            tot = tot + d*ko;
        }else{
            tot = tot + d*po;
        }
        
    }

    double ans = (1.0*tot)/n;

    printf("%0.6lf\n",ans);

    return 0;
}
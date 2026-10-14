#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define loop(i,n) for(ll i=1; i<=n; i++)
#define loop2(i,n) for(ll i=2; i<=n; i++)
#define loopo(i,n) for(ll i=0; i<=n; i++)
#define no {cout<<"NO"; return 0;}
#define yes {cout<<"YES"; return 0;}
ll intpow(ll a, ll n)
{
    ll s=1,i;
    if(n==0)return 1;
    else
    if(n%2==0)return ((intpow(a,n/2))*(intpow(a,n/2)));
    else
    return ((intpow(a,n/2))*(intpow(a,n/2))*a);
}
ll fact(ll n)
{
    ll f=1;
    loop2(i,n)f*=i;
    return f;
}
ll comb(ll n, ll k)
{
    return fact(n)/fact(k)/fact(n-k);
}
bool f(ll a, ll b)
{
    return a>b;
}
int main()
{
ios::sync_with_stdio (false);
cin.tie(0);
cout.tie(0);
ll i,j,k,n,d,q=0;
long double z=0.0, m;
cin>>n>>m;
ll a[n+7], b[n+7];
loop(i,n){cin>>a[i];if(a[i]==1)q=1;}
loop(i,n){cin>>b[i];if(b[i]==1)q=1;}
if(q==1){cout<<-1; return 0;}
long double t[2*n+100],s=0.0;
t[1]=(m+0.0)/(b[1]-1);
z+=t[1];
t[2]=(m+t[1])/(a[n]-1);
z+=t[2];
i=2;
for(j=n; j>=2; j--)
{
    i++;
    t[i]=(m+z)/(b[j]-1);
    z+=t[i];
    i++;
    t[i]=(m+z)/(a[j-1]-1);
    z+=t[i];
}
cout<<fixed<<setprecision(10)<<z;
return 0;
}
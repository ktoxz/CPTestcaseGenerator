#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
int main()
{
    ios::sync_with_stdio(false);
    ll n,m;
    cin>>n>>m;
    ll i;
    ll a[n];
    memset(a,0,sizeof(a));
    ll j=0;
    ll xx,dd,ddd;
    xx=dd=ddd=0;
    for(j=0;j<m;j++)
    {
        int x,d;
        cin>>x>>d;
        xx+=x;
        if(d<0)
            ddd+=d;
        else
            dd+=d;
    }
    ll mid=n/2;
    for(i=0;i<n;i++)
        a[i]+=xx;
    for(i=0;i<n;i++)
        a[i]+=dd*(n-1-i);
    for(i=0;i<n;i++)
        a[i]+=ddd*(fabs(mid-i));
    double avg=0;
    for(i=0;i<n;i++)
        avg+=a[i];
    avg/=n;
    cout<<setprecision(9)<<fixed<<avg<<endl;
    return 0;
}
#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cmath>
#include<vector>
#include<queue>
#include<set>
#include<map>
#include<stack>
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef pair<int,int> pii;
typedef pair<ll,ll> pII;
#define pb push_back
#define mp make_pair
#define clr(x,y) memset(x,y,sizeof(x))
const int inf=0x3f3f3f3f;
const ll mod=1e9+7;
const int maxn=1e6+5;
//ll fmod(ll x,ll y){ll res=1;while(y){if(y&1)res=res*x%mod;y>>=1;x=x*x%mod;}return res;}
double v[maxn];
int main()
{
   ll n,m;
   while(cin>>n>>m)
   {
        ll da=0;
       //cout<<nn<<"  "<<n<<endl;
        for(int i=0;i<m;i++)
        {
            ll x,y;cin>>x>>y;
            da+=x*n;
            //cout<<da<<endl;
            if(y>=0)
            {
                da+=y*(n-1LL)*n/2;
            }
            else
            {
                if(n%2)
                {
                    da+=y*(n*n-1LL)/4;
                }
                else
                {
                    int now=n/2;
                    da+=y*2LL*now*(now-1)/2+(n-now)*y;
                }
            }
        }
        //cout<<da/n;
        double ans=(double)da/(1.0*n);
        //printf("%.8lf\n",ans);
        cout<<fixed<<setprecision(10)<<ans<<endl;
   }
}
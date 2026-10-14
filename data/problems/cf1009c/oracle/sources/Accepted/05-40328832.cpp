#include<bits/stdc++.h>
using namespace std;
#define fre(i,t,n)  for(int i =(t);i<=(n);++i)
#define fer(i,n,t)  for(int i =(n);i>=(t);--i)
#define mp make_pair
#define pb push_back
typedef long long ll;
void smain();
int main(){
    //ios::sync_with_stdio(false);
    smain();
    return 0;
}
ll sumx,dm,dp;
void smain(){
    int n,m;
    scanf("%d%d",&n,&m);
    for(int i=0,x,d;i<m;++i)
    {
        scanf("%d%d",&x,&d);
        sumx=sumx+x;
        if(d>0) dp=dp+d;
        else dm=dm+d;
    }
    ll Big = 0,Small=0;
    for(int i=1;i<=n;++i)   Big=Big+abs(i-1);
    int mid = (1+n)>>1;
    for(int i=1;i<=n;++i)   Small=Small+abs(i-mid);
    ll sum=sumx*n+Big*dp+Small*dm;
    long double ans=(long double)sum/n;
    //cout<<setprecision(10)<<ans<<endl;
    printf("%.10f\n",(double)ans);
}
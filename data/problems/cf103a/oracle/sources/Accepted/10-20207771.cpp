#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef unsigned long long ull;
const double pi=3.141592653589;
int main()
{
    /*freopen("input.txt","r",stdin);
    freopen("output.txt","w",stdout);*/
    ios_base::sync_with_stdio(0);cin.tie(NULL);cout.tie(NULL);
    ll n,i,a,t=0;
    cin>>n;
    for(i=1;i<=n;i++)
    {
        cin>>a;
        t+=1+a*i-i;
    }
    cout<<t;
    return 0;
}
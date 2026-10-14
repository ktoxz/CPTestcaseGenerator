#include<bits/stdc++.h>
#include<set>
#include<cstdio>
#include<iomanip>
#include<iostream>
#include<string>
#include<cstring>
#include<algorithm>
#define pb push_back
#define ll long long
#define fi first
#define se second
#define PI 3.14159265
#define ls l,m,rt<<1
#define rs m+1,r,rt<<1|1
#define eps 1e-7
#define pii pair<int,int>
typedef unsigned long long ull;
const int mod=1e3+5;
const ll inf=0x3f3f3f3f3f3f3f;
const int maxn=2e5+5;
using namespace std;
ll n,k;
int a[maxn];
vector<int>qq;
map<int,int>mp;
void init()
{
    ll tmp=1;
    while(tmp<=2e9+10)
    {
        qq.pb(tmp);tmp*=2;
    }
}
bool judge(int x)
{
       for(int i=0;i<qq.size();i++)
       {
            if(qq[i]-x==x&&mp[x]>=2)
            {
                //if(x==2)cout<<mp[qq[i]-x]<<endl;
                return true;
            }
            else if(qq[i]-x!=x&&mp.count(qq[i]-x)>0)
            {
                return true;
            }
       }
     return false;
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    init();
    cin>>n;
    for(int i=0;i<n;i++)
    {
        cin>>a[i];
        mp[a[i]]++;
    }
    int ans=0;
    for(int i=0;i<n;i++)
    {
        if(!judge(a[i]))
        { // cout<<a[i]<<endl;
            ans++;
        }
    }
    cout<<ans<<endl;
    return 0;
}
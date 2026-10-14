#include<bits/stdc++.h>
using namespace std;
#define pii pair<int,int>
#define mp make_pair
#define x first
#define y second
#define pb push_back
#define ll long long
string s;
int dp[200001][3][2];
int f(int i,int rem,int start)
{
    if(i>=s.size())
    {
        if(start)
        {
            return rem == 0;
        }
        return 0;
    }
    int &ret = dp[i][rem][start];
    if(ret!=-1)
        return ret;
    int r=0,t=0,d,a,b,l;
    if(start)
    {

        d = s[i]-'0';
        if(rem==0)
        {
            if(d==0)
            {
                r=2+f(i+1,0,0);
            }
            else
            {
                r=1+f(i+1,d%3,1);
            }
        }
        else
        {
            a = f(i+1,(d+rem)%3,1);
            if(d==0)
            {
                b = 1+f(i+1,0,0);
            }
            else
            {
                b = f(i+1,d%3,1);
            }
            r = max(a,b);
        }


    }
    else
    {
        d=s[i]-'0';
        if(d!=0)
            r = f(i+1,d%3,1);
        else
        {
            r = 1+f(i+1,0,0);
        }
    }
    return ret=r;
}


int main()
{
    cin>>s;
    memset(dp,-1,sizeof(dp));
    cout<<f(0,0,0);



    return 0;
}
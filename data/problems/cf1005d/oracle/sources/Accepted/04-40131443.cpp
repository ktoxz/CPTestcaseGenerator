#include <bits/stdc++.h>
using namespace std;
#define ll long long
ll min(ll a,ll b)
{
    if(a<b)return a;
    return b;
}
 int s[300000];
int main() {
    std::ios::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);
    string a;
    cin>>a;
    int ans=0;
    int n=a.size();
    for(int i=0;i<a.size();i++)
   		s[i]=((a[i]-'0')%3);
    int r[3]={0};
    for(int i=0;i<n;i++)
    {
    	if(s[i]==0)
    	{
    		ans++;
    		r[1]=0;
    		r[2]=0;
    	}
    	else if(s[i]==1)
    	{
    		if(r[2]==1)
    		{
    			ans++;
    			r[1]=0;
    			r[2]=0;
    		}
    		else
    		{
    			if(r[1]==1)
    				r[2]=1;
    			r[1]=1;
    		}
    	}
    	else
    	{
    		if(r[1]==1)
    		{
    			ans++;
    			r[1]=0;
    			r[2]=0;
    		}
    		else
    		{
    			if(r[2]==1)
    				r[1]=1;
    			r[2]=1;
    		}	
    	}
    }
    cout<<ans<<endl;
	return 0;
}
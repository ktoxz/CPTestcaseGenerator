/* dsingh_24 */

#include<bits/stdc++.h>
#define ll          long long
#define pb          push_back
#define	endl		'\n'
#define pii         pair<ll ,ll>
#define vll          vector<ll>
#define all(a)      (a).begin(),(a).end()
#define F           first
#define S           second
#define sz(x)       (ll int)x.size()
#define rep(i,a,b)	for(ll int i=a;i<b;i++)
#define hell 		1000000007
#define lbnd        lower_bound
#define ubnd        upper_bound
#define bs          binary_search
#define mp          make_pair
#define ios         ios_base::sync_with_stdio(false);cin.tie(0);cout.tie(0);
using namespace std;

#define N  100005
int main()
{
	ios
	ll n,i,j;
	cin>>n;
	ll a[n+1],ans=0;
	map<ll,ll>m;
	for(i=0;i<n;i++){
		cin>>a[i];
		m[a[i]]++;
	}
	for(i=0;i<n;i++){
		ll f=0;
		for(j=0;j<=34;j++){
			ll dif=(1LL<<j)-a[i];
			if(dif>0){
				if(dif!=a[i]&&m[dif])f=1;
				else if(dif==a[i]&&m[dif]>1)f=1;
			}
		}
		if(f==0){
			ans++;
			m[a[i]]--;
		}
	}
	cout<<ans;
	return 0;
}
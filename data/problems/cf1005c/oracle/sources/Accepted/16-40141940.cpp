#include<bits/stdc++.h>
#include <sstream>
#include<math.h>
#define ll long long int
#define mp make_pair
#define pb push_back
#define mod 1000000007
#define all(c) c.begin(),c.end()
#define fl(i,n) for(i=0;i<n;i++)
#define fl1(i,a,b) for(i=a;i<=b;i++)
#define ff first.first
#define fs first.second
#define sf second.first
#define ss second.second
#define matrix(v,n)	std::vector<std::vector<int> > v(n,std::vector<int> (n));
#define trace1(x)                cout << #x << ": " << x << endl;
#define trace2(x, y)             cout << #x << ": " << x << " | " << #y << ": " << y << endl;
#define trace3(x, y, z)          cout << #x << ": " << x << " | " << #y << ": " << y << " | " << #z << ": " << z << endl;
#define trace4(a, b, c, d)       cout << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << endl;
#define trace5(a, b, c, d, e)    cout << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << endl;
#define trace6(a, b, c, d, e, f) cout << #a << ": " << a << " | " << #b << ": " << b << " | " << #c << ": " << c << " | " << #d << ": " << d << " | " << #e << ": " << e << " | " << #f << ": " << f << endl;
using namespace std;

bool isPowerofTwo (ll x)
{
  /* First x in the below expression is for the case when x is 0 */
  return x && (!(x&(x-1)));
}
vector<ll> twopow;
void gen(){
	ll i=1;
	while(i<10e9){
		twopow.pb(i);
		i=i*2;
	}
}

int main(){
	gen();
//	int t;
//	cin>>t;
//	while(t--){
	ll n,m,i,j,k;
	cin>>n;
	map<ll,ll> vcount;
	set<ll> s;
	vector<ll> v(n),veven,vodd;
	fl(i,n){
		cin>>v[i];
		vcount[v[i]]++;
		s.insert(v[i]);
//		if(v[i]%2==0){
//			veven.pb(v[i]);
//		}
//		else{
//			vodd.pb(v[i]);
//		}
	}

	ll count=0;
	ll ln=twopow.size();

	for(i=0;i<n;i++){
		for(j=0;j<ln;j++){
//			cout<<twopow[j]<<endl;
			if(twopow[j]>v[i]){
//				cout<<"EWFwe"<<endl;
				if(s.find(twopow[j]-v[i])!=s.end()){
					if((twopow[j]-v[i])==v[i]){
						std::map<ll,ll>::iterator p;
						p=vcount.find(v[i]);
						if(p!=vcount.end() && p->second>1){
							break;
						}
						else{
						}
					}
					else{
						break;
					}
					
				}
				
			}
			if(j==ln-1){
				count++;
			}
		}
	}
	cout<<count<<endl;
//	}
	
	
	
}
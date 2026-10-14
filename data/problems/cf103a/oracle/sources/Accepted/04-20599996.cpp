#include <bits/stdc++.h>

 

using namespace std;

 

#define fi first

#define se second

#define mp make_pair

#define pb push_back

#define pf push_front;

#define fbo find_by_order

#define ook order_of_key

#define lb lower_bound

#define ub upper_bound

#define rep(n) for(int i=0;i<n;i++)

#define rep1(n) for(int j=0;j<n;j++)

#define fori(a,b) for(int i=a;i<=b;i++)

 

typedef long long ll;

typedef pair<ll,ll> ii;

typedef vector<int> vi;

typedef long double ld;

typedef map<ll,ll> h;

typedef set<ll,ll> si;

typedef set<int>::iterator sit;

typedef map<int,int>::iterator mii;

typedef vector<int>::iterator vit;

typedef vector<ii> vii;

typedef set<ii> sii;

typedef multiset<ii> msii;

const int INF = 1e9 + 7;

const int MOD = 1e9 + 7;

const int N = 1e6 + 2 ;

int main()

{

	ll sum=0;

	ll n;

	cin>>n;

	ll a[n+2];

	fori(1,n)

	cin>>a[i];

	fori(1,n)

	{

		sum+=(ll)(i*(a[i]-1));

		sum++;

	}

	cout<<sum;

}
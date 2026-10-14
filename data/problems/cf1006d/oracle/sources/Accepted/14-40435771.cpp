#include <bits/stdc++.h>
#include <sstream>
using namespace std;
#define ll long long int
#define ld long double
#define key pair<ld,ld>
#define vii vector<pair<int,int> >
#define vi vector<int>
#define vll vector<ll>
#define vb vector<bool>
#define vvi vector<vector<int> >
#define vs vector<string>
#define all(v) v.begin(),v.end()
#define rep(i,n) for(int i=0;i<n;++i)
#define pb push_back
#define mp make_pair
#define f first
#define s second
#define nu 100001
#define mod 1000000007
#define mul(x,y) ((ll)(x)*(y))%mod
#define tr(c,i) for(auto i = (c).begin(); i != (c).end(); i++)
#define fastio  ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL);
#define INF 0x3f3f3f3f
const double PI=3.141592653589793238462643383279502884197169399375105820974944;     
     
     
int main()
{
	fastio;
	int n;
	cin>>n;
	string a,b;
	cin>>a>>b;
	int p=0;
	if(n%2==1)
	{
		if(a[(n-1)/2]!=b[(n-1)/2])
		{
			p++;
		}
	}
	for(int i=0,j=n-1;i<j;++i,--j)
	{
		set<char> s;
		s.insert(b[i]);
		s.insert(b[j]);
		int sz=s.size();
		if(sz==2)
		{
			set<char> s1;
			s1.insert(a[i]);
			s1.insert(a[j]);
			if(s1.size()==2){
			if(a[i]!=b[i]&&a[i]!=b[j])
			{
				p++;
			}
			if(a[j]!=b[i]&&a[j]!=b[j])
			{
				p++;
			}}
			if(s1.size()==1)
			{
				if(a[i]!=b[i]&&a[i]!=b[j])
				{
					p++;
				}
				p++;
			}
		}
		if(sz==1)
		{
			set<char> s1;
			s1.insert(a[i]);
			s1.insert(a[j]);
			p+=s1.size()-1;
		}
	}
	cout<<p;
	return 0;
}
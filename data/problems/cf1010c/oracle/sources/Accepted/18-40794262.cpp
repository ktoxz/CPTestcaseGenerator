#include <algorithm>
#include <bitset>
#include <complex>
#include <deque>
#include <exception>
#include <fstream>
#include <functional>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <limits>
#include <list>
#include <locale>
#include <map>
#include <memory>
#include <new>
#include <numeric>
#include <ostream>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <streambuf>
#include <string>
#include <typeinfo>
#include <utility>
#include <valarray>
#include <vector>
#if __cplusplus >= 201103L
#include <array>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <forward_list>
#include <future>
#include <initializer_list>
#include <mutex>
#include <random>
#include <ratio>
#include <regex>
#include <scoped_allocator>
#include <system_error>
#include <thread>
#include <tuple>
#include <typeindex>
#include <type_traits>
#include <unordered_map>
#include <unordered_set>
#endif

long long max(long long x, long long y){return (x > y ? x : y);}
long long min(long long x, long long y){return (x < y ? x : y);}
int gcd(int a, int b) { return b ? gcd(b, a%b) : a; }

#define ll long long
#define pb push_back
#define ld long double
#define mp make_pair
#define F first
#define S second
#define pii pair<ll,ll> 

using namespace :: std;

const ll maxn=1e5+500;
const ll inf=1e9+800;
const ll mod=1e9+7;

bool a[maxn];
int main(){
	ios_base::sync_with_stdio(0);cin.tie(0);cout.tie(0);	
	ll n,k;
	cin>>n>>k;
	for(ll i=0;i<n;i++){
		ll v;
		cin>>v;
		a[v%k]=1;
	}
	a[0]=1;
	ll res=k;
	for(ll i=1;i<k;i++){
		if(a[i]){
			res=gcd(res,i);
		}
	}
	for(ll i=res;i<k;i+=res){
		a[i]=1;
	}
	ll ans=0;
	for(ll i=0;i<k;i++){
		ans+=a[i];
	}
	cout<<ans<<endl;
	for(ll i=0;i<k;i++){
		if(a[i])cout<<i<<' ';
	}
}
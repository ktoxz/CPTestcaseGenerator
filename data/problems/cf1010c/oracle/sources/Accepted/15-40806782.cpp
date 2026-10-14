#include <queue>
#include <iostream>       
#include <string>
#include <vector>
#include <fstream>        
#include <functional> 
#include <algorithm>  
#include <cstdlib>    
#include <cstring>    
#include <map>        
#include <iomanip>    
#include <limits> 
#include <unordered_map>
#include <set>
#include <cmath>
#include <numeric> //accumulate
#include <stack>
#include <bitset>
#include <cstdio>

//#include <unordered_set>//unordered_set

#define rep(i,a) for (int i = 0; i < (a); ++i)
#define rep2(i,a,b) for (int i = (a); i < (b); ++i)
#define pb push_back
#define mp make_pair
#define all(x) (x).begin(),(x).end()
#define PI 3.14159265359

using namespace std;
typedef long long ll;
typedef double lf;
typedef pair<int, int> pii;
typedef pair<int, pair<int, int>> piii;
typedef pair<ll, ll> pll;
typedef pair<ll, int> pli;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef vector<double> vd;
typedef vector<string> vs;
typedef vector<pair<int, int>> vpii;
typedef vector<pair<int, pair<int, int>>> vpiii;
typedef vector<vector<int>> vvi;
typedef const vector<int> cvi;
typedef vector<bool> vb;

const ll INF = 1ull << 60;
//const int INF = 1987654321;
//const int INF = 2147483647;
//const int INF = 1587654321;
//const int INF = 987654321;
//const double eps = 0.00000000001;
//unordered_map<ll, deque<int>> my;
ll gcd(ll a, ll b) {
	if (b == 0) return a;
	return gcd(b, a%b);
}
int main() {
	//freopen("input.txt", "r", stdin);
	//freopen("output.txt", "w", stdout);
	ios::sync_with_stdio(false); cin.tie(0);
	ll n, k; cin >> n >> k;
	ll cur = k;
	vll arr(n);
	rep(i, n) cin >> arr[i];
	rep(i, n) {
		ll num = arr[i];
		num %= k;
		ll tmp = gcd(k, num);
		ll tmp2 = gcd(tmp, cur);
		if (tmp2 == 1) {
			cur = 1;
			break;
		}
		cur = tmp2;
	}
	cout << k / cur << '\n';
	for (int i = 0; i < k; i += cur)
		cout << i << " ";
	return 0;
}
#include <iostream>
#include <iomanip>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <vector>
#include <set>
#include <map>
#include <queue>
#include <deque>
#include <stack>
#include <ctime>
#include <algorithm>

#define int long long
#define ull unsigned long long
#define f first
#define ppb pop_back
#define s second
#define mp make_pair
#define pb push_back
#define ld long double
#define pii pair < int, int >
#define lowb lower_bound

using namespace std;

const int maxn = 3e5 + 100;
const int inf = 2e9;
const int mod = 1e9 + 7;

int n, a[maxn], ans, st[maxn], mx = -inf;
map < int, int > cnt;

main() {
	cin >> n;
	for(int i = 1; i <= n; i++) {
		cin >> a[i];
		cnt[a[i]]++;
		mx = max(mx, a[i]);
	}
	sort(a + 1, a + 1 + n);
	int p = 1;
	for(int i = 1; i <= n; i++) {
		while(p < a[i])
			p *= 2;
		st[i] = p;
	}

	for(int i = 1; i <= n; i++) {
		int x = st[i];
		while(((x - a[i] != a[i] && cnt[x - a[i]] == 0) || (x - a[i] == a[i] && cnt[a[i]] < 2)) && x - a[i] <= mx) 
			x *= 2;

		if(x - a[i] > mx) 
			ans++;
	}
	cout << ans;
	return 0;
}
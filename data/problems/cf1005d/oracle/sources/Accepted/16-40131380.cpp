#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <vector>
#include <deque>
#include <cmath>
#include <string>
#include <queue>
#include <map>
using namespace std;

#ifdef _MSC_VER
#define INLINE __forceinline
#else
#define INLINE __attribute__((always_inline))
#endif
#define FOR(var,start,end) for(int var=(start);var<(end);var++)
#define ROF(var,start,end) for(int var=(start);var>(end);var--)
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define zmem(x) memset(x, 0, sizeof(x))
#define REP(x) FOR(i, 0, (x))
#define ULL_MAX 0xffffffffffffffffull
#define LL_MAX 0x7fffffffffffffffll
typedef long long ll;
typedef unsigned long long ull;
typedef pair<int,int> pr;
#define mp make_pair

INLINE void ios_optimize(void) {
	ios::sync_with_stdio(false);
	cin.tie(0);
}

#define MAXN 200005
string s;

/* main */
int main(void) {
	ios_optimize();

	cin >> s;
	int ans = 0;
	int status = 0;
	bool flag = false;
	for(auto &c : s) {
		int dig = c - '0';
		if(dig % 3 == 0) {
			ans++;
			status = 0;
			flag = false;
		} else if(dig % 3 == 1) {
			if(status == 2 || flag == true) {
				ans++;
				status = 0;
				flag = false;
			} else if(status == 0) {
				status = 1;
			} else if(status == 1) {
				flag = true;
			}
		} else if(dig % 3 == 2) {
			if(status == 1 || flag == true) {
				ans++;
				status = 0;
				flag = false;
			} else if(status == 0) {
				status = 2;
			} else if(status == 2) {
				flag = true;
			}
		}
	}
	cout << ans << endl;
	return 0;
}
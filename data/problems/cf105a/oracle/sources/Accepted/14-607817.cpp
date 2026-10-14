#include <iostream>
#include <sstream>
#include <iomanip>

#include <iterator>

#include <algorithm>
#include <numeric>
#include <utility>
#include <limits>

#include <string>

#include <vector>
#include <deque>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <stack>

#include <tuple>
#include <initializer_list>

#include <cmath>

typedef unsigned long long ULL;
typedef long long LL;
typedef unsigned long UL;
typedef unsigned int UI;
typedef unsigned short US;
typedef unsigned char UC;

#define RNG(v) (v).begin(), (v).end()
#define REP(v, e) for(UI v = 0U; v < e; ++v)
#define REP_(v, s, e) for(auto v = s; v < e; ++v)
#define REPV(type, v, e) for(type v = 0; v < e; ++v)

using namespace std;

int main(void)
{
	ios::sync_with_stdio(false);

	int n,m; string s; cin >> n >> m >> s;
	int k = (s[2]-'0')*10+s[3]-'0';

	map<string, int> ns;
	REP(i, n) {
		string s; int val; cin  >> s >> val; int val_ = k * val;
		if(val_ >= 10000) ns[s] = val_ / 100;
	}
	REP(i, m) {
		string s; cin >> s;
		if(ns.count(s) == 0) ns[s] = 0;
	}
	cout << ns.size() << endl;
	for(auto &v : ns) {
		cout << v.first << ' ' << v.second << endl;
	}

	return 0;
}
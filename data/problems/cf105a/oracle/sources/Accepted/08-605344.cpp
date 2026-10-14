#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <cmath>
#include <ctime>

#include <string>
#include <sstream>
#include <algorithm>
#include <iostream>
#include <vector>
#include <list>
#include <set>
#include <map>

using namespace std;

#define Eo(x) { cerr << #x << " = " << (x) << endl; }
#define Sz(x) (int((x).size()))

template<typename A, typename B> ostream& operator<<(ostream& os, const pair<A, B>& p) { return os << '(' << p.first << ", " << p.second << ')'; }
#define foreach(i, x) for(__typeof((x).begin()) i = (x).begin(); i != (x).end(); i ++)
template<typename C> inline void operator<<(vector<C>& v, const C& c) { v.push_back(c); }

typedef double real;
typedef long long int64;
typedef unsigned long long uint64;
typedef pair<int, int> pip;

const int inf = 0x3f3f3f3f;
const int64 inf64 = 0x3f3f3f3f3f3f3f3fLL;
const real eps = 1e-5;

typedef map<string, int> abi;
abi as;

int main() {
	int n, m; cin >> n >> m;
	real k; cin >> k;
	for(int i=0; i<n; i++) {
		string name; cin >> name;
		int val; cin >> val;
		int t =  int(val*k+eps);
		if(t >= 100) as[name] = t;
	}
	for(int i=0; i<m; i++) {
		string name; cin >> name;
		if(!as.count(name)) as[name] = 0;
	}

	cout << Sz(as) << endl;
	for(auto i : as) {
		cout << i.first << ' ' << i.second << endl;
	}
	
	return 0;
}
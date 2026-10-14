#include <iostream>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <vector>
#include <algorithm>
using namespace std;

typedef pair<int, int> PII;
#define FOR(a, b, c) for(int a = (b); a <= (c); a++)
#define FORD(a, b, c) for(int a = (b); a >= (c); a--)
#define REP(a, b) FOR(a, 0, b-1)
#define all(a) (a).begin(), (a).end()
#define si size()
#define pb push_back
#define mp make_pair
#define st first
#define nd second

int n, m, a, x, y, resa, resb;
vector<int> p, v;
string s;
map<string, int> t;

int main() {
	cin >> n >> m;
	REP(i, n) {
		cin >> a;
		p.pb(a);
	}
	sort(all(p));
	REP(i, m) {
		cin >> s;
		t[s]++;
	}
	for(map<string, int>::iterator i = t.begin(); i != t.end(); i++) {
		if(i->nd)
			m-=(i->nd)-1;
		v.pb(i->nd);
	}
	sort(all(v));
	reverse(all(v));
	while(x<m) {
		resa+=p[x]*v[x];
		x++;
	}
	reverse(all(p));
	x = 0;
	while(x<m) {
		resb+=p[x]*v[x];
		x++;
	}
	cout << resa << ' ' << resb << "\n";
	return 0;
}
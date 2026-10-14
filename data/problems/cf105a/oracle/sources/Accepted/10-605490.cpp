#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <set>
#include <map>
#include <list>
#include <queue>
#include <deque>
#include <stack>
#include <string>
#include <cstring>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <ctime>
#include <cassert>
#include <functional>
#include <iterator>
#include <utility>

typedef long double LD;
typedef long long LL;
using namespace std;

int main()
{

#ifdef DEBUG
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#endif

	int n, m, k;
	cin >> n >> m;
	char c; cin >> c >> c >> k;
	
	map<string, int> q;
	for (int i = 0; i < n; ++i)
	{
		string s; int e;

		cin >> s >> e;
		int ne = e * k / 100;
		if (ne < 100) continue;
		q[s] = ne;
	}

	for (int i = 0; i < m; ++i)
	{
		string s; cin >> s;
		if (q.find(s) == q.end())
			q[s] = 0;
	}

	cout << q.size() << '\n';
	for (map<string, int>::const_iterator it = q.begin(); it != q.end(); ++it)
		cout << it->first << ' ' << it->second << '\n';
	return 0;
}
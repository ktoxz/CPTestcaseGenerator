#define _USE_MATH_DEFINES
#include <iostream>
#include <complex>
#include <algorithm>
#include <vector>
#include <stack>
#include <string>
#include <queue>
#include <cmath>
#include <math.h>
#include <numeric>
#include <list>
#include <sstream>
#include <fstream>
#include <iomanip>
#include <climits>
#include <set>
#include <memory.h>
#include <memory>
#include <cstdio>
#include <cstdlib>
#include <cctype>
#include <cassert>
#include <map>
#include <cassert>
#include <time.h>
#include <ctime>

using namespace std;

typedef complex<double> xy_t;
typedef pair<xy_t, xy_t> line;
typedef vector<xy_t> polygon;
typedef long long ll;
typedef pair<int, int> P;
typedef pair<int , P> PP;
typedef pair<int, PP> PPP;
typedef pair<string, int> Ps;
typedef vector<int> vec;
typedef vector<vec> mat;
const int INF = 1 << 29;
const double EPS = 1e-10;
const double PI = 3.1415926535897932384626433832795;
const int CLK = CLOCKS_PER_SEC;

#define rep(i, n) for(int i = 0; i < n; i++)

int check_type(string s){
	int n = s.size();
	if(n >= 4 && string(s.begin() + n - 4, s.end()) == "lios") return 0;
	if(n >= 3 && string(s.begin() + n - 3, s.end()) == "etr") return 1;
	if(n >= 6 && string(s.begin() + n - 6, s.end()) == "initis") return 2;
	if(n >= 5 && string(s.begin() + n - 5, s.end()) == "liala") return 0;
	if(n >= 4 && string(s.begin() + n - 4, s.end()) == "etra") return 1;
	if(n >= 6 && string(s.begin() + n - 6, s.end()) == "inites") return 2;
	return -1;
}

int check_jen(string s){
	int n = s.size();
//	cout << string(s.begin() + n - 5, s.end()) << endl;
	if(n >= 4 && string(s.begin() + n - 4, s.end()) == "lios") return 1;
	if(n >= 3 && string(s.begin() + n - 3, s.end()) == "etr") return 1;
	if(n >= 6 && string(s.begin() + n - 6, s.end()) == "initis") return 1;
	if(n >= 5 && string(s.begin() + n - 5, s.end()) == "liala") return 2;
	if(n >= 4 && string(s.begin() + n - 4, s.end()) == "etra") return 2;
	if(n >= 6 && string(s.begin() + n - 6, s.end()) == "inites") return 2;
	return 0;
}

vector<string> vs;
int main(){
	string s;
	while(cin >> s){
		vs.push_back(s);
	}
	int n = vs.size();
	int phase = 0;
	int jen = check_jen(vs[0]);
	if(jen == 0) {
	//	cout << "**" << endl;
		cout << "NO" << endl;
		return 0;
	}
	if(n == 1){
		cout << "YES" << endl;
		return 0;
	}
	rep(i, n){
		int jender = check_jen(vs[i]);
		if(jender != jen){
			cout << "NO" << endl;
			return 0;
		}
		int t = check_type(vs[i]);
		if(phase == 0){
			if(t == 0) continue;
			else if(t == 1) phase++;
			else {
				cout << "NO" << endl;
				return 0;
			}
		}else if(phase == 1){
			if(t == 2) phase++;
			else{
				cout << "NO" << endl;
				return 0;
			}
		}else{
			if(t != 2){
				cout << "NO" << endl;
				return 0;
			}
		}
	}
	if(phase == 2 || phase == 1) cout << "YES" << endl;
	else cout << "NO" << endl;
	return 0;
}



















/*
int memo[1 << 12][10][10];
int n, m;
int dx[] = {-1, 0, 1, 0};
int dy[] = {0, -1, 0, 1};

int calc(int mask, int x, int y){
	if(y >= n) return 0;
	if(memo[mask][x][y] != -1) return memo[mask][x][y];
	int res = INF;
	int cost = 1;
	int mask2 = mask - (mask & (1 << (x + m))) + ((mask & (1 << x)) << m) - (mask & (1 << x));
	int nextx = (x + 1) % m;
	int nexty = y + (x + 1) / m;
	//cout << "mask2" << "  "<< mask2 << endl;
	if(mask & (1 << x)) cost = 0;
	res = min(res, cost + calc(mask2 | 1 << (x + m), nextx, nexty));
	for(int i = 0; i < 4; i++){
		cout << res << endl;
		int x2 = x + dx[i];
		int y2 = y + dy[i];
		if(0 > x2 || x2 >= m || 0 > y2 || y2 >= n) continue;
		
		if(i != 3){
			if(i < 2){
				if(mask & (1 << (x2 + m))) cost = 0;
				else cost = 1;
				res = min(res, cost + calc(mask2 | (1 << (x2 + m)), nextx, nexty));
			}else{
				if(mask & (1 << x2)) cost = 0;
				else cost = 1;
				res = min(res, cost + calc(mask2 | (1 << x2), nextx, nexty));
			}
		}else{
			cost = 1;
			res = min(res, cost + calc(mask2 | (1 << x2), nextx, nexty));
		}
	}
	cout << mask << " " << x << " " << y << "result=" << res << endl;
	return memo[mask][x][y] = res;
}

int main(){
	while(cin >> n >> m){
		if(n < m) swap(n, m);
		memset(memo, -1, sizeof(memo));
		cout << n * m - calc(0, 0, 0) << endl;
	}
	return 0;
}
*/
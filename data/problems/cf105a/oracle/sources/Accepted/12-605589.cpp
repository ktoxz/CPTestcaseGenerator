#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <cmath>
#include <climits>
#include <vector>
#include <string>
#include <algorithm>
#include <sstream>
#include <map>
#include <set>
#include <queue>
#include <numeric>

using namespace std;

#define FOR(i,a,b) for (int (i) = (a); (i) < (b); (i)++)
#define _FORIT(it, b, e) for (__typeof(b) it = (b); it != (e); it++)
#define FORIT(x...) _FORIT(x)
#define ALL(M) (M).begin(), (M).end()
#define SI(V) (int)(V.size())
#define UNIQUE(v) sort(ALL(v)),(v).resize(unique(ALL(v))-(v).begin())

typedef long long ll;

const int INF = 0x3F3F3F3F;
const ll LINF = 0x3F3F3F3F3F3F3F3FLL;
const double EPS = 1E-10;

inline int cmp(double x, double y = 0, double tol = EPS) {
    return (x <= y + tol) ? (x + tol < y) ? -1 : 0 : 1;
}


int main() {

//	freopen("A.in","r",stdin);

    int N, M, K;
    map<string,int> RET;
    scanf("%d %d %*d.%d ", &N, &M, &K);
    FOR(i,0,N) {
        string s;
        int l;
        cin >> s >> l;
        l = (l * K) / 100;
        if (l < 100) continue;
        RET[s] = l;
    }
    FOR(i,0,M) {
        string s;
        cin >> s;
        if (RET.count(s)) continue;
        RET[s] = 0;
    }
    printf("%d\n", RET.size());
    FORIT(it, ALL(RET)) {
        printf("%s %d\n", it->first.c_str(), it->second);
    }

    return 0;
}
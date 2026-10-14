#include <iostream>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cstring>
#include <string>
#include <algorithm>
#include <vector>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <sstream>
#include <numeric>
#include <bitset>

#define re return
#define fi first
#define se second
#define y1 y269
#define y0 y91236
#define sqr(x) ((x) * (x))
#define rep(i, n) for (int i = 0; i < (n); i++)
#define rrep(i, n) for (int i = (n) - 1; i >= 0; i--)
#define fill(a,b) memset(a, b, sizeof(a))
#define all(a) a.begin(), a.end()
#define sz(a) ((int)(a).size())
#define sqrt(x) sqrt(abs(x))
#define mp make_pair
#define pb push_back

using namespace std;

typedef vector <int> vi;
typedef vector <vi> vvi;
typedef pair <int, int> ii;
typedef vector <ii> vii;
typedef vector <string> vs;
typedef long long ll;
typedef long double ld;
typedef double D;

#define filename "a"

template <class T> T abs (const T & a) {
    re a > 0 ? a : -a;
}

int n;
int m;

int main() {
#ifdef LOCAL_DEBUG
    freopen("input.txt", "r", stdin);
    //freopen("output.txt", "w", stdout);
#endif

    cin >> n;
    rrep(i, n + 1) {
        if (n >= 7 * i) {
            int res = n - 7 * i;
            if (res % 4 == 0) {
                res /= 4;
                rep(t, res)
                    cout << 4;
                rep(j, i)
                    cout << 7;
                cout << endl;
                re 0;
            }
        }
    }

    cout << -1 << endl;

    return 0;
}
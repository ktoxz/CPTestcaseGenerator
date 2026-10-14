#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <cmath>
#include <stack>
#include <iomanip>

using namespace std;

#define forn(i, n) for (int i = 0; i < n; ++i)
#define vi vector
#define pb push_back
#define all(a) (a).begin(), (a).end()

typedef long long ll;
typedef pair<int, int> pii;


int main() {
    ll n, m;
    cin >> n >> m;
    ll f = 0;

    forn(i, m) {
        ll x, d;
        cin >> x >> d;
        f += n * x;
        if (d >= 0) {
            ll curr = (ll) ((n * (n - 1)) / 2) * (ll) d;
            f += curr;
        } else {
            ll k = n / 2;
            k = (ll) k;
            ll k2 = (ll) max((int)(n - 1 - k), 0);
            ll curr = (((k + 1) * k) / 2) * d;
            curr += (((k2 + 1) * k2) / 2) * d;
            f += curr;
        }
    }

    f = (double) f;


    cout << setprecision(7) << f / ((double) n );
    return 0;
}
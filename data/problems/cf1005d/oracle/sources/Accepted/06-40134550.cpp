#include<bits/stdc++.h>
#define MOD 1000000007
#define F first
#define S second
#define PI 3.14159265
typedef long long ll;
using namespace std;

string s;
int n, a[200010], cnt;
int main() {
    ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);
    cin >> s;
    n = s.size();
    for (int i = 0; i < n; ++i)
        a[i] = s[i] -  '0';
    for (int i = 0; i < n; ++i) {
        if (a[i] % 3 == 0) {
            ++cnt;
            continue;
        }

        if (i == n - 1) break;
        else ++i;

        if (a[i] % 3 == 0) {
            ++cnt;
            continue;
        }
        else if ((a[i - 1] +  a[i]) % 3 == 0) {
            ++cnt;
            continue;
        }

        if (i == n - 1) break;
        else {
            ++i;
            ++cnt;
        }
    }

    cout << cnt;
    return 0;
}
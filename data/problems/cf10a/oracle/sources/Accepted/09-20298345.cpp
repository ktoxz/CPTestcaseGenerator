#include <iostream>

using namespace std;

int main() {
    int n, p1, p2, p3, t1, t2;
    cin >> n >> p1 >> p2 >> p3 >> t1 >> t2;
    int oldR = 0, ans = 0;
    for (int i = 0; i < n; ++i) {
        int l, r;
        cin >> l >> r;
        if (i) {
            ans += min(l - oldR, t1) * p1 +
                    min(max(0, l - oldR - t1), t2) * p2 +
                    max(0, l - oldR - t1 - t2) * p3;
        }
        ans += (r - l) * p1;
        oldR = r;
    }
    cout << ans << "\n";
    return 0;
}
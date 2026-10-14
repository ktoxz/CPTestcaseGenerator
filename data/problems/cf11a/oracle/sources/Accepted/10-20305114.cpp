#include <iostream>
#include <cstdlib>

using namespace std;

int main() {
    int n, d;
    cin >> n >> d;
    int prev = 0, ans = 0;
    for (int i = 0; i < n; ++i) {
        int a;
        cin >> a;
        if (prev >= a) {
            int delt = ((prev - a) / d + 1);
            a += d * delt;
            ans += delt;
        }
        prev = a;
    }
    cout << ans << "\n";
//    system("pause");
    return 0;
}
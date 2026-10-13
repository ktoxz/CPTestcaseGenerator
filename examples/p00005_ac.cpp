#include <iostream>
#include <numeric>
using namespace std;
int main() {
    long long a, b;
    while (cin >> a >> b) {
        long long g = gcd(a, b);
        cout << g << ' ' << (a / g) * b << '\n';
    }
}

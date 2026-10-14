#include <iostream>
#include <iomanip>
#include <string>
#include <algorithm>
#include <unordered_set>
using namespace std;

int gcd(int a, int b) {
    if (a == b)
        return a;

    if (a > b) {
        return gcd(a - b, b);
    } else {
        return gcd(b - a, a);
    }
}

int main()
{
    int a, b, n;

    cin >> a >> b >> n;

    bool turn = true;
    while (n > 0) {
        if (turn) {
            int g = gcd(a, n);
            if (g > n) {
                break;
            }
            n -= g;
            turn = false;
        } else {
            int g = gcd(b, n);
            if (g > n) {
                break;
            }
            n -= g;
            turn = true;
        }
    }

    cout << turn << endl;
    return 0;
}
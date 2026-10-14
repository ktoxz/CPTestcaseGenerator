#include <iostream>

using namespace std;

int main()
{
    char c[9];
    for (int i(0); i < 9; ++i) cin >> c[i];
    for (int i(0); i < 4; ++i) if (c[i] != c[8 - i]) { cout << "NO"; return 0; }
    cout << "YES";
}
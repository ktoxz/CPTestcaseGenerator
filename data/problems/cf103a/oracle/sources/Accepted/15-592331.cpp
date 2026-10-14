#include <iostream>
using namespace std;

int main()
{
    int n;
    long long a, ret;
    while (cin >> n)
    {
        cin >> ret;
        for (int i = 1; i < n; ++i)
        {
            cin >> a;
            ret += (a - 1) * (i + 1) + 1;
        }
        cout << ret << endl;
    }
    return 0;
}
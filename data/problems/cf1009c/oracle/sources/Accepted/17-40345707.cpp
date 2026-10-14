#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cmath>
#include <queue>
#include <set>
#include <map>
#include <iomanip>

using namespace std;

int main() {
    
    long long n, m;
    cin >> n >> m;
    
    long double sum = 0;
    for (int i = 0; i < m; ++i)
    {
        long double x, d;
        cin >> x >> d;
        
        sum += x * n;
        
        if (d > 0)
        {
            if (n > 2)
            {
                long long num = ((n * (n - 1)) / 2);
                sum += num * d;
            }
            else if (n == 2)
            {
                sum += d;
            }
        }
        else
        {
            if (n > 4)
            {
                if (n % 2)
                {
                    long long num = (((n - 1) / 2) + 1) * (n - 1) / 2;
                    sum += num * d;
                }
                else
                {
                    long long num = ((n / 2) + 1) * (n / 2) / 2 + (n / 2) * ((n / 2) - 1) / 2;
                    sum += num * d;
                }
            }
            else if (n == 2)
            {
                sum += d;
            }
            else if (n == 3)
            {
                sum += 2 * d;
            }
            else if (n == 4)
            {
                sum += 4 * d;
            }
        }
    }
    
    cout << fixed << setprecision(10) << sum / (long double)n << endl;
    
    return 0;
}
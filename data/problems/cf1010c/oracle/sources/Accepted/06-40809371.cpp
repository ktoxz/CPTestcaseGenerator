#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

template<class T> inline T gcd(T a, T b)
{
    if(a < 0) return gcd(-a, b);
    if(b < 0) return gcd(a, -b);
    return (b==0) ? a : gcd(b, a%b);
}

int main()
{
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    int g = 1;
    for(int i = 0; i < n; ++i)
    {
        cin >> a[i];
        a[i] = a[i] % k;
        if(i == 0)
	        g = gcd(k, a[i]);
        else
            g = gcd(g, gcd(k, a[i]));
    }
    cout << k / g << endl;
    for(int i = 0; i < k; i += g)
        printf("%d ", i);
    
    
    return 0;
}
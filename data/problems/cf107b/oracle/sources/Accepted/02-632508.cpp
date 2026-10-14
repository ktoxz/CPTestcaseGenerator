//

#include <algorithm>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <complex>
#include <sstream>
#include <iomanip>
#include <cstdio>
#include <vector>
#include <bitset>
#include <cmath>
#include <set>
#include <map>

//#define int long long
#define eps 10e-8
#define sqr(x) ((x) * (x))
#define prec(x) fixed << setprecision (x)
#define equal(a,b) ((bool) (abs ((a) - (b) < eps))) 
#define dis(x1,y1,x2,y2) (sqrt ((sqr ((x1) - (x2)))+(sqr ((y1) - (y2)))))

using namespace std;

#define maxN (1000 + 10)

int n, m, h;
int a[maxN];

/*double c (int n, int r)
{
	if (r == 0)
		return 1;
	return c (n - 1, r - 1) * (double) n / (double) r;
}*/

double c (int n, int r)
{
	double res = 1;
	for (int i = n - r + 1; i <= n; i++)
		res *= i;
	return res;
}

main()
{
	cin >> n >> m >> h;
	h--;
	int s = 0, os = 0;
	for (int i = 0; i < m; i++)
	{
		cin >> a[i];
		s += a[i];
		if (h != i)
			os += a[i];
	}

	cout << prec(6);
	if (s < n)
	{
		cout << -1 << endl;
		return 0;
	}
	if (os < n - 1)
	{
		cout << 1 << endl;
		return 0;
	}
	double res = 1;
	res -= c (os, n - 1) / c (s - 1, n - 1);
	cout << res << endl;

	return 0;
}
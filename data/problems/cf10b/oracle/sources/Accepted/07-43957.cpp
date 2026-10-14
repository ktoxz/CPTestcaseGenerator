#include <iostream>
#include <cmath>

using namespace std;

int n, k, ceilk;
bool arr[2000][2000];

int absi(int n)
{
	return n < 0 ? -n : n;
}

int sum_dist(int x, int y, int m)
{
	int s = 0;
	for(int i = 0; i < m; i++)
		s += absi(x - ceilk) + absi(y + i - ceilk);
	return s;
}

bool free (int x, int y, int m)
{
	for(int i = 0; i < m; i++)
		if(arr[x][y + i])
			return false;
	return true;
}

int main ()
{
	cin >> n >> k;
	ceilk = ceil(k / 2.0);
	for(int i = 0; i < n; i++)
	{
		int m;
		cin >> m;
		int min = -1, minx, miny;
		for(int x = 1; x <= k; x++)
		{
			for(int y = 1; y <= k - m + 1; y++)
			{
				if(free(x, y, m))
				{
					int tmp = sum_dist(x, y, m);
					if(min == -1 || tmp < min || (tmp == min && x < minx))
					{
						min = tmp;
						minx = x;
						miny = y;
					}
				}
			}
		}
		if(min < 0)
			cout << min << endl;
		else
		{
			cout << minx << ' ' << miny << ' ' << miny + m - 1 << endl;
			for(int j = 0; j < m; j++)
				arr[minx][miny + j] = true;
		}
	}
}
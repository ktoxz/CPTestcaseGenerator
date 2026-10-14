#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <vector>
#include <bitset>
#include <iomanip>
#include <queue>
#include <stack>
#include <map>
#include <set>
#include <sstream>
#include <cstdio>
#include <strstream>

using namespace std;

int a[110][110],n;

int main()
{
	int i,j,m,t,M,k;
	
	cin >> m >> n;

	for (i = 0 ; i < n; i++)
		for (j = 0 ; j < n;j++)
			a[i][j] = 0;

	int xc = (n + 1)/2 - 1;
	int yc = (n + 1)/2 - 1;
	
	for (t = 0 ; t < m; t++)
	{
		cin >> M;
		int answer = -1,ansX,ansYs,ansYe;
		for (i = 0; i < n; i++)
		{
			for (j = 0; j <= n - M;j++)
			{
				bool f = true;
				for (k = 0; k < M && f; k++)
					if (a[i][j + k] != 0)
						f = false;
				if (f)
				{
					int ans = 0;
					for (k = 0; k < M && f; k++)
						ans += abs(i - xc) + abs(j + k - yc);
					if (ans < answer || answer == -1)
					{
						answer = ans;
						ansX  = i;
						ansYs = j;
						ansYe = j + M - 1;
					}
				}
			}
		}
		if (answer == -1)
			cout << answer << endl;
		else
		{
			cout << ansX + 1 << " " << ansYs + 1 << " " << ansYe + 1 << endl;
			for (i = ansYs; i <= ansYe; i++)
				a[ansX][i] = 1;
		}
	}
	
	return 0;
}
#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

int arr[120000];
bool good[120000];

int main()
{
	cin.sync_with_stdio(false), cin.tie(nullptr);

	int n;
	cin >> n;
	for (int i = 0; i < n; i++)
	{
		cin >> arr[i];
	}
	sort(arr, arr + n);

	for (int i = 0; i < n; i++)
	{
		for (int j = 0; j <= 30; j++)
		{
			int x = 1 << j;
			int target = x - arr[i];
			if (target < 0)
				continue;
			auto iter = lower_bound(arr, arr+n, target);
			if (iter != arr + n && *iter == target)
			{
				if (iter - arr == i)
				{
					if (*(iter + 1) == target)
					{
						good[i] = true;
						break;
					}
				}
				else
				{
					good[i] = true;
					break;
				}
			}
		}
	}
	int ans = 0;
	for (int i = 0; i < n; i++)
		ans += !good[i];
	cout << ans << endl;
	//for (int i = 0; i < n; i++)
	//{
	//	for (int j = 0; j <= 30; j++)
	//	{
	//		int x = 1 << j;
	//		int target = x - arr[i];
	//		auto iter = lower_bound(arr, arr+n, target);
	//		if (target > 0 && iter != arr + n && *iter == target)
	//			;
	//	}
	//}

	return 0;
}
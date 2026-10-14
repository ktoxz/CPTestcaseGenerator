#include<iostream>
#include<algorithm>
#include<cstring>
#include<map>

using namespace std;

int dp[100];

int main()
{
	for (int i = 0; i <= 30; i++)
		dp[i] = 1 << i;
	int N, del[200000] = { 0 }, num[200000] = { 0 }, cnt = 0;

	scanf("%d", &N);

	for (int i = 0; i < N; i++) {
		scanf("%d", &num[i]);
	}
	sort(num, num + N);
	for (int i = 0; i < N; i++) {
		int flg = true;
		for (int j = 0; j <= 30; j++) {
			if (dp[j] > num[i]) {
				auto lo = lower_bound(num, num + N, dp[j] - num[i]);
				auto up = upper_bound(num, num + N, dp[j] - num[i]) - 1;
				if (lo != &num[i] && *lo == dp[j] - num[i]) {
					flg = false;
					break;
				}
				if (up != &num[i] && *up == dp[j] - num[i]) {
					flg = false;
					break;
				}
			}
		}
		if (flg)
			cnt++;
	}

	printf("%d", cnt);

	return 0;
}
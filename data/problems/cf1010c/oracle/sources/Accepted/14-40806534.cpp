#include <bits/stdc++.h>
using namespace std;
const int N = 112345;

int main () {
	int n, k; scanf("%d %d", &n, &k);
	int kappaloiro = k;
	for (int i = 0; i < n; ++i) {
		int x; scanf("%d", &x); x %= k;
		kappaloiro = __gcd(kappaloiro, __gcd(x, k));
	}
	vector<int> ans;
	ans.push_back(0);
	for (int i = kappaloiro; i < k; i += kappaloiro)
		ans.push_back(i);
	printf("%d\n", int(ans.size()));
	for (auto i : ans)
		printf("%d ", i);
	return puts(""), 0;
}
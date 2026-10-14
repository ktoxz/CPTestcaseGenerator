#include <bits\stdc++.h>
using namespace std;

#define sc(a) scanf("%d",&(a))
#define ll long long

long long a[200005];
long long s[200005] = {};

int main() {

	int n;
	cin >> n;

	string a;
	string b;
	cin >> a >> b;

	if (n == 1) {
		if (a[0] == b[0])
			cout << 0 << endl;
		else
			cout << 1 << endl;
		return 0;
	}

	int cnt = 0;

	char c[26];


	for (int i = 0; i < (n / 2); i++) {
		int j = n - i - 1;

		for (int i = 0; i < 26; i++)
			c[i] = 0;

		c[b[i] - 'a']++;
		c[b[j] - 'a']++;
		c[a[i] - 'a']--;
		c[a[j] - 'a']--;

		int sum = 0;
		int havem2 = 0;
		int have2 = 0;
		for (int i = 0; i < 26; i++)
		{
			if (c[i] > 0)
				sum += c[i];
			if (c[i] == 2) {
				have2 = 1;
			}
			else if (c[i] == -2)
				havem2 = 1;

			if (have2&&havem2) {
				sum = 0;
				break;
			}

		}
		if (have2 && !havem2)
			sum = 1;
		cnt += sum;
	}

	if (n % 2) {
		if (a[n / 2] == b[n / 2])
			;
		else
			cnt++;
	}


	cout << cnt << endl;
	return 0;
}
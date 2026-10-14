#define _CRT_SECURE_NO_WARNINGS

#include<iostream>

#include<vector>

#include<set>

#include<map>

#include<queue>

#include<algorithm>

#include<numeric>

#include<string>

#include <iomanip>

#include<string.h>

#include<memory.h>

#include<stdlib.h>

#include<cstdio>

#include <stack>

#include <bitset>





using namespace std;

typedef long long LL;

#define mp make_pair



long double d(long double n1, long double s, long double sms)

{

	long double tmp = 1;

	for (int i = s - n1 + 1; i <= s; i++)

	{

		tmp *= (long double)i;

	}

	for (int i = sms - n1; i < sms; i++)

	{

		tmp /= (long double)i;

	}



	

	return tmp;

}



int main()

{

#ifdef _DEBUG

	freopen("input.txt", "r", stdin);

	freopen("output.txt", "w", stdout);

#endif



	int n, m, h;

	scanf("%d%d%d", &n, &m, &h);



	vector<int> a(m + 1);

	int sms = 0;

	for (int i = 1; i <= m; i++)

	{

		scanf("%d", &a[i]);

		sms += a[i];

	}

	int n1 = n - 1;

	int s = sms - a[h];

	if (sms < n)

	{

		cout << -1;

		return 0;

	}

	if (s < n1)

	{

		cout << 1;

		return 0;

	}

	long double ans = 1;



	cout << setprecision(10) << fixed << 1 - d(n1, s, sms);



	return 0;

}
#include <vector>

#include <list>

#include <map>

#include <math.h>

#include <cmath>

#include <set>

#include <queue>

#include <deque>

#include <string>

#include <stack>

#include <bitset>

#include <algorithm>

#include <functional>

#include <numeric>

#include <utility>

#include <string.h>

#include <sstream>

#include <iostream>

#include <iomanip>

#include <cstdio>

#include <cstdlib>

#include <ctime>

#include <unordered_map>



#define ll long long int

#define ld long double



using namespace std;

vector<pair<pair<int,int>,pair<int,pair<int,int> > > >arr;

int main()

{

	ios::sync_with_stdio(false);

	ios_base::sync_with_stdio(false);

	cin.tie(nullptr), cout.tie(nullptr);

	//freopen("input.txt", "r", stdin);

	//freopen("output.txt", "w", stdout);

	int n,a,b,c,d;

	cin >> n;

	for (int i = 0; i < n;i++)

	{

		cin >> a >> b >> c >> d; 

		arr.push_back({ { d, i + 1 }, { a, { b, c } } });

	}

	sort(arr.begin(), arr.end());

	for (int i = 0; i < n; i++)

	{

		for (int j = i + 1; j < n; j++)

		{

			if (arr[j].second.first > arr[i].second.first &&

				arr[j].second.second.first > arr[i].second.second.first &&

				arr[j].second.second.second > arr[i].second.second.second)

			{

				break;

			}

			if (j == n - 1)

			{

				cout << arr[i].first.second << endl;

				return 0;

			}

		}

	}

	cout << arr[n-1].first.second << endl;

	return 0;

}
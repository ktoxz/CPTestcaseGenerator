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

int main()

{

	ios::sync_with_stdio(false);

	ios_base::sync_with_stdio(false);

	cin.tie(nullptr), cout.tie(nullptr);

	freopen("input.txt", "r", stdin);

	freopen("output.txt", "w", stdout);

	string a;

	char b;

	cin >> a >> b;

	if ((a == "front" && b == '1') || (a == "back" && b == '2'))cout << "L\n";

	else cout << "R\n";

	return 0;

}
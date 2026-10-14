#include <algorithm>

#include <iomanip>

#include <istream>

#include <map>

#include <numeric>

#include <ostream>

#include <set>

#include <sstream>

#include <string>

#include <utility>

#include <vector>

#include <queue>

#include <iostream>

#include <string>



using namespace std;

// Powered by caide (code generator, tester, and library code inliner)



const int size = 101;



long long a[size];





class Solution {

public:

	void solve(std::istream& in, std::ostream& out) {



		int n; in >> n;



		long long ans = 0;



		long long sum = 0;

		for (int i = 0; i < n; i++){

			in >> a[i];



			ans += a[i];

			ans += (a[i] - 1) * i;

		}



		out << ans;



	}

};



void solve(std::istream& in, std::ostream& out)

{

	out << std::setprecision(12);

	Solution solution;

	solution.solve(in, out);

}

#include <fstream>

#include <iostream>



int main() {

	ios_base::sync_with_stdio(0);

	cin.tie(0);



	istream& in = cin;



	ostream& out = cout;

	solve(in, out);



	int end;

	cin >> end;

	return 0;

}
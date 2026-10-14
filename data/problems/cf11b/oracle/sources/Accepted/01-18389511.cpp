#include <bits/stdc++.h>



#define mp make_pair

#define pb push_back

#define PI 3.14159265358979323846



using namespace std;



typedef unsigned long long ull;

typedef long long ll;

typedef long double ld;



const int MAXN = 100 + 10;

const int INF = INT_MAX;

const double EXP = 0.0001;



void files(){

	freopen("input.txt", "r", stdin);

	freopen("output.txt", "w", stdout);

}



int main(){

//	files();

	ios_base::sync_with_stdio(false);



	int x;



	cin >> x;

	x = abs(x);



	int i = 0, s = 0;

	while (true){

		s += i;

		if (s >= x && (s - x) % 2 == 0) {cout << i; return 0;}

		i++;

	}



	return 0;

}
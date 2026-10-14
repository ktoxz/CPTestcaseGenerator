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



bool a[MAXN][MAXN];



int main(){

//	files();

	ios_base::sync_with_stdio(false);



	int n, k, m;



	cin >> n >> k;

	int mid = round((double)k / 2);

	for (int i = 0; i < n; i++){

		cin >> m;

		int Min = INF, ansx = -1, ansr = -1, ansl = -1;

		for (int x = 1; x <= k; x++)

			for (int y = 1; y <= k - m + 1; y++){

				bool gg = false;

				int sum = 0;

				for (int r = y; r <= y + m - 1; r++){

					if (a[x][r]) {gg = true; break;}

					sum += abs(x - mid) + abs(r - mid);

				}

				if (!gg)

					if (sum < Min){

						Min = sum;

						ansx = x;

						ansl = y;

						ansr = y + m - 1;

					}

			}

		if (ansx == -1) cout << -1 << endl;

		else {

			cout << ansx << " " << ansl << " " << ansr << endl;

			for (int j = ansl; j <= ansr; j++)

				a[ansx][j] = true;

		}	

	}	

							

	return 0;

}
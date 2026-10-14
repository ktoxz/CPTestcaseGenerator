#include <string>
#include <vector>
#include <cstdio>
#include <iostream>
#include <algorithm>

using namespace std;

#define MAX_N 1000

typedef struct {
	int d;
	int x;
} node;

int n;
int p;
node a[MAX_N][2];

int main(void) {
	int x; int y; int d;
	
	cin >> n >> p;
	for (int i = 0; i < p; i++) {
		cin >> x >> y >> d;
		a[x - 1][0].d = d;
		a[x - 1][0].x = y - 1;
		a[y - 1][1].d = d;
		a[y - 1][1].x = x - 1;
	}
	
	int sol[MAX_N][3];
	int sol_cnt = 0;
	
	for (int i = 0; i < n; i++) {
		int min_d = a[i][0].d;
		if (a[i][0].d != 0 && a[i][1].d == 0) {
			int j = a[i][0].x;
			while (a[j][0].d != 0) {
				if (a[j][0].d < min_d)
					min_d = a[j][0].d;
				j = a[j][0].x;
			}
			sol[sol_cnt][0] = i + 1;
			sol[sol_cnt][1] = j + 1;
			sol[sol_cnt][2] = min_d;
			sol_cnt++;
		}
	}
	
	cout << sol_cnt << "\n";
	for (int i = 0; i < sol_cnt; i++) {
		cout << sol[i][0] << " " << sol[i][1] << " " << sol[i][2] << "\n";
	}
	
	//system("pause");
	
    return 0;
}
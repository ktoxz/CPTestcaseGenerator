#include <iostream>
#include <cstdio>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <cstring>
#include <string.h>
#include <cstdlib>
#include <sstream>
#include <stack>
#include <queue>
#include <numeric>
#include <utility>
#include <cctype>
#include <list>
#include <climits>
#include <signal.h>
#include <ctime>
#include <map>
#include <set>

using namespace std;

struct lap{
	int a;
	int b;
	int c;
	int d;
	int in;
};

bool compare(const lap&a, const lap&b){
	return a.d < b.d;
}

int main(){

	long long int i, j, k, ct=0, n, t, x, y, z;
	double a, b, c, d;
	char p, q, r, s;

	lap lp[200];
	string str, s1, s2, s3;
	map<int, int> m;
	vector<int> v;

	cin >> t;
	
	for( i = 0; i < t; i++ ) {
		cin >> lp[i].a >> lp[i].b >> lp[i].c >> lp[i].d;
		lp[i].in = i+1;
	}

	sort(lp, lp+t, compare);

	bool fl = false;
	int ans;

	for(i = 0; i<t; i++){
		fl = false;

		for(j = 0; j < t; j++){
			if(lp[i].a < lp[j].a && lp[i].b < lp[j].b && lp[i].c < lp[j].c ){
				fl = true;
				break;
			}
		}

		if(fl == false){
			cout << lp[i].in;
			break;
		}
	}

	return 0;
}
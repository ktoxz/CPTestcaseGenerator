#include <bits/stdc++.h>

using namespace std;

int main() {

	long long n,d,x,y,s=0,t;

	cin >> n >> d;

	x=0;

	for (long i=0;i<n;i++) {

		cin >> y;

		if (x>=y) {

			t=(x-y)/d+1;

			s+=t;

			x=y+t*d;

		} else x=y;

	}

	cout << s;

}
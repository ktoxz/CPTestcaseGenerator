#include <iostream>
using namespace std;

int main() {

//freopen("in.txt", "r", stdin);

int N, l[128], r[128], i, P1, P2, P3, T1, T2, RES, tmp;

cin >> N;
cin >> P1;
cin >> P2;
cin >> P3;
cin >> T1;
cin >> T2;

RES = 0;
for (i=0; i<N; i++) {
	cin >> l[i];
	cin >> r[i];
	RES += (r[i]-l[i])*P1;
}

for (i=1; i<N; i++) {
	tmp = l[i]-r[i-1];
	if (tmp > T1 + T2) RES += T1*P1 + T2*P2 + (tmp-T1-T2)*P3;
	else if (tmp > T1) RES += T1*P1 + (tmp-T1)*P2;
	else RES += tmp*P1;
}

cout << RES << endl;

return 0;
}
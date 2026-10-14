#include <bits/stdc++.h>



using namespace std;



int main(){

	long long i, j, d = 1;

	string t, m;

	cin >> t >> m;

	if (t == m && t.size() == 1){

		cout << "OK" << endl;

		return 0;

	} else {

		sort(t.begin(), t.end());

		if (t[0] == '0'){

			while (t[d] == '0') d++;

			swap(t[0], t[d]);

		}

		t == m ? cout << "OK" << endl : cout << "WRONG_ANSWER" << endl;

		return 0;

	}

}
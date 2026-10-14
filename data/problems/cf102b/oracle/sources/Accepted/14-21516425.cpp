#include <bits/stdc++.h>



using namespace std;



int main() {

    string str;

    cin >> str;

    int n, res = 0;

    while (true) {

        if (str.size() == 1) {

            break;

        }

        ++res;

        n = 0;

        for (int i = 0; i < str.size(); ++i) {

            n += str[i] - '0';

        }

        str = to_string(n);

    }

    cout << res << endl;

}
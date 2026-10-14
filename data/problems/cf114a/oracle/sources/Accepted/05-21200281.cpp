#include <algorithm>

#include <iostream>

#include <fstream>

#include <utility>

#include <iomanip>

#include <string>

#include <math.h>

#include <vector>

#include <cmath>

#include <ctime>

#include <queue>

#include <map>

#include <set>

#define F first

#define S second

#define PB push_back

#define PPB pop_back

#define MP make_pair

#define LL long long

#define ULL unsigned long long

using namespace std;



const ULL MXN = 1e18 + 7;

ULL k, l;



int main () {

    cin >> k >> l;

    if (l % k != 0) {

        cout << "NO";

        return 0;

    }

    int index = 0;

    for (ULL i = k;i <= MXN; i *= k) {

        if (i > l) {

            cout << "NO";

            return 0;

        }

        if (i == l) {

            cout << "YES\n" << index;

            return 0;

        }

        index++;

    }

}
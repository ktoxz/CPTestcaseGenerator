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

#define sz(a) (int)a.size()

#define PII pair <int, int>

#define ULL unsigned long long

using namespace std;



int n, c[20];



void fillItUp() {

    for (int i = 1;i <= 9; i++)

        c[i] = 4;

    c[10] = 15;

    c[11] = 4;

}



int main () {

    cin >> n;

    fillItUp();

    if (n - 10 > 0)

        cout << c[n - 10];

    else

        cout << 0;

    return 0;

}
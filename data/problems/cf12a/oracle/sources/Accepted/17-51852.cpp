//  Copyright(c) 2009-2010, all rights reserved.
//  written by ZHUMAZHANOV ADLET.

#include <iostream>
#include <iterator>
#include <sstream>
#include <iomanip>
#include <algorithm>
#include <numeric>
#include <utility>
#include <functional>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <cstring>
#include <climits>
#include <string>
#include <vector>
#include <bitset>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <queue>
#include <stack>

#define PROBLEM_NAME    "data"
#define SZ(v)           (int)v.size()

#define sqr(x)          ((x)*(x))
#define all(v)          v.begin(), v.end()

typedef unsigned int uint;
typedef long long i64;

using namespace std;

const int   n = 3;

char a[3][3];

void Assert(const int& value,
            const int& lowerBound, const int& upperBound)
{
    assert (lowerBound <= value && value <= upperBound);
}

void print_ok() {
    cout << "YES";
    exit(EXIT_SUCCESS);
}

int main() {

//    assert (freopen(PROBLEM_NAME".in", "r", stdin));
//    assert (freopen(PROBLEM_NAME".out", "w", stdout));

    int amountX = 0;
    for (int i = 0; i < n; ++ i) {
        for (int j = 0; j < n; ++ j) {
            //scanf("%c", &a[i][j]);
            cin >> a[i][j];
            amountX += (a[i][j] == 'X' ? 1 : 0);
        }
    //    scanf("\n");
    }

    /*if (amountX == 0) {
        cout << "NO";
        return 0;
    }*/

    printf ("%s", (a[0][0] == a[n-1][n-1] && a[0][n-1] == a[n-1][0] && a[n/2][0] == a[n/2][n-1] && a[0][n/2] == a[n-1][n/2] ? "YES" : "NO"));
    return 0;

    bool flag = true;
    for (int i = 0; i < n; ++ i)
        if (a[0][i] != a[n-1][i]) {
            flag = false;
            break;
        }

    if (flag && a[n/2][0] == a[n/2][n-1]) {
        print_ok();
    }

    flag = true;
    for (int i = 0; i < n; ++ i)
        if (a[i][0] != a[i][n-1]) {
            flag = false;
            break;
        }

    if (flag && a[0][n/2] == a[n-1][n/2]) {
        print_ok();
    }

    flag = true;
    for (int i = 0; i < n; ++ i) {
        for (int j = 0; j < n; ++ j)
            if (a[i][j] != a[j][i]) {
                flag = false;
                break;
            }
        if (!flag) break;
    }

    if (flag) print_ok();

    flag = true;
    for (int i = 0; i < n; ++ i) {
        for (int j = 0; j < n; ++ j) {
            if (a[i][j] != a[n-i-1][n-j-1]) {
                flag = false;
                break;
            }
        }
        if (!flag) break;
    }

    if (flag) print_ok();

    cout << "NO";

    return 0;
}
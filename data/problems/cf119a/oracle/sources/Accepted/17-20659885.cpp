#include <iostream>

#include <fstream>

#include <map>

#include <set>

#include <vector>

#include <queue>

#include <list>

#include <stack>

#include <string>

#include <algorithm>

#include <cmath>

#include <cstdio>



using namespace std;



#define X first

#define Y second



#define add push_back

typedef long long ll;

typedef pair<int, int> Point;

typedef pair<float, float> PointF;

typedef pair<double, double> PointD;



int gcd(int a, int b) {

    if (a == 0 || b == 0) {

        return a + b;

    }

    if (a < b) {

        swap(a, b);

    }

    if (a > b) {

        return gcd(a - b, b);

    }

    return a;

}





int main() {

    ios::sync_with_stdio(false);

    cin.tie(NULL);



    int a, b, n;

    cin >> a >> b >> n;

    bool flag = true;



    while (true) {

        int t;

        if (flag) {

            t = gcd(a, n);

        } else {

            t = gcd(b, n);

        }

        if (n < t) {

            break;

        } else {

            n -= t;

            flag = !flag;

        }



    }

    cout << (flag ? 1 : 0) << endl;







#ifdef _DEBUG

    system("pause");

#endif

    return 0;

}
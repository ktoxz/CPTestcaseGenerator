#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;

const int INF = (int) 1e9;

unsigned int n;
vector<vector<bool>> cinema;
int ic = 0, jc = 0;

int empty(int u, int l, int r) {
    int ans = abs(u - ic) * (r - l + 1);
    for (int j = l; j <= r; ++j) {
        if (cinema[u][j]) {
            return -1;
        }
        ans += abs(j - jc);
    }
    return ans;
}

void notEmpty(int u, int l, int r) {
    for (int i = l; i <= r; ++i) {
        cinema[u][i] = true;
    }
}

int main() {
    int q;
    cin >> q >> n;
    ic = n / 2;
    jc = n / 2;
    cinema.resize(n, vector<bool>(n, false));
    for (int t = 0; t < q; ++t) {
        int m;
        cin >> m;
        int minDist = INF;
        int y = 0, x = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n - m + 1; ++j) {
                int e = empty(i, j, j + m - 1);
//                cout << i << " " << j << " " << e << "\n";
                if (e != -1 && e < minDist) {
                    minDist = e;
                    y = i;
                    x = j;
                }
            }
        }
        if (minDist != INF) {
            notEmpty(y, x, x + m - 1);
            cout << y + 1 << " " << x + 1 << " " << x + m << "\n";
        } else {
            cout << "-1\n";
        }
//        for (int i = 0; i < n; ++i) {
//            for (int j = 0; j < n; ++j) {
//                cout << cinema[i][j];
//            }
//            cout << "\n";
//        }
    }
//    system("pause");
    return 0;
}
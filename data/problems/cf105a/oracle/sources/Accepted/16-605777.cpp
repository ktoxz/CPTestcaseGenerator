#include <cstdio>
#include <iostream>
#include <map>
#include <string>
using namespace std;

map <string, int> mp;

int main()
{
    int n, m;
    double k;

    while (scanf("%d%d%lf", &n, &m, &k) != EOF) {
        int K = (k+1e-6) * 100;
        string name;
        int t;
        for (int i = 0; i < n; ++i) {
            cin >> name >> t;
            int v = t * K;
            if (v < 10000) continue;
            mp[name] = v / 100;
        }
        for (int i = 0; i < m; ++i) {
            cin >> name;
            if (mp.find(name) == mp.end()) mp[name] = 0;
        }
        cout << mp.size() << endl;
        for (map <string, int> :: iterator it = mp.begin(); it != mp.end(); ++it) {
            cout << it -> first << " " << it -> second << endl;
        }
    }
    return 0;
}
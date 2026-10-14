#include <bits/stdc++.h>

using namespace std;

bool big(int a, int b) { return a > b; }
bool few(int a, int b) { return a < b; }

int main()
{
    int n, m;
    cin >> n >> m;
    int c[n];
    for (int i(0); i < n; ++i) cin >> c[i];
    sort(c, c + n, few);
    string tmp;
    map <string, int> List;
    for (int i(0); i < m; ++i)
    {
        cin >> tmp;
        ++List[tmp];
    }
    int num[List.size()], p(0);
    for (map <string, int>::iterator i(List.begin()); i != List.end(); ++i)
        num[p++] = i->second;
    sort(num, num + p, big);
    int ans(0);
    for (int i(0); i < p; ++i) ans += c[i] * num[i];
    cout << ans << ' ';
    sort(c, c + n, big);
    ans = 0;
    for (int i(0); i < p; ++i) ans += c[i] * num[i];
    cout << ans;
}
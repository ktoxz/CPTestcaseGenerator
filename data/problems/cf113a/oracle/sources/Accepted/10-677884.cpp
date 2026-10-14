#include <cstdlib>
#include <cstdio>
#include <cctype>
#include <cstring>
#include <cmath>
#include <ctime>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <bitset>
#include <set>
#include <vector>
#include <queue>
#include <stack>
#include <map>
#include <numeric>
#include <utility>
#include <list>

using namespace std;

typedef long long ll;
typedef long double ld;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef stringstream ss;
typedef istringstream iss;

const int INF = (int)2E9;
const ll LINF = (ll)9E18;

const ld PI = acos(-1.0);
const ld EPS = 1E-11;

#define For(i, a, b) for (int i = (a); i <= (b); ++i)
#define Ford(i, a, b) for (int i = (a); i >= (b); --i)
#define Rep(i, a) for (int i = 0; i < (a); ++i )
#define Repd(i, a) for (int i = (a) - 1; i >= 0; --i)
#define Fit(it, v) for (typeof((v).begin())it = (v).begin(); it != (v).end(); ++it)
#define Fitd(it, v) for (typeof((v).rbegin())it = (v).rbegin(); it != (v).rend(); ++it)

#define Let(a, b) typeof(b) a(b)
#define All(v) (v).begin(), (v).end()
#define Set(a, x) memset((a), (x), sizeof(a))
#define Size(a) ((int)(a).size())

#define Exist(a, b) (find(ALL(a), (b)) != (a).end())
#define Sort(x) sort(ALL(x))
#define Gsort(x) sort(ALL(x), greater<typeof(*((x).begin()))>())
#define Enum(v) FIT(it, (v)) cout << *it << " "; cout << endl

#define Pb push_back
#define Mp make_pair

string t[] = {"lios", "liala", "etr", "etra", "initis", "inites"};
int a[100010], n;
string s;

int next() {
    char c = ' ';
    s = "";
    while (c == ' ') {
          if (!scanf("%c", &c)) return -1;    
          if (c == '\n') return -1; 
          if (c == ' ') return -1; 
    }
        
    while (c != ' ') {
          s=s + c;
          if (!scanf("%c", &c)) c = ' ';   
          if (c == '\n') c = ' ';   
    }
    
    For (i, 0, 5) {
        size_t pos;
        pos = s.rfind(t[i]);
        if (pos == string :: npos) continue;
        if (s.size() - (int) pos == t[i].size()) return i; 
    }
    return 6;
}

int main() {
    //freopen("a.txt", "r", stdin);freopen("a.out", "w", stdout);
    n = 0;
    int nxt = next();
    while (nxt != -1) {
          n++;
          a[n - 1] = nxt;
          nxt = next();      
    }
    
    int ok = 1;
    if (n == 1) {
       if (a[0] > 5) ok = -1;      
    }
    else {
         For (i, 0, n - 1) if (a[i] > 5) ok = -1;
         For (i, 1, n - 1) 
             if (((a[i] - a[0]) % 2) != 0) ok = -1;
         For (i, 1, n - 1)
             if (a[i] < a[i - 1]) ok = -1;
         
         int cnt = 0;
         For (i, 0, n - 1) 
             if (a[i] == 2 || a[i] == 3) cnt ++;
         if (cnt != 1) ok = -1;
    }
    
    //For (i, 0, n - 1) cout << a[i] << " ";
    if (ok == 1) cout <<"YES";
    else cout << "NO";
}
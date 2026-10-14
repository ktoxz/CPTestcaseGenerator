// {{{ Headers
// vim:filetype=cpp:foldmethod=marker:foldmarker={{{,}}}

#include <cassert>
#include <cctype>
#include <cmath>
#include <climits>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>

#include <algorithm>
#include <deque>
#include <functional>
#include <iterator>
#include <list>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <stack>
#include <string>
#include <utility>
#include <vector>

#include <fstream>
#include <iostream>
#include <sstream>

using namespace std;
// }}}

typedef long long int64;
const int INF = 0x3f3f3f3f;
template <class T> inline int len (const T &a) { return a.size (); }

// {{{ Unused templates and debug
const double EPS = 1e-9;
const double PI = 3.14159265358979323846264338328;
const long long LINF = (long long) 1e16 + 5;

template <class T> inline int toInt (const T& t) { int n; stringstream ss; ss << t; ss >> n; return n; }
template <class T> inline string toStr (const T& t) { stringstream ss; ss << t; return ss.str(); }
template <class T> inline int64 toInt64 (const T& t) { int64 n; stringstream ss; ss << t; ss >> n; return n; }
template <typename T> int sgn (T val) { return (T(0) < val) - (val < T(0)); }
template <class T> T gcd (T a, T b) { T r; while (b) { r = a % b; a = b; b = r; } return a; }
template <class T> T lcm (T a, T b) { return a / gcd (a, b) * b; }

// Overloading ostream for printing STL containers (pair, vector, set, map)
template <typename T1, typename T2>
inline std::ostream &operator << (std::ostream &os, const std::pair <T1, T2> &p) {
    return os << "(" << p.first << ", " << p.second << ")";
}
template <typename T>
inline std::ostream &operator << (std::ostream &os, const std::vector <T> &v) {
    bool first = true;
    os << "[";
    for (unsigned int i = 0; i < v.size(); i++) {
        if (! first)
            os << ", ";
        os << v[i];
        first = false;
    }
    return os << "]";
}
template <typename T>
inline std::ostream &operator << (std::ostream &os, const std::set <T> &S) {
    bool first = true;
    os << "set([";
    for (typename std::set <T>::const_iterator it = S.begin(); it != S.end(); ++it) {
        if (! first)
            os << ", ";
        os << *it;
        first = false;
    }
    return os << "])";
}
template <typename T1, typename T2>
inline std::ostream &operator << (std::ostream &os, const std::map <T1, T2> &d) {
    bool first = true;
    os << "{";
    for (typename std::map<T1, T2>::const_iterator it = d.begin(); it != d.end(); ++it) {
        if (! first)
            os << ", ";
        os << it->first << ": " << it->second;
        first = false;
    }
    return os << "}";
}

// Color codes for highlighting debugs.
// Does not work within macvim due to dumb terminal.
#ifdef MVIM
    #define COLOR_CLEAR ""
    #define COLOR_RED ""
    #define COLOR_GREEN ""
    #define COLOR_MAGENTA ""
    #define COLOR_CYAN ""
#else
    #define COLOR_CLEAR "\033[0m"
    #define COLOR_RED "\033[31m"
    #define COLOR_GREEN "\033[32m"
    #define COLOR_MAGENTA "\033[35m"
    #define COLOR_CYAN "\033[36m"
#endif

// A macro to print statement and execute it.
#define exec(args...) cerr << COLOR_CYAN << #args << '\n' << COLOR_CLEAR; args

// A macro to print arrays.
#define print(arr, _N) { cerr << COLOR_RED << ">>> " << #arr << " " << #_N << COLOR_CLEAR << " #--> "; for (int _i = 0; _i < _N; _i++) cerr << arr [_i] << " "; putchar ('\n'); }

// A macro to print 2d arrays.
#define print2(arr, _R, _C) { cerr << COLOR_RED << ">>> " << #arr << " " << #_R << " " << #_C << COLOR_CLEAR << " #-->\n";\
    for (int _i = 0; _i < _R; _i++) { \
        for (int _j = 0; _j < _C; _j++) cerr << arr [_i][_j] << " ";\
        putchar ('\n'); } };

// debug () can print vector, set, map, pairs etc now.
#define debug(args...) { cerr << COLOR_RED << ">>> " << #args << COLOR_CLEAR << " #--> "; dbg, args; cerr << endl; }
struct debugger {
    template <typename T> debugger& operator, (const T v) {
        cerr << v << " ";
        return *this;
    }
} dbg;
// }}}

int memo [200005][3];
string s;
int N;

int
solve (int idx, int c) {
    if (idx >= N) return 0;
    if (memo [idx][c] != -1) return memo [idx][c];
    int ret = 0;
    int x = s [idx] - '0';
    if ((x + c) % 3 == 0 || (x % 3 == 0)) ret = max (ret, 1 + solve (idx + 1, 0));
    ret = max (ret, solve (idx + 1, x % 3));
    ret = max (ret, solve (idx + 1, (x + c) % 3));
    ret = max (ret, solve (idx + 1, 0));
    return memo [idx][c] = ret;
}

int
main () {
#ifdef LOCALHOST
    freopen ("test.in", "r", stdin);
    // freopen ("test.out", "w", stdout);
#endif
    cin >> s;
    N = len (s);
    memset (memo, -1, sizeof (memo));
    printf ("%d\n", solve (0, 0));

    return 0;
}
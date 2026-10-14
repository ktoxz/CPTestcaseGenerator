//include
//------------------------------------------
#include <vector>
#include <list>
#include <map>
#include <climits>
#include <set>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cctype>
#include <string>
#include <cstring>
#include <ctime>
#include <queue>
#include <random>
#include <cctype>
#include <complex>

using namespace std;

//typedef
//------------------------------------------
typedef long long LL;
typedef vector<int> VI;
typedef vector<bool> VB;
typedef vector<char> VC;
typedef vector<double> VD;
typedef vector<string> VS;
typedef vector<LL> VLL;
typedef vector<VI> VVI;
typedef vector<VB> VVB;
typedef vector<VS> VVS;
typedef vector<VLL> VVLL;
typedef vector<VVI> VVVI;
typedef vector<VVLL> VVVLL;
typedef pair<int, int> PII;
typedef pair<LL, LL> PLL;
typedef pair<int, string> PIS;
typedef pair<string, int> PSI;
typedef pair<string, string> PSS;


//数値・文字列
//------------------------------------------
inline int toInt(string s) {
    int v;
    istringstream sin(s);
    sin >> v;
    return v;
}

inline LL toLongLong(string s) {
    LL v;
    istringstream sin(s);
    sin >> v;
    return v;
}

template<class T>
inline string toString(T x) {
    ostringstream sout;
    sout << x;
    return sout.str();
}

inline VC toVC(string s) {
    VC data(s.begin(), s.end());
    return data;
}

template<typename List>
void SPRIT(const std::string &s, const std::string &delim, List &result) {
    result.clear();
    string::size_type pos = 0;
    while (pos != string::npos) {
        string::size_type p = s.find(delim, pos);
        if (p == string::npos) {
            result.push_back(s.substr(pos));
            break;
        } else {
            result.push_back(s.substr(pos, p - pos));
        }
        pos = p + delim.size();
    }
}

string TRIM(const string &str, const char *trimCharacterList = " \t\v\r\n") {
    string result;
    string::size_type left = str.find_first_not_of(trimCharacterList);
    if (left != string::npos) {
        string::size_type right = str.find_last_not_of(trimCharacterList);
        result = str.substr(left, right - left + 1);
    }
    return result;
}

template<typename T>
bool VECTOR_EXISTS(vector<T> vec, T data) {
    auto itr = std::find(vec.begin(), vec.end(), data);
    size_t index = distance(vec.begin(), itr);
    if (index != vec.size())return true;
    else return false;
}

#define UPPER(s) transform((s).begin(), (s).end(), (s).begin(), ::toupper)
#define LOWER(s) transform((s).begin(), (s).end(), (s).begin(), ::tolower)



//四捨五入 nLen=小数点第N位にする
//------------------------------------------

//切り上げ
double ceil_n(double dIn, int nLen) {
    double dOut;
    dOut = dIn * pow(10.0, nLen);
    dOut = (double) (int) (dOut + 0.9);
    return dOut * pow(10.0, -nLen);
}

//切り捨て
double floor_n(double dIn, int nLen) {
    double dOut;
    dOut = dIn * pow(10.0, nLen);
    dOut = (double) (int) (dOut);
    return dOut * pow(10.0, -nLen);
}

//四捨五入
double round_n(double dIn, int nLen) {
    double dOut;
    dOut = dIn * pow(10.0, nLen);
    dOut = (double) (int) (dOut + 0.5);
    return dOut * pow(10.0, -nLen);
}

//n桁目の数の取得
int take_a_n(int num, int n) {
    string str = toString(num);
    return str[str.length() - n] - '0';
}


//進数
//------------------------------------------

//"1111011" → 123
int strbase_2to10(const std::string &s) {
    int out = 0;
    for (int i = 0, size = s.size(); i < size; ++i) {
        out *= 2;
        out += ((int) s[i] == 49) ? 1 : 0;
    }
    return out;
}

//"123" → 1111011
int strbase_10to2(const std::string &s) {
    int binary = toInt(s);
    int out = 0;
    for (int i = 0; binary > 0; i++) {
        out = out + (binary % 2) * pow(static_cast<int>(10), i);
        binary = binary / 2;
    }
    return out;
}

//"ABC" 2748
int strbase_16to10(const std::string &s) {
    int out = stoi(s, 0, 16);
    return out;
}

//1111011 → 123
int intbase_2to10(int in) {
    string str = toString(in);
    return strbase_2to10(str);
}

//123 → 1111011
int intbase_10to2(int in) {
    string str = toString(in);
    return strbase_10to2(str);
}

int intbase_16to10(int in) {
    string str = toString(in);
    return strbase_16to10(str);
}

//123→ "7B"
string intbase_10to16(unsigned int val, bool lower = true) {
    if (!val)
        return std::string("0");
    std::string str;
    const char hc = lower ? 'a' : 'A';     // 小文字 or 大文字表記
    while (val != 0) {
        int d = val & 15;     // 16進数一桁を取得
        if (d < 10)
            str.insert(str.begin(), d + '0');  //  10未満の場合
        else //  10以上の場合
            str.insert(str.begin(), d - 10 + hc);
        val >>= 4;
    }
    return str;
}

//整数を2進数表記したときの1の個数を返す
LL bitcount64(LL bits) {
    bits = (bits & 0x5555555555555555) + (bits >> 1 & 0x5555555555555555);
    bits = (bits & 0x3333333333333333) + (bits >> 2 & 0x3333333333333333);
    bits = (bits & 0x0f0f0f0f0f0f0f0f) + (bits >> 4 & 0x0f0f0f0f0f0f0f0f);
    bits = (bits & 0x00ff00ff00ff00ff) + (bits >> 8 & 0x00ff00ff00ff00ff);
    bits = (bits & 0x0000ffff0000ffff) + (bits >> 16 & 0x0000ffff0000ffff);
    return (bits & 0x00000000ffffffff) + (bits >> 32 & 0x00000000ffffffff);
}



//comparison
//------------------------------------------
#define C_MAX(a, b) ((a)>(b)?(a):(b))
#define C_MIN(a, b) ((a)<(b)?(a):(b))
#define C_ABS(a, b) ((a)<(b)?(b)-(a):(a)-(b))

template<typename T1, typename T2>
inline void S_MAX(T1 &a, T2 b) { a = C_MAX(a, b); };

template<typename T1, typename T2>
inline void S_MIN(T1 &a, T2 b) { a = C_MIN(a, b); };


//container util
//------------------------------------------
#define ALL(a)  (a).begin(),(a).end()
#define RALL(a) (a).rbegin(), (a).rend()
#define SZ(a) int((a).size())
#define EACH(i, c) for(typeof((c).begin()) i=(c).begin(); i!=(c).end(); ++i)
#define EXIST(s, e) ((s).find(e)!=(s).end())
#define COUNT(obj, v) count((obj).begin(), (obj).end(), v)
#define SEARCH(v, w) search((v).begin(), (v).end(), (w).begin(), (w).end())
#define B_SEARCH(obj, v) binary_search((obj).begin(), (obj).end(), v)
#define SORT(c) sort((c).begin(),(c).end())
#define RSORT(c) sort((c).rbegin(),(c).rend())
#define REVERSE(c) reverse((c).begin(), (c).end())
#define SUMI(obj) accumulate((obj).begin(), (obj).end(), 0)
#define SUMD(obj) accumulate((obj).begin(), (obj).end(), 0.)
#define SUMLL(obj) accumulate((obj).begin(), (obj).end(), 0LL)
#define SUMS(obj) accumulate((obj).begin(), (obj).end(), string())
#define UB(obj, n) upper_bound((obj).begin(), (obj).end(), n)
#define LB(obj, n) upper_bound((obj).begin(), (obj).end(), n)
#define PB push_back
#define MP make_pair




//input output
//------------------------------------------
#define GL(s) getline(cin, (s))
#define INIT std::ios::sync_with_stdio(false);std::cin.tie(0);
#define OUT(d) std::cout<<(d);
#define OUT_L(d) std::cout<<(d)<<endl;
#define FOUT(n, data) std::cout<<std::fixed<<std::setprecision(n)<<(data);
#define FOUT_L(n, data) std::cout<<std::fixed<<std::setprecision(n)<<(data)<<"\n";
#define EL() std::cout << "\n";
#define SHOW_VECTOR(v) {std::cerr << #v << "\t:";for(const auto& xxx : v){std::cerr << xxx << " ";}std::cerr << "\n";}
#define SHOW_MAP(v) {std::cerr << #v << endl; for(const auto& xxx: v){std::cerr << xxx.first << " " << xxx.second << "\n";}}


//repetition
//------------------------------------------
#define FOR(i, a, b) for(int i=(a);i<(b);++i)
#define RFOR(i, a, b) for(int i=(b)-1;i>=(a);--i)
#define REP(i, n)  FOR(i,0,n)
#define RREP(i, n) for(int i = n-1;i >= 0;i--)
#define FORLL(i, a, b) for(LL i=LL(a);i<LL(b);++i)
#define RFORLL(i, a, b) for(LL i=LL(b)-1;i>=LL(a);--i)
#define REPLL(i, n) for(LL i=0;i<LL(n);++i)
#define RREPLL(i, n) for(LL i=LL(n)-1;i>=0;--i)
#define FOREACH(x, v) for(auto &(x) : (v))
#define FORITER(x, v) for(auto (x) = (v).begin(); (x) != (v).end(); ++(x))


//constant
//--------------------------------------------
const double EPS = 1e-10;
const double PI = acos(-1.0);
const int MOD = 1000000007;
//const int dx[] = {-1, 0, 1, 0};
//const int dy[] = {0, 1, 0, -1};


//math
//--------------------------------------------

//min <= aim <= max
template<typename T>
inline bool BETWEEN(const T aim, const T min, const T max) {
    if (min <= aim && aim <= max) {
        return true;
    } else {
        return false;
    }
}


template<class T>
inline T SQR(const T x) { return x * x; }

template<class T1, class T2>
inline T1 POW(const T1 x, const T2 y) {
    if (!y)return 1;
    else if ((y & 1) == 0) {
        return SQR(POW(x, y >> 1));
    } else return POW(x, y ^ 1) * x;
}


template<typename T>
constexpr T ABS(T x) {
    return x < 0 ? -x : x;
}

//partial_permutation nPr 順列
//first・・最初の数
//middle・・r(取り出す数)
//last・・n(全体数)
template<class Iter>
bool next_partial_permutation(Iter first, Iter middle, Iter last) {
    reverse(middle, last);
    return next_permutation(first, last);
}

//combination nCr 組み合わせ
//first1・・最初の数
//last1==first2・・r(取り出す数)
//last2・・n(全体数)
template<class Iter>
bool next_combination(Iter first1, Iter last1, Iter first2,
                      Iter last2) {
    if ((first1 == last1) || (first2 == last2)) {
        return false;
    }
    Iter m1 = last1;
    Iter m2 = last2;
    --m2;
    while (--m1 != first1 && !(*m1 < *m2)) {
    }
    bool result = (m1 == first1) && !(*first1 < *m2);
    if (!result) {
        while (first2 != m2 && !(*m1 < *first2)) {
            ++first2;
        }
        first1 = m1;
        std::iter_swap(first1, first2);
        ++first1;
        ++first2;
    }
    if ((first1 != last1) && (first2 != last2)) {
        m1 = last1;
        m2 = first2;
        while ((m1 != first1) && (m2 != last2)) {
            std::iter_swap(--m1, m2);
            ++m2;
        }
        std::reverse(first1, m1);
        std::reverse(first1, last1);
        std::reverse(m2, last2);
        std::reverse(first2, last2);
    }
    return !result;
}


//numeric_law
//--------------------------------------------

template<typename T>
constexpr bool ODD(T x) {
    return x % 2 != 0;
}

template<typename T>
constexpr bool EVEN(T x) {
    return x % 2 == 0;
}

//最大公約数
template<class T>
inline T GCD(const T x, const T y) {
    if (x < 0)return GCD(-x, y);
    if (y < 0)return GCD(x, -y);
    return (!y) ? x : GCD(y, x % y);
}

//最小公倍数
template<class T>
inline T LCM(const T x, const T y) {
    if (x < 0)return LCM(-x, y);
    if (y < 0)return LCM(x, -y);
    return x * (y / GCD(x, y));
}

//ax + by = 1
//x,yが変数に格納される
template<class T>
inline T EXTGCD(const T a, const T b, T &x, T &y) {
    if (a < 0) {
        T d = EXTGCD(-a, b, x, y);
        x = -x;
        return d;
    }
    if (b < 0) {
        T d = EXTGCD(a, -b, x, y);
        y = -y;
        return d;
    }
    if (!b) {
        x = 1;
        y = 0;
        return a;
    } else {
        T d = EXTGCD(b, a % b, x, y);
        T t = x;
        x = y;
        y = t - (a / b) * y;
        return d;
    }
}

//素数
template<class T>
inline bool ISPRIME(const T x) {
    if (x <= 1)return false;
    for (T i = 2; SQR(i) <= x; i++)if (x % i == 0)return false;
    return true;
}

//素数をtrueとして返す
template<class T>
VB ERATOSTHENES(const T n) {
    VB arr(n, true);
    for (int i = 2; SQR(i) < n; i++) {
        if (arr[i]) {
            for (int j = 0; i * (j + 2) < n; j++) {
                arr[i * (j + 2)] = false;
            }
        }
    }
    return arr;
}

// a <= x < b の素数を返す
template<typename T>
VB ERATOSTHENES(const T a, const T b) {
    VB small = ERATOSTHENES(b);
    VB prime(b - a, true);

    for (int i = 2; (T) (SQR(i)) < b; i++) {
        if (small[i]) {
            for (T j = max(2, (a + i - 1) / i) * i; j < b; j += i) {
                prime[j - a] = false;
            }
        }
    }

    return prime;
}

//nの約数
template<typename T>
vector<T> DIVISOR(T n) {
    vector<T> v;
    for (int i = 1; i * i <= n; ++i) {
        if (n % i == 0) {
            v.push_back(i);
            if (i != n / i) {
                v.push_back(n / i);
            }
        }
    }
    sort(v.begin(), v.end());
    return v;
}

//nまでのすべての約数
template<typename T>
vector<vector<T>> DIVISOR_ALL(T n) {
    vector<vector<T>> res(n + 1);
    for (int i = 1; i <= n; i++) {
        for (int j = i; j <= n; j += i) {
            res[j].push_back(i);
        }
    }
    return res;
}

//組み合わせ個数
template<typename T>
T NCR(T n, T r) {
    T ans = 1;
    REPLL(i, r) {
        ans = ans * (n - i) / (i + 1);
    }
    return ans;
}


//confirmation
//--------------------------------------------

//clear memory
#define CLR(arr, d) memset((arr), (d),sizeof(arr))

//debug
#define dump(x)  cerr << #x << " = " << (x) << endl;
#define debug(x) cerr << #x << " = " << (x) << " (L" << __LINE__ << ")" << " " << __FILE__ << endl;


/*
 *
 *
 *   ~~~~Below My Answer~~~~
 *
 *
 **/


int main() {

    int N;
    cin >> N;

    string a, b;
    cin >> a >> b;

    int count = 0;

    //   if (N % 2 == 0) {
    for (int i = 0; i < N / 2; i++) {
        //一致してたら
        if (a[i] == b[i] && a[N - i - 1] == b[N - i - 1]) continue;

        //アルファベットの数が2 2なら
        map<char, int> M;
        M[a[i]]++, M[b[i]]++, M[a[N - i - 1]]++, M[b[N - i - 1]]++;
        if (M.size() == 2) {
            bool good = true;
            FOREACH(x, M) {
                if (x.second % 2 == 1) good = false;
            }
            if (!good) count++;
            continue;
        }

        if (M.size() == 3) {
            if (a[i] == a[N - i - 1]) count += 2;
            else count += 1;
            continue;
        }

        if (M.size() == 4) {
            count += 2;
        }

    }
    // }

    if (N % 2 == 1) {
        if(a[N/2]!= b[N/2]) count++;
    }


    cout << count << endl;
    return 0;
};
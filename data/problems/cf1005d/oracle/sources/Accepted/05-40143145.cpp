#include <bits/stdc++.h>
#include <fstream>

#define endl "\n"
#define pb push_back
#define mp make_pair
#define fs first
#define sc second
#define all(x) (x).begin(),(x).end()
#define rect return 0
#define pause cout << endl; system("pause")
#define FAST ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
#define sz(x) (int)(x).size()
#define Pi acos(-1.0)
#define bitcount __builtin_popcountll

#define TupleGet(name, index) std::get<(index)>(name)
#define FOR(a, b, c) for(int (a) = (b); (a) < (c); ++(a))
#define FORs(a, b, c) for(int (a) = (b); (a) <= (c); ++(a))
#define revFOR(a, b, c) for(int (a) = (b); (a) > (c); --(a))
#define revFORs(a, b, c) for(int (a) = (b); (a) >= (c); --(a))
#define foreach(it, a) for(auto it = (a).begin(); it != (a).end(); it++)

using namespace std;

// *** TYPEDEF'S, CONSTANTS AND FUNCTIONS *** //
typedef long long ll;
typedef unsigned long long ull;
typedef long double ld;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef vector<pair<int, int>> vpii;
typedef pair<int, int> pii;
typedef pair<ll, ll> pll;
typedef tuple<int, int, int> tii;
typedef vector<vector<int> > vvi;

/* |T| |I| |P| |S|
@ string abc = "abcdefghijklmnopqrstuvwxyz";
@ 'char' - 'a' ::: порядковый номер латинской буквы
@ 'digit' - '0' or 'digit' - 48 ::: (char) ---> (int)
@ 'A' = dec 65 'Z' = dec 90
  'a' = dec 97 'z' = dec 122
  '0' = dec 48 '9' = dec 57
@ Если страдает скорость ввода:
1) ios::sync_with_stdio(0);
   cin.tie(0);
2) юзать сканф
@ для стринга перевод i-того символа в другой регистр: a[i] = char (a[i] +- 32)  :::  32 == 'a' - 'A'
@ int n (m знаков) :::  n[1] = n / 10^(m-1) ; n[m] = n % 10 ; n[m-1] = (n % 100)/10 ; n[m-2] = (n % 1000)/100...
@ cout << fixed << setprecision(n) ::: n знаков после запятой, без "fixed" - всего n знаков
@ abs(x-y) < EPS ::: равентсво вещественных чисел x и y по точности EPS
@ x + EPS < y  или  x - EPS < y ::: сравнение больше-меньше для вещественных чисел по точности EPS
@ если цифру можешь записать из головы - так и пиши в программе, иначе - пиши ФОРМУЛУ
@ «экспонента» - целое число, показывающее, на сколько надо сдвинуть десятичную запятую в числе ::: 123e2 = 12300 , 123e-4 = 0.0123
@ если задача плохо решается при нумерации с единицы, иногда оказывается намного проще перейти к нумерации с нуля.
  Особенно задачах, где явно надо делить на равные части.
@ while(cin >>)  |||  while (getline(cin, )) ::: считывание, пока даются данные
@ ctrl+Z ::: конец файла в консоли
@ Глобальные массивы, чтобы не было ошибок; размер брать с запасом
@ Количество цифр N числа X в b-ичной записи, N = floor[ log[b](X) ] + 1
@ ios::sync_with_stdio(0); //ввод
@ cin.tie(0); cout.tie(0); //могут быть проблемы в интерактивных задачах (частый ввод-вывод)
*/

void A() {
    int n;
    cin >> n;

    vi a(n);
    FOR(i, 0, n)cin >> a[i];

    int c = 0;
    FOR(i, 0, n) if (a[i] == 1) c++;

    cout << c << endl;

    vi ans;
    int prev = 0;
    FOR(i, 1, n) {
        if (a[i] == 1) {
            ans.pb(i - prev);
            prev = i;
        }
    }

    FOR(i, 0, sz(ans))cout << ans[i] << " ";
    cout << n - prev;
}

void B() {
    string s, t;
    cin >> s >> t;

    int com = 0;

    if (sz(s) < sz(t)) {
        swap(s, t);
    }
    int d = sz(s) - sz(t);

    int i = sz(s) - 1, j = i - d;
    while (s[i] == t[j] && i >= 0 && j >= 0) {
        com++;
        i--;
        j--;
    }

    cout << sz(s) + sz(t) - com - com;
}

void C() {
    ll n;
    cin >> n;
    vll a(n);
    FOR(i, 0, n)cin >> a[i];

    multiset<ll> s;
    FOR(i, 0, n)s.insert(a[i]);

    int ans = 0;
    FOR(i, 0, n) {
        s.erase(s.find(a[i]));
        bool ok = false;
        for (ll d = 0; d <= 31; d++) {
            ll val = (1LL << d) - a[i];
            if (s.find(val) != s.end()) {
                ok = true;
            }
        }
        if (!ok) ans++;
        if (ok) s.insert(a[i]);
    }

    cout << ans;
}

void D() {
    string s;
    cin >> s;

    vi a(sz(s));
    FOR(i,0,sz(s)) {
        a[i] = (s[i] - '0');
    }

    multiset<ll> ms;

    ll sum = 0, ans = 0;
    FOR(i, 0, sz(a)) {
        if (a[i] % 3 == 0) {
            ans++;
            sum = 0;
            ms.clear();
        } else {
            sum += a[i];
            if (ms.find(sum % 3) != ms.end()) {
                ans++;
                sum = 0;
                ms.clear();
            } else {
                if (sum % 3 == 0) {
                    ans++;
                    sum = 0;
                    ms.clear();
                } else {
                    ms.insert(sum % 3);
                }
            }
        }
    }
    cout << ans;
}


int main() {
    D();
    return 0;
}
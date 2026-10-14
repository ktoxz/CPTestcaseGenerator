#define _CRT_SECURE_NO_DEPRECATE

#define _USE_MATH_DEFINES

#include <iostream>

#include <cmath>

#include <string>

#include <vector>

#include <algorithm>

#include <cstdio>

#include <memory.h>

#include <set>

#include <ctime>

#include <map>

#include <cstring>

#include <iterator>

#include <queue>

#include <assert.h>

#include <unordered_map>

#include <unordered_set>

#include <bitset>



using namespace std;







#define pb push_back

#define pii pair<int, int>

#define mp make_pair

#define ull unsigned long long

#pragma comment(linker, "/STACK:64000000")



typedef long double ld;

typedef pair<ld, ld> pldld;

typedef long long ll;

typedef pair<ll, ll> pll;





typedef unsigned int ui;

typedef unsigned char uc;

const int infi = 1e9 + 7;

const ll infl = 1e18;









/** Interface */



inline int readChar();

inline void writeChar( int x ); 

inline void writeWord( const char *s );

inline void flush();



/** Read */



static const int buf_size = 4096;



inline int getChar() {

  static char buf[buf_size];

  static int len = 0, pos = 0;

  if (pos == len)

    pos = 0, len = fread(buf, 1, buf_size, stdin);

  if (pos == len)

    return -1;

  return buf[pos++];

}



inline int readChar() {

  int c = getChar();

  while (c >= 0 && c <= 32)

    c = getChar();

  return c;

}

//char bf[10];

inline int readWord(char *bf) {

	char *cur = bf;

	*cur = getChar();

	

  while (*cur <= 32)

    *cur = getChar();

  while (*cur > 32) {

	++cur;

	*cur = getChar();

  }

  return cur - bf;

}



inline int readInt() {

  int s = 1, c = readChar();

  int x = 0;

  if (c == '-')

    s = -1, c = getChar();

  while ('0' <= c && c <= '9')

    x = x * 10 + c - '0', c = getChar();

  return s == 1 ? x : -x;

}



/** Write */



static int write_pos = 0;

static char write_buf[buf_size];



inline void writeChar( int x ) {

  if (write_pos == buf_size)

    fwrite(write_buf, 1, buf_size, stdout), write_pos = 0;

  write_buf[write_pos++] = x;

} 



inline void flush() {

  if (write_pos)

    fwrite(write_buf, 1, write_pos, stdout), write_pos = 0;

}



inline void writeInt(ll x ) {

  if (x < 0)

    writeChar('-'), x = -x;



  char s[24];

  int n = 0;

  while (x || !n)

    s[n++] = '0' + x % 10, x /= 10;

  while (n--)

    writeChar(s[n]);

}



inline void writeWord( const char *s ) {

  while (*s)

    writeChar(*s++);

}



inline void add(vector <int> &a, int n) {

	for (int i = 1; i <= n; ++i)

		a.push_back(i);

}

int ar[1010];



int main() {

	//ios_base::sync_with_stdio(0);

//	cin.sync_with_stdio(false);

	//cin.tie(0);

	//freopen("input.txt", "r", stdin);freopen("output.txt", "w", stdout);

	//freopen("partition.in", "r", stdin);freopen("partition.out", "w", stdout);

	int n, m, h;

	cin >> n >> m >> h;

	int s = 0;

	--h;

	for (int i = 0; i < m; ++i) {

		cin >> ar[i];

		s += ar[i];

	}

	--s, --n, --ar[h];

	if (s < n) {

		cout << -1;

		return 0;

	}

	if (s - ar[h] < n) {

		cout << 1;

		return 0;

	}

	vector <int> zm, ch;

	add(ch, s - ar[h]);

	add(ch, s - n);

	add(zm, s);

	add(zm, s - ar[h] - n);

	double ans = 1;

	while (ch.size() || zm.size()) {

		if (ch.empty()) {

			ans /= (double)zm.back();

			zm.pop_back();

			continue;

		}

		if (zm.empty()) {

			ans *= (double)ch.back();

			ch.pop_back();

			continue;

		}

		if (ans > 1.0) {

			ans /= (double)zm.back();

			zm.pop_back();

		}

		else {

			ans *= (double)ch.back();

			ch.pop_back();

		}

	}

	cout.precision(20);

	cout << fixed;

	cout << 1.0 - ans;

	//flush();

	return 0;

}
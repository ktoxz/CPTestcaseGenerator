#pragma warning( disable : 4786 )
#include <string>
#include <vector>
#include <list>
#include <map>
#include <set>
#include <stack>
#include <bitset>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <cassert>
#include <queue>
#include <cstring>
using namespace std;

#ifdef _MSC_VER
	typedef __int64 i64;
	typedef unsigned __int64 u64;
	#define I64 "%I64d"
	#define U64 "%I64u"

	std::ostream& operator<<(std::ostream& os, __int64 i ){
		char buf[40];
		sprintf(buf,"%I64d", i );
		os<<buf;
		return os;
	}
	std::istream& operator>>(std::istream& ist, __int64 &i ){
		scanf ("%I64d",&i);
		return ist;
    	}

#else
	typedef long long i64;
	#define I64 "%lld"
	typedef unsigned long long u64;
	#define U64 "%llu"
#endif



#define sq(x) ((x)*(x))

#define EPS 1e-7

#define eq(a,b) (a - b < EPS && b - a < EPS) 
#define les(a, b) (b - a > EPS) 

typedef vector<int> VI; 

#define rep(i,n) for((i)=0;(i)<(n);++(i))

#define all(c) (c).begin(),(c).end() 
#define tr(c,i) for(typeof((c).begin() i = (c).begin(); i != (c).end(); i++) 
#define present(c,x) ((c).find(x) != (c).end()) 
#define cpresent(c,x) (find(all(c),c) != (c).end()) 

#define FOR(v, it) for(it = v.begin(); it!=v.end(); ++it)
#define foreach(vtype, v, it) for(vtype::iterator it = v.begin(); it!=v.end(); ++it)

// tostring
string itos (int i){ stringstream s; s << i; return s.str(); }
string i64tos (i64 i){ char s[51];sprintf(s,I64,i);string ss=s;return ss; }


#define dbg(x) if(DEBUG) cerr << __LINE__ << ": " << #x << " -> " << (x) << "\t";
#define dbge(x) if(DEBUG) cerr << __LINE__ << ": "<<#x << " -> " << (x) << endl;

#define CLR(c, v) memset(c, v, sizeof(c))

vector<string> Tokenize(string s, string ch) {
  vector<string> ret;
  for (int p = 0, p2; p < s.size(); p = p2+1) {
    p2 = s.find_first_of(ch, p);
    if (p2 == -1) p2 = s.size();
    if (p2-p > 0) ret.push_back(s.substr(p, p2-p));
  }
  return ret;
}

vector<int> TokenizeInt(string s, string ch) {
  vector<int> ret;
  vector<string> p = Tokenize(s, ch);
  for( int i = 0; i < p.size(); i++ )
    ret.push_back(atoi(p[i].c_str()));
  return ret;
}

vector<vector<int> > TokenizeMatrix(vector<string> s, string ch) {
  vector<vector<int> > ret;
  for( int i = 0; i < s.size(); i++ )
    ret.push_back( TokenizeInt(s[i], ch) );
  return ret;
}

int parseInts(char buff[], int a[]){
	int n = 0;
    char *p = strtok(buff," ");
    while(p!=NULL){
        sscanf(p,"%d",&a[n++]);
        p = strtok(NULL," ");
    }
	return n;
}

int getInt(void){
	int d;
	scanf("%d",&d);
	return d;
}
#define INT getInt()

double getDouble(void){
    double d;
    scanf("%lf", &d);
    return d;
}
#define DOUB getDouble()


bool DEBUG = true;

////////////////////////////////////////////////////////////////////////////////////////////////////////////
// END OF PREWRITTEN CODES 
////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define mmin(a, b) ((a)<(b)?(a):(b))
#define mmax(a, b) ((a)>(b)?(a):(b))

int L[200], R[200];
#define INF 1000000

int cost(int r, int c, int l, int mid){
	int ret = 0;
	ret += abs(mid - r) * l;

	if (c > mid){
		ret += (l * (l - 1)) / 2 + l * (c - mid);
	}
	else if (c + l - 1 < mid){
		ret += (l * (l - 1)) / 2 + l * (mid - (c + l - 1));
	}
	else{
		int d = mid - c;
		ret += (d * (d + 1)) / 2;
		d = c + l - 1 - mid;
		ret += (d * (d + 1)) / 2;
	}

	return ret;
}

int main (void){
	//freopen("input.txt", "r", stdin);
	int i;
	int N = INT;
	int K = INT;
	memset(L, -1, sizeof(L));
	memset(R, -1, sizeof(R));

	int MID = (K + 1) / 2;


	while(N--){
		int M = INT;
		int dist = INF;
		int r = -1;
		int c = -1;

		for(i = 1; i <= K; ++i){
			if (L[i] == -1){ // mid
				int r1 = i;
				int c1 = MID - (M / 2);

				int d1 = cost(r1, c1, M, MID);

				if (d1 < dist){
					dist = d1;
					r = r1;
					c = c1;
				}
			}
			else{
				// try left
				int r1 = i;
				int c1 = L[i] - M;
				if (c1 >= 1){
					int d1 = cost(r1, c1, M, MID);

					if (d1 < dist){
						dist = d1;
						r = r1;
						c = c1;
					}
				}
				

				// try right
				r1 = i;
				c1 = R[i] + 1;
				if (c1 + M - 1 <= K){
					int d1 = cost(r1, c1, M, MID);

					if (d1 < dist){
						dist = d1;
						r = r1;
						c = c1;
					}
				}
			}
		}

		if (dist < INF){
			cout<<r<<" "<<c<<" "<<c + M - 1<<endl;
			if (L[r] == -1){
				L[r] = c;
			}
			else {
				L[r] = mmin(L[r], c);
			}

			if (R[r] == -1){
				R[r] = c + M - 1;
			}
			else {
				R[r] = mmax(R[r], c + M - 1);
			}
		}
		else{
			cout<<-1<<endl;
		}
	}

	return 0;
}
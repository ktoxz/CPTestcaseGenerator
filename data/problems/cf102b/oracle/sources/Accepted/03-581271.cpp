#include <iostream> 
#include <algorithm> 
#include <vector> 
#include <cstdio> 
#include <string> 
#include <bitset> 
#include <cmath> 
#include <list> 
#include <cstdlib> 
#include <map> 
#include <cstring> 
#include <set> 
#include <stack> 
#include <sstream> 
#include <queue> 
#include <deque> 
#include <ctime> 

using namespace std; 

#define debug(x) cout<<#x<<" = "<<x<<"\n" 
#define REP(i,n) for(int (i)=0;(i)<(n);(i)++) 
#define PI 3.1415926535897932385 
#define INF (1<<29) 
#define EPS (1e-7) 
#define pb push_back 
#define sz size() 
#define ln length() 
#define mp make_pair 
#define all(a) a.begin(),a.end() 
#define fill(ar,val) memset(ar,val,sizeof ar) 
#define sqr(x) ((x)*(x)) 
#define min(a,b) ((a)<(b)?(a):(b)) 
#define max(a,b) ((a)>(b)?(a):(b)) 
#define FORE(c,itr) for(__typeof((c).begin()) itr=(c).begin();itr!=(c).end();itr++) 

typedef long long LL; 
typedef long double LD; 
typedef vector<int> VI; 
long sumdg( long n ) {
	long sum = 0;
	int d;
	while ( n > 0 ) {
		d = n % 10;
		sum += d;
		n /= 10;
	}
	
	return sum;
}

int main()
{
	long n = 0;
	string s;
	cin >> s;
	
	if ( s.size() == 1 ) {
		cout << "0";
		return 0;
	}
	
	int siz = s.size();
	int spells = 1;
	
	REP(i,siz) {
		n += (s[i]-'0');
	}
	//debug(n);
	while ( n >= 10 ) {
		spells++;
		n = sumdg(n);
		//debug(n);
	}
	
	cout << spells;
	return 0;
	}
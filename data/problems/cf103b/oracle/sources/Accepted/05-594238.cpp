/* .................................................................................................................................. */

/** Header **/

#include <iostream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <cstdio>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <bitset>
#include <list>
#include <set>
#include <map>

using namespace std;

/** Repeat **/

#define REP(I, N) for (int I=0;I<int(N);++I)
#define FOR(I, A, B) for (int I=int(A);I<int(B);++I)
#define DWN(I, B, A) for (int I=int(B-1);I>=int(A);--I)
#define REP_1(I, N) for (int I=1;I<=int(N);++I)
#define FOR_1(I, A, B) for (int I=int(A);I<=int(B);++I)
#define DWN_1(I, B, A) for (int I=int(B);I>=int(A);--I)
#define REP_C(I, N) for (int N____=int(N),I=0;I<N____;++I)
#define FOR_C(I, A, B) for (int B____=int(B),I=A;I<B____;++I)
#define DWN_C(I, B, A) for (int A____=int(A),I=B-1;I>=A____;--I)
#define REP_1_C(I, N) for (int N____=int(N),I=1;I<=N____;++I)
#define FOR_1_C(I, A, B) for (int B____=int(B),I=A;I<=B____;++I)
#define DWN_1_C(I, B, A) for (int A____=int(A),I=B;I>=A____;--I)
#define DO(N) while(N--)
#define DO_C(N) int N____ = N; while(N____--)
#define TO(i, a, b) int s_=a<b?1:-1,b_=b+s_;for(int i=a;i!=b_;i+=s_)
#define TO_1(i, a, b) int s_=a<b?1:-1,b_=b;for(int i=a;i!=b_;i+=s_)
#define SQZ(I, J, A, B) for (int I=int(A),J=int(B)-1;I<J;++I,--J)
#define SQZ_1(I, J, A, B) for (int I=int(A),J=int(B);I<=J;++I,--J)

#define For_each(IT, A) for(list<Seg>::iterator IT = begin(); IT != A.end(); ++IT)

/** Macro **/

#define ALL(A) A.begin(), A.end()
#define CLR(A) A.clear()
#define CPY(A, B) memcpy(A, B, sizeof(A))
#define INS(A, P, B) A.insert(A.begin() + P, B)
#define ERS(A, P) A.erase(A.begin() + P)
#define SRT(A) sort(ALL(A))
#define BSC(A, X) find(ALL(A), X) // != A.end()
#define SZ(A) int(A.size())
#define PB push_back
#define MP(A, B) make_pair(A, B)

#define Rush int T____; RD(T____); DO(T____)
#pragma comment(linker, "/STACK:36777216")
#define Ruby system("ruby main.rb")
#define Haskell system("runghc main.hs")
#define Pascal system("fpc main.pas")

/** Typedef **/

typedef long long LL;
typedef double DB;

typedef vector<int> VI;
typedef vector<string> VS;
typedef vector<LL> VL;
typedef vector<DB> VD;
typedef set<int> SI;
typedef set<string> SS;
typedef set<LL> SL;
typedef set<DB> SD;
typedef map<int, int> MII;
typedef map<string, int> MSI;
typedef map<LL, int> MLI;
typedef map<DB, int> MDI;
typedef pair<int, int> PII;
typedef pair<int, bool> PIB;

/* ... :" We are I/O Accelerator ... Use us at your own risk ;) ... " .. */

template<class T> inline void RD(T &x){
    cin >> x;
    //scanf("%d", &x);
    //char c; for (c = getchar(); c < '0'; c = getchar()); x = c - '0'; for (c = getchar(); c >= '0'; c = getchar()) x = x * 10 + c - '0';
    //char c; c = getchar(); x = c - '0'; for (c = getchar(); c >= '0'; c = getchar()) x = x * 10 + c - '0';

}

template<class T> inline void OT(T &x){
    cout << x;
    //printf("%d", &x);
}

inline int RD(){ int x; RD(x); return x;}
template<class T0, class T1> inline void RD(T0 &x0, T1 &x1){RD(x0), RD(x1);}
template<class T0, class T1, class T2> inline void RD(T0 &x0, T1 &x1, T2 &x2){RD(x0), RD(x1), RD(x2);}
template<class T0, class T1, class T2, class T3> inline void RD(T0 &x0, T1 &x1, T2 &x2, T3 &x3){RD(x0), RD(x1), RD(x2), RD(x3);}
template<class T0, class T1, class T2, class T3, class T4> inline void RD(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4){RD(x0), RD(x1), RD(x2), RD(x3), RD(x4);}
template<class T0, class T1, class T2, class T3, class T4, class T5> inline void RD(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4, T5 &x5){RD(x0), RD(x1), RD(x2), RD(x3), RD(x4), RD(x5);}
template<class T0, class T1, class T2, class T3, class T4, class T5, class T6> inline void RD(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4, T5 &x5, T6 &x6){RD(x0), RD(x1), RD(x2), RD(x3), RD(x4), RD(x5), RD(x6);}
template<class T0, class T1> inline void OT(T0 &x0, T1 &x1){OT(x0), OT(x1);}
template<class T0, class T1, class T2> inline void OT(T0 &x0, T1 &x1, T2 &x2){OT(x0), OT(x1), OT(x2);}
template<class T0, class T1, class T2, class T3> inline void OT(T0 &x0, T1 &x1, T2 &x2, T3 &x3){OT(x0), OT(x1), OT(x2), OT(x3);}
template<class T0, class T1, class T2, class T3, class T4> inline void OT(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4){OT(x0), OT(x1), OT(x2), OT(x3), OT(x4);}
template<class T0, class T1, class T2, class T3, class T4, class T5> inline void OT(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4, T5 &x5){OT(x0), OT(x1), OT(x2), OT(x3), OT(x4), OT(x5);}
template<class T0, class T1, class T2, class T3, class T4, class T5, class T6> inline void OT(T0 &x0, T1 &x1, T2 &x2, T3 &x3, T4 &x4, T5 &x5, T6 &x6){OT(x0), OT(x1), OT(x2), OT(x3), OT(x4), OT(x5), OT(x6);}


template<class T> inline void RST(T &A){memset(A, 0, sizeof(A));}
template<class T0, class T1> inline void RST(T0 &A0, T1 &A1){RST(A0), RST(A1);}
template<class T0, class T1, class T2> inline void RST(T0 &A0, T1 &A1, T2 &A2){RST(A0), RST(A1), RST(A2);}
template<class T0, class T1, class T2, class T3> inline void RST(T0 &A0, T1 &A1, T2 &A2, T3 &A3){RST(A0), RST(A1), RST(A2), RST(A3);}
template<class T0, class T1, class T2, class T3, class T4> inline void RST(T0 &A0, T1 &A1, T2 &A2, T3 &A3, T4 &A4){RST(A0), RST(A1), RST(A2), RST(A3), RST(A4);}
template<class T0, class T1, class T2, class T3, class T4, class T5> inline void RST(T0 &A0, T1 &A1, T2 &A2, T3 &A3, T4 &A4, T5 &A5){RST(A0), RST(A1), RST(A2), RST(A3), RST(A4), RST(A5);}

//#

template<class T> inline void FLC(T &A, int x){memset(A, x, sizeof(A));}
template<class T0, class T1> inline void FLC(T0 &A0, T1 &A1, int x){FLC(A0, x), FLC(A1, x);}
template<class T> inline void FLC(T &A0, T &A1, T &A2, int x){FLC(A0, x), FLC(A1, x), FLC(A2, x);}
template<class T> inline void FLC(T &A0, T &A1, T &A2, T &A3, int x){FLC(A0, x), FLC(A1, x), FLC(A2, x), FLC(A3, x);}
template<class T> inline void FLC(T &A0, T &A1, T &A2, T &A3, T &A4, int x){FLC(A0, x), FLC(A1, x), FLC(A2, x), FLC(A3, x), FLC(A4, x);}
template<class T> inline void FLC(T &A0, T &A1, T &A2, T &A3, T &A4, T &A5, int x){FLC(A0, x), FLC(A1, x), FLC(A2, x), FLC(A3, x), FLC(A4, x), FLC(A5, x);}

//#

template<class T> inline void checkMin(T &a, T b){if (b<a) a=b;}
template<class T> inline void checkMax(T &a, T b){if (b>a) a=b;}

/* .................................................................................................................................. */

const int MOD = 1000000007;
const int INF = 0x7fffffff;
const int N = 100;


const int gray = 1, white = 0, black = 2;
bool G[N][N]; int Color[N];
int n, m; int cir;

void dfs(int u = 0, int p = -1){

//    cout << u << endl;

    Color[u] = gray;

    REP(v, n) if (G[u][v] && v != p) {

//        cout << " " << v << " " << cir << endl;

        if (Color[v] == gray) ++cir;
        if (Color[v] == white) dfs(v, u);

    }



    Color[u] = black;

}

bool check(){

    dfs();

    //cout << cir << endl;

    if (cir != 1) return false;

    REP(k, n) REP(i, n) REP(j, n)
    G[i][j] = G[i][j] || G[i][k] && G[k][j];


    REP(i, n) REP(j, n) if (i != j){
        if (!G[i][j]) return false;
    }

    return true;
}



int main(){
  //  freopen("B.in", "r", stdin);



    RD(n, m);
    REP(i, m){
        int a, b; RD(a, b); --a, --b;
        //cout << a << ' ' << b << endl;
        G[a][b] = G[b][a] = true;
    }


    cout << (check() ?  "FHTAGN!" : "NO") << endl;

}
#include <cstdio>
#include <algorithm>
#include <cmath>
using namespace std;

#define REP(i,n) for(int i=0,_n=(n);i<_n;++i)
#define FOR(i,a,b) for(int i=(a),_b=(b);i<=_b;++i)
#define MP make_pair

typedef pair<int,int > PII; 
const int INF = 1000000000;
inline int getint() { int x; scanf("%d",&x); return x; }

// Powered By TimoAI 2.2


int used[128][128];
int value[128][128][128];
const PII impossible = MP(-1,-1);

PII solve(int M,int K) {
    PII ret = MP(-1,-1);
    int best = INF;
    FOR(x,1,K) {
        int kosong = 0;
        FOR(y,1,K) {
            if(used[x][y]) {
                kosong = 0;
                continue;
            }else kosong++;
            if(kosong >= M) {
                int yfrom = y - M + 1;
                int v = value[x][yfrom][y];
                if(v < best) {
                    best = v;
                    ret = MP(x,yfrom);
                }
            }
        }
    }

    if(ret!=impossible) {

        int x = ret.first;
        int y = ret.second;
        REP(i,M) {
            used[x][y+i] = 1;
        }
    }

    return ret;
}

int main() {
    int N = getint();
    int K = getint();

    int xc = (K + 1) / 2;
    int yc = (K + 1) / 2;
    FOR(x,1,K) {
        FOR(y,1,K) {
            int sum = 0;
            FOR(z,y,K) {
                sum += abs(x - xc) + abs(z - yc);
                value[x][y][z] = sum;
            }
        }
    }

    REP(i,N) {
        int M = getint();
        PII ans = solve(M, K);
        if(ans==impossible) puts("-1");
        else printf("%d %d %d\n",ans.first, ans.second, ans.second+M-1);
    }
    return 0;
}
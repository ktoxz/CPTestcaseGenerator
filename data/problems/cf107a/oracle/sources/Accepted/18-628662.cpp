#include <stdio.h>
#include <memory.h>
#include <algorithm>
#include <vector>
#include <set>
using namespace std;

#define PI 3.141592653589793
#define INF 2123456789
#define NUL 0.0000001

#define PB push_back
#define SZ size()
#define CLR clear()
#define INS insert
#define EMP empty()

int a[1005], d[1005];
bool tank[1005];

int sol, solA[1005], solB[1005], solD[1005];

int main(){
    int n, p; scanf("%d%d", &n, &p);

    memset(a, 0, sizeof(a));
    memset(tank, true, sizeof(tank));
    for (int i = 1; i <= p; i++){
        int x; scanf("%d", &x);
        scanf("%d%d", &a[x], &d[x]);
        tank[ a[x] ] = false;
    }

    int sol = 0;
    for (int i = 1; i <= n; i++) if (a[i] && tank[i]){
        int p = INF, j = i;
        while (j){
            if (!d[j]) break;
            p = min(p, d[j]);
            j = a[j];
        }
        sol++; solA[sol] = i; solB[sol] = j; solD[sol] = p;
    }

    printf("%d\n", sol);
    for (int i = 1; i <= sol; i++) printf("%d %d %d\n", solA[i], solB[i], solD[i]);

    return 0;
}
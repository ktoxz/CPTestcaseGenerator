/*#include <iostream>
#include <cstdio>
#include <cstring>
#include <string>
using namespace std;

#define INF 0x7f7f7f7f
#define MAXN 200010

int a[MAXN], sum[MAXN];
int n, m, l;
int qu[2 * MAXN], head, rear;
int i;
int d[101][MAXN];

double g(int k1, int k2){
	return double(d[i - 1][k1] - d[i - 1][k2]) / (sum[k1] - sum[k2]);
}

int main(){
	int j, k;
	int T;
	int st;

	scanf("%d", &T);
	while (T--){
		scanf("%d %d %d", &n, &m, &l);
		sum[n] = 0;
		for (i = n - 1; i >= 0; i--){
			scanf("%d", &a[i]);
			sum[i] = sum[i - 1] + a[i];
		}
		memset(d, 0x7f, sizeof(d));
		st = n;
		d[0][n] = 0;
		for (i = 1; i <= m; i++, st -= l){
			head = rear = MAXN;
			qu[head--] = st;

			for (j = st - 1; i >= 0; j--){
				while (rear - head >= 2 && g(qu[rear - 1], qu[rear]) < i){
					rear--;
				}
				k = qu[rear];
				d[i][j] = d[i - 1][k] + (sum[j] - sum[k]) * i;
				while (rear - head >= 2 && g(j, qu[head + 1]) < g(qu[head + 1], qu[head + 2])){
					head++;
				}
				qu[rear--] = j;
			}
		}
		int mn = INF;
		for (i = 0; i <= m; i++){
			if (d[i][0] < mn){
				mn = d[i][0];
			}
		}
		printf("%d\n", mn);
	}
	return 0;
}
*/




/*
#include <iostream>
#include <cstring>
#include <cstdio>
using namespace std;

#define MAXN 3002

struct Node{
	int x, y;
}nod[MAXN];
int n, m;

int a[MAXN * MAXN];
int seq[MAXN * MAXN];

int main(){
	int i, j;
	int len;
	int l, r, mid, res;
	while (scanf("%d", &m) != EOF){
		for (i = 0; i < m; i++){
			scanf("%d %d", &nod[i].x, &nod[i].y);
		}
		n = 0;
		for (i = 0; i < m; i++){
			for (j = m - 1; j >= 0; j--){
				if (nod[i].x == nod[j].x && nod[i].y == nod[j].y){
					a[n++] = m - 1 - j;
				}
			}
		}
		len = 1;
		seq[0] = a[0];
		for (i = 1; i < n; i++){
			if (a[i] > seq[len - 1]){
				seq[len++] = a[i];
				continue;
			}
			l = 0, r = len - 1, res = -1;
			while (l <= r){
				mid = (l + r) >> 1;
				if (seq[mid] >= a[i]){
					res = mid;
					r = mid - 1;
				}
				else l = mid + 1;
			}
			seq[mid] = a[i];
		}
		printf("%d\n", len);



	}
	return 0;
}

*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

#define MAXN 3010

int n, m;
int d[MAXN];
int ans[MAXN];

struct Node{
	int x, y;
	int operator<(const Node &t){
		return x < t.x;
	}
	int operator==(const Node &t){
		return (x == t.x && y == t.y);
	}
}a[MAXN], b[MAXN];

void solve(int &mxlen, int &mxx){
	int i, j, k, mx;
	//memset(d[0], 0, sizeof(d[0]));
	for (i = 1; i <= n; i++) {
		mx = 0;
		for (j = 1; j <= m; j++) {
			if (i == 1)d[j] = 0;
			//else d[i][j] = d[i - 1][j];

			if (b[j] < a[i] && d[j] > d[mx])
				mx = j;//DP过程中更新mx，免去枚举求mx

			if (a[i] == b[j]) {
				if (mx == 0 || d[mx] + 1 > d[j]) {
					d[j] = d[mx] + 1;
				}
			}
		}
	}
	mx = 1;
	for (i = 2; i <= m; i++)
		if (d[i] > d[mx])
			mx = i;
	//printf("%d\n", d[n][mx]);
	mxlen = d[mx];
	if (d[mx] == 0)
		return;
	mxx = b[mx].x;
	return;
}



inline int getnum() {
	char c;
	int ret = 0;
	while (c = getchar(), c < '0' || c > '9');
	ret = c - '0';
	while (c = getchar(), c >= '0' && c <= '9')
		ret = ret * 10 + c - '0';
	return ret;
}

int main(){
	int i, j, k, mx, nn;
	int mxlen, mxx, ans;
	while (scanf("%d", &nn) != EOF){
		for (i = 1; i <= nn; i++){
			//scanf("%d %d", &a[i].x, &a[i].y);
			a[i].x = getnum();
			a[i].y = getnum();
		}
		n = nn - 1, m = 1;
		b[1] = a[nn];

		ans = 0;
		solve(mxlen, mxx);
		ans = max(ans, mxlen * 2);

		while (n - 1){
			n--;
			solve(mxlen, mxx);
			if (a[n + 1].x > mxx){
				ans = max(ans, mxlen * 2 + 1);
			}
			else ans = max(ans, mxlen * 2);

			m++;
			b[m] = a[n + 1];
			solve(mxlen, mxx);
			ans = max(ans, mxlen * 2);
		}

		printf("%d\n", ans);






	}

	return 0;
}
*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

#define MAXN 3010

int n, m;
int d[MAXN];
int ans[MAXN];

struct Node{
	int x, y;
	int operator<(const Node &t){
		return x < t.x;
	}
	int operator==(const Node &t){
		return (x == t.x && y == t.y);
	}
}a[MAXN], b[MAXN];

void solve(int &mxlen){
	int i, j, k, mx;
	mxlen = 0;
	memset(d, 0, sizeof(d));
	for (i = 1; i <= n; i++) {
		mx = 0;
		for (j = 1; j <= n - i; j++) {
			//if (i == 1)d[j] = 0;
			//else d[i][j] = d[i - 1][j];

			if (b[j] < a[i] && d[j] > d[mx])
				mx = j;//DP过程中更新mx，免去枚举求mx

			if (a[i] == b[j]) {
				if (mx == 0 || d[mx] + 1 > d[j]) {
					d[j] = d[mx] + 1;
					mxlen = max(mxlen, d[j] * 2);
				}
			}
		}
	}


}


void solve1(int &mxlen){
	int i, j, k, mx, t;
	mxlen = 0;
	memset(d, 0, sizeof(d));
	for (i = 1; i < n; i++) {
		mx = 0;
		for (j = 1; j <= n - i - 1; j++) {
			//if (i == 1)d[j] = 0;
			//else d[i][j] = d[i - 1][j];

			if (b[j] < a[i] && d[j] > d[mx])
				mx = j;//DP过程中更新mx，免去枚举求mx

			if (a[i] == b[j]) {
				if (mx == 0 || d[mx] + 1 > d[j]) {
					d[j] = d[mx] + 1;
					t = d[j];
					if (a[i + 1].x > b[j].x)
						mxlen = max(mxlen, t * 2 + 1);
					else mxlen = max(mxlen, t * 2);
				}
			}
		}
	}


}



inline int getnum() {
	char c;
	int ret = 0;
	while (c = getchar(), c < '0' || c > '9');
	ret = c - '0';
	while (c = getchar(), c >= '0' && c <= '9')
		ret = ret * 10 + c - '0';
	return ret;
}

int main(){
	int i, j, k, mx, nn;
	int mxlen, mxx, ans;
	while (scanf("%d", &nn) != EOF){
		for (i = 1; i <= nn; i++){
			//scanf("%d %d", &a[i].x, &a[i].y);
			a[i].x = getnum();
			a[i].y = getnum();
			b[nn - i + 1] = a[i];
		}
		n = nn;

		ans = 0;
		solve(mxlen);
		ans = max(ans, mxlen);
		solve1(mxlen);
		ans = max(ans, mxlen);








		if (ans == 0){
			ans++;
		}

		printf("%d\n", ans);






	}

	return 0;
}*/


/*
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <algorithm>
#include <vector>
#include <cassert>

using namespace std;
typedef long long LL;
const LL MOD = 1000000007;
char day[7][20] = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday"};
char buf[100];
LL C[20][20];
int getD(char* s){
    for(int i = 0; i < 7; i ++){
        if(strcmp(s, day[i]) == 0) return i;
    }
    assert(0);
    return -1;
}
LL mpow(LL x, LL k){
    LL ret = 1;
    while(k){
        if(k&1) ret = (ret*x)%MOD;
        k >>= 1;
        x = (x*x)%MOD;
    }
    return ret;
}
//1^x + 8^x + 15^x + ..... (0<=x<=k)
vector<LL> getA(LL x, LL num, int k){
    if(num == 0) return vector<LL>(k+1, 0LL);
    vector<LL> ret;
    if(num&1){
        ret = getA(x, num-1, k);
        LL top = 1+(num-1)*7;
        for(int i = 0; i <= k; i ++){
            ret[i] = (ret[i]+mpow(top, i))%MOD;
        }
        return ret;
    }else{
        vector<LL> tmp = getA(x, num>>1, k);
        ret = vector<LL>(k+1, 0LL);
        LL dis = (num/2*7)%MOD;
        for(int i = 0; i <= k; i ++){
            for(int j = 0; j <= i; j ++){
                ret[i] = (ret[i] + ((C[i][j]*tmp[j])%MOD*mpow(dis, i-j))%MOD)%MOD;
            }
            ret[i] += tmp[i];
        }
        return ret;
    }
}
//is Saturday or Sunday ?
bool rest[10];
int main() {
    int test, n, k, cas = 0;
    memset(C, 0, sizeof(C));
    for(int i = 0; i < 20; i ++){
        for(int j = 0; j <= i; j ++){
            C[i][j] = (i==j)?1:(C[i-1][j-1]+C[i-1][j])%MOD;
        }
    }
    scanf("%d", &test);
    while(test --){
        scanf("%s%d%d", buf, &n, &k);
        printf("Case %d: ", ++cas);
        int day = getD(buf);
        for(int i = 0; i < 7; i ++){
            int x = (i+day+6)%7;
            if(x == 5 || x == 6) rest[i] = true;
            else rest[i] = false;
        }
        LL ans = 0;
        //norm
        while(n%7 != 0){
            if(!rest[n%7]){
                ans = (ans + mpow(n, k))%MOD;
            }
            n --;
        }
        vector<LL> tmp = getA(1, n/7, k);
//        printf("n = %d\n", n);
//        for(int i = 0; i <= k; i ++) printf("i = %d tmp = %d\n", i, (int)tmp[i]);

        for(int i = 1; i <= 7; i ++){
            if(rest[i%7]) continue;
            int x = i - 1;
            for(int j = 0; j <= k; j ++){
                LL add = ((mpow(x, j)*tmp[k-j])%MOD*C[k][j])%MOD;
                ans = (ans+add)%MOD;
            }
        }
        printf("%d\n", (int)ans);
    }
    return 0;
}*/


/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
using namespace std;

const double eps = 1e-10;

int main(){
	double s, m, h, j;
	int cnt;
	int i, k;
	int x;
	int T;
	scanf("%d", &T);
	while (T--){
		cnt = 0;
		scanf("%d", &x);
		//x /= 360;
		for (i = 0; i < 43200; i++){
			k = i / 3600;
			j = i;
			h = j / 3600;
			h = h * 30;
			m = j / 60;
			m -= k * 60;
			m = m * 6;
			if (min(360 - fabs(m - h), fabs(m - h)) - eps <= x){
				cnt++;
			}
			else{
				//puts("1");
			}
		}
		printf("%d.00\n", 2 * cnt);
	}
	return 0;
}
*/
/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cmath>
using namespace std;

int main(){
	int i, j;
	double k;
	int x;
	double ans;
	int T;
	double a, b;
	scanf("%d", &T);
	while (T--){
		scanf("%d", &x);
		ans = 0;
		for (i = 0; i < 12; i++){
			for (j = 0; j < 60; j++){
				for (k = 0; k < 60; k += 0.1){

					a = i * 30 + (60 * j + k) / 120.0;
					b = 6 * j + k / 20.0;
					double t = a - b;
					if (t < 0)t = -t;
					if (t > 180){
						t -= 180;
					}
					if (t < x){
						ans += 0.1;
					}
				}
			}
		}
		printf("%lf\n", 2 * ans);
	}
	return 0;
}*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

#define MAXN 10010

queue<int> qu;
int deg[MAXN];
bool hash[MAXN], inq[MAXN];
int cnt;


struct Edge{
	int v, next;
}edg[2 * MAXN];

int p[MAXN], ecnt;

void insertEdge(int u, int v){
	edg[ecnt].v = v;
	edg[ecnt].next = p[u];
	p[u] = ecnt++;
	edg[ecnt].v = u;
	edg[ecnt].next = p[v];
	p[v] = ecnt++;
}

void init(){
	while (!qu.empty())qu.pop();
	memset(deg, 0, sizeof(deg));
	ecnt = 0;
	memset(p, -1, sizeof(p));
	memset(hash, false, sizeof(hash));
	memset(inq, false, sizeof(inq));
	cnt = 0;
}

int n;

int main(){
	int i, j, u1, u, v;
	int ans;
	while (scanf("%d", &n) != EOF){
		if (n == 1){
			puts("1");
			continue;
		}
		ans = 0;
		init();
		for (i = 1; i < n; i++){
			scanf("%d %d", &u, &v);
			insertEdge(u, v);
			deg[u]++;
			deg[v]++;
		}
		for (i = 1; i <= n; i++){
			if (deg[i] == 1){
				qu.push(i);
				inq[i] = true;
			}
		}

		while (!qu.empty()){
			u = qu.front();
			qu.pop();
			inq[u] = false;
			//if (hash[u])continue;
			if (deg[u] == 0){
				if (hash[u])continue;
				ans++;
				hash[u] = true;
				cnt++;
				if (cnt == n){
					break;
				}
				continue;
			}
			for (i = p[u]; i != -1; i = edg[i].next){
				v = edg[i].v;
				if (deg[v]){
					break;
				}
			}
			u = v;

			ans++;

			if (!hash[u]){
				hash[u] = true;
				cnt++;
				if (cnt == n)break;
			}



			for (i = p[u]; i != -1; i = edg[i].next){
				v = edg[i].v;

				if (!hash[v]){
					hash[v] = true;
					cnt++;
					if (cnt == n)break;
				}

				for (j = p[v]; j != -1; j = edg[j].next){
					u1 = edg[j].v;
					deg[v]--;
					deg[u1]--;
					if (u1 == u)continue;
					if (deg[u1] <= 1 && !inq[u1]){
						qu.push(u1);
						inq[u1] = true;
					}
				}
			}
			if (cnt == n)break;
		}
		printf("%d\n", ans);
	}
	return 0;
}
*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <ctime>
using namespace std;

#define ll long long

ll rand64(){
	return 1LL * rand() * rand();
}

int main(){
	srand(time(NULL));
	freopen("tetris2.in", "w", stdout);
	int T = 2;
	printf("%d\n", T);
	int n = 100000, k = 10;


	int i, j;
	ll y1, y2;

	while (T--){
		printf("%d %d\n", n, k);
		for (i = 0; i < n; i++){
			if (rand() % 10 < 7){
				putchar('i');
				//printf(" %d %d %lld\n", rand() % k + 1, rand() & 1, 1LL * rand() % 1000000000 + 1);
				printf(" %d %d %lld\n", rand() % k + 1, rand() & 1, rand64() % 1000000000 + 1);
			}
			else{
				putchar('q');
				y2 = rand64() % (1000000000000LL);
				y1 = rand64() % y2;
				printf(" %lld %lld\n", y1, y2);
			}
		}
	}
	return 0;
}
*/


/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <vector>
#include <string>
#include <vector>
#include <queue>
#include <algorithm>
#include <cmath>
using namespace std;


class T9{
public:
	int from[300];
	bool ok[100];
	vector<string> vec;
	void makevec(string ss, vector<string> &dict, vector<string> &part){
		int i, j, k;
		int len = ss.length();
		int ds = dict.size();
		vec.clear();
		memset(ok, true, sizeof(ok));
		for (j = 0; j < ds; j++){
			if (dict[j].length() != len){
				ok[j] = false;
			}
		}
		for (i = 0; i < len; i++){
			k = ss[i] - '0';
			if (part[k - 1].length() == 0)continue;
			for (j = 0; j < ds; j++){
				if (ok[j]){
					if (from[dict[j][i]] != k){
						ok[j] = false;
					}
				}
			}
		}
		for (j = 0; j < ds; j++){
			if (ok[j]){
				vec.push_back(dict[j]);
			}
		}

	}
	string message(vector <string> part, vector <string> dict, vector <string> keystr){
		int i, j, k;
		int len;
		for (i = 0; i < 9; i++){
			k = part[i].length();
			for (j = 0; j < k; j++){
				from[part[i][j]] = i + 1;
			}
		}

		sort(dict.begin(), dict.end());

		string str = "", ans = "", ss;
		len = keystr.size();
		for (i = 0; i < len; i++){
			str += keystr[i];
		}
		len = str.length();

		ss = "";
		i = 0;
		while (i < len){
			if (str[i] >= '1' && str[i] <= '9'){
				ss += str[i];
				i++;
				continue;
			}
			cout << ss << endl;
			if (ss.length()){
				makevec(ss, dict, part);
				ss = "";
				j = 0;
				while (i < len && (str[i] == '#' || str[i] == '*')){
					if (str[i] == '#')j++;
					else j += 5;
					i++;
				}
				ans += vec[j];
				cout << ans << endl;
				if (i == len)break;
			}
			if (str[i] == '0'){
				ans += " ";
				i++;
				continue;
			}
		}
		if (ss.length()){
			makevec(ss, dict, part);
			j = 0;
			while (i < len && (str[i] == '#' || str[i] == '*')){
				if (str[i] == '#')j++;
				else j += 5;
			}
			ans += vec[j];

		}
		return ans;

	}
};

T9 tt;

int main(){
	vector<string> vec, v2, v3;
	vec.push_back("");
	vec.push_back("abc");
	vec.push_back("def");
	vec.push_back("ghi");
	vec.push_back("jkl");
	vec.push_back("mno");
	vec.push_back("pqrs");
	vec.push_back("tuv");
	vec.push_back("wxyz");

	v2.push_back("bad");
	v2.push_back("tie");

	v3.push_back("0843#000843#000");

	cout << tt.message(vec, v2, v3) << endl;
	return 0;

}
*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

#define ll long long
#define INF 0x7f7f7f7f

int n, m;

struct S{
	int x, y, z, step;
	ll b, e;
	bool logic(){
		return (0 <= x && x < n && 0 <= y && y < m);
	}
}cur, next;

int hash[8][8][576];
char g[10][10];

int move[4][2] = {
		{0, 1},
		{0, -1},
		{1, 0},
		{-1, 0}
};

inline ll poss(int x, int y){
	return 1LL << (x * m + y);
}

void bfs(int x, int y){
	int i, j;
	cur.x = x;
	cur.y = y;
	cur.z = cur.step = 0;
	cur.b = cur.e = 0;
	for (i = 0; i < n; i++){
		for (j = 0; j < m; j++){
			if (g[i][j] == 'X'){
				cur.b += poss(i, j);
			}
			if ('1' <= g[i][j] && g[i][j] <= '9'){
				cur.e += poss(i, j);
			}
		}
	}
	memset(hash, 0x7f, sizeof(hash));
	hash[x][y][0] = 0;

	queue<S> qu;
	qu.push(cur);

	while (!qu.empty()){
		cur = qu.front();
		qu.pop();

		for (i = 0; i < 4; i++){
			next = cur;
			next.x += move[i][0];
			next.y += move[i][1];

			if (next.logic()){
				if (g[next.x][next.y] == 'X' && (next.b & poss(next.x, next.y)) != 0){
					if (next.z && next.step + 2 < hash[next.x][next.y][next.z - 1]){
						next.b &= ~poss(next.x, next.y);
						next.z--;
						next.step += 2;
						hash[next.x][next.y][next.z] = next.step;
						qu.push(next);
					}
				}
				else if ('1' <= g[next.x][next.y] && g[next.x][next.y] <= '9' && (next.e & poss(next.x, next.y)) != 0){
					if (next.step + 1 < hash[next.x][next.y][next.z + g[next.x][next.y] - '0']){
						next.e &= ~poss(next.x, next.y);
						next.z += g[next.x][next.y] - '0';
						next.step++;
						hash[next.x][next.y][next.z] = next.step;
						qu.push(next);
					}
				}
				else{
					if (next.step + 1 < hash[next.x][next.y][next.z]){
						next.step++;
						hash[next.x][next.y][next.z] = next.step;
						qu.push(next);
					}
				}
			}

		}


	}


}

int main(){
	int i, j;
	int ans;
	int edx, edy;
	while (scanf("%d %d", &n, &m) != EOF && n + m){
		getchar();
		for (i = 0; i < n; i++){
			scanf("%s", g[i]);
		}
		for (i = 0; i < n; i++){
			for (j = 0; j < m; j++){
				if (g[i][j] == 'S'){
					bfs(i, j);
				}
				if (g[i][j] == 'D'){
					edx = i;
					edy = j;
				}
			}
		}
		ans = INF;
		for (i = 0; i < 576; i++){
			ans = min(ans, hash[edx][edy][i]);
		}
		if (ans == INF){
			puts("-1");
		}
		else printf("%d\n", ans);
	}
	return 0;
}*/
/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <ctime>
using namespace std;

int main(){
	srand(time(NULL));
	int i, j, k;
	j = 30;
	while (j--){
		for (i = 0; i < 100; i++){
			if (rand() & 1){
				if (rand() % 4 == 0)putchar('+');
				else if (rand() % 4 == 1)putchar('-');
				else if (rand() % 4 == 2)putchar('*');
				else if (rand() % 4 == 3)putchar('/');
			}
			else{
				printf("%d", rand() % 10);
			}
		}
		putchar('\n');
	}

}*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <queue>
using namespace std;

#define INF 0x7f7f7f7f
#define MAXN 4100

struct Edge {
	int v, c, cost, next;
} edg[210000];
int ecnt, p[MAXN];

bool inq[MAXN];
int d[MAXN], pre[MAXN], low[MAXN];
int st, ed, mxflow, mncost;

void init() {
	ecnt = 0;
	memset(p, -1, sizeof(p));
}

void insertEdge(int u, int v, int c, int cost) {
	edg[ecnt].v = v;
	edg[ecnt].c = c;
	edg[ecnt].cost = cost;
	edg[ecnt].next = p[u];
	p[u] = ecnt++;
	edg[ecnt].v = u;
	edg[ecnt].c = 0;
	edg[ecnt].cost = INF;
	edg[ecnt].next = p[v];
	p[v] = ecnt++;
}

bool spfa() {
	int u, v, i, c, cost;
	queue<int> qu;
	memset(inq, false, sizeof(inq));
	memset(d, 0x7f, sizeof(d));
	memset(pre, -1, sizeof(pre));
	d[st] = 0;
	inq[st] = true;
	low[st] = INF;
	qu.push(st);
	while (!qu.empty()) {
		u = qu.front();
		qu.pop();
		inq[u] = false;
		for (i = p[u]; i != -1; i = edg[i].next) {
			v = edg[i].v, c = edg[i].c, cost = edg[i].cost;
			if (c > 0 && d[u] + cost < d[v]) {
				d[v] = d[u] + cost;
				pre[v] = i;
				low[v] = min(low[u], c);
				if (!inq[v]) {
					inq[v] = true;
					qu.push(v);
				}
			}
		}
	}
	return d[ed] != INF;
}

void costflow() {
	int tag;
	mxflow = mncost = 0;
	while (spfa()) {
		tag = pre[ed];
		mxflow += low[ed];
		mncost += low[ed] * d[ed];
		while (tag != -1) {
			edg[tag].c -= low[ed];
			edg[tag ^ 1].c += low[ed];
			edg[tag ^ 1].cost = -edg[tag].cost;
			tag = pre[edg[tag ^ 1].v];
		}
	}
}

int val[2010];
char str[2010];

int main(){
	int i, j, n;
	while (scanf("%d", &n) != EOF && n){
		init();
		st = 0, ed = 2 * n + 1;
		for (i = 1; i <= n; i++){
			scanf("%d", &val[i]);
			insertEdge(st, i, 1, 0);
			insertEdge(i + n, ed, 1, 0);
		}
		getchar();
		for (i = 1; i <= n; i++){
			scanf("%s", str);
			for (j = 1; j <= n; j++){
				if (str[j - 1] == '1'){
					insertEdge(i, j + n, 1, 200 - (val[i] ^ val[j]));
				}
			}
		}
		costflow();
		printf("%d\n", 200 * mxflow - mncost);

	}
	return 0;
}
*/

/*
#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
using namespace std;

#define MAXN 32000

int prim[MAXN], pcnt;
bool isp[MAXN];

void sha(){
	pcnt = 0;
	memset(isp, true, sizeof(isp));
	int i, j;
	for (i = 2; i < MAXN; i++){
		if (isp[i]){
			prim[pcnt++] = i;
			for (j = i; i * j < MAXN; j++){
				isp[i * j] = false;
			}
		}
	}
}

int p[100], pc;

void fen(int n){
	int i;
	for (i = 0; i < pcnt && prim[i] * prim[i] <= n; i++){
		if (n % prim[i] == 0){
			p[pc++] = prim[i];
			do{
				n /= prim[i];
			}while (n % prim[i] == 0);
		}
		if (n == 1)break;
	}
	if (n != 1){
		p[pc++] = n;
	}
}

int dfs(int index, int mx) {//求mx以下(包含)可被2,3或5整除的数的个数
	int i, ret = 0;
	for (i = index; i < pc; i++) {
		ret += mx / p[i];
		ret -= dfs(i + 1, mx / p[i]);
	}
	return ret;
}

int main(){
	int cas = 1;
	int i, j;
	int n, m, k;
	long long l, r, mid, res;

	sha();
	int T;
	scanf("%d", &T);
	while (T--){
		scanf("%d %d %d", &n, &m, &k);
		pc = 0;
		fen(n);
		fen(m);
		if (pc){
			sort(p, p + pc);
			j = 1;
			for (i = 1; i < pc; i++){
				if (p[i] != p[j - 1]){
					p[j++] = p[i];
				}
			}
			pc = j;
		}

		l = 1, r = 10000000000LL, res = -1;
		while (l <= r){
			mid = (l + r) >> 1;
			if (mid - 1 - dfs(0, mid - 1) < k){
				res = mid;
				l = mid + 1;
			}
			else r = mid - 1;



		}
		printf("Case %d: %lld\n", cas++, res);

	}
	return 0;
}
*/

#include <iostream>
#include <cstdio>
#include <cstring>
using namespace std;

char g[5][5];

int main(){
	int i, j, x, y;
	for (i = 0; i < 3; i++){
		scanf("%s", &g[i]);
	}
	for (i = 0; i < 3; i++){
		for (j = 0; j < 3; j++){
			x = 3 - 1 - i;
			y = 3 - 1 - j;
			if (g[i][j] != g[x][y])break;
		}
		if (j < 3)break;
	}
	if (i < 3)puts("NO");
	else puts("YES");
	return 0;
}
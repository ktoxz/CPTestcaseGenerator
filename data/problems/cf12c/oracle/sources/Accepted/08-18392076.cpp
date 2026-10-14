#include <bits/stdc++.h>



#define mp make_pair

#define pb push_back

#define PI 3.14159265358979323846

#define FORup(i, a, n) for (int i = a; i < n; i++)

#define FORdown(i, a, n) for (int i = a; i >= n; i--)



using namespace std;



typedef unsigned long long ull;

typedef long long ll;

typedef long double ld;



const int MAXN = 100 + 10;

const int INF = INT_MAX;

const double EXP = 0.0001;



void files(){

	freopen("input.txt", "r", stdin);

	freopen("output.txt", "w", stdout);

}



int a[MAXN], b[MAXN];

map <string, int> fruit;



int main(){

//	files();

	ios_base::sync_with_stdio(false);

    

    int n, m;

    string s;

    

    cin >> n >> m;

    for (int i = 0; i < n; i++) cin >> a[i];

    

    for (int i = 0; i < m; i++){

        cin >> s;

        fruit[s]++;

    }

    

    int j = 0;

    for (auto i = fruit.begin(); i != fruit.end(); i++, j++){

        b[j] = i -> second; 

    }

    

    sort(b, b + j);

    sort(a, a + n);

    

    int d = 0, p = n - 1, minAns = 0, maxAns = 0;

    for (int i = j - 1; i >= 0; i--, d++, p--){

        minAns += b[i] * a[d];

        maxAns += b[i] * a[p];

    }

    

    cout << minAns << " " << maxAns;

    

    return 0;

}
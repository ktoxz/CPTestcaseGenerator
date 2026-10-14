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



const int MAXN = 100000 + 10;

const int INF = INT_MAX;

const double EXP = 0.0001;



void files(){

	freopen("input.txt", "r", stdin);

	freopen("output.txt", "w", stdout);

}



char a[4][4];



int main(){

//	files();

	ios_base::sync_with_stdio(false);



    for (int i = 1; i <= 3; i++)

        for (int j = 1; j <= 3; j++) cin >> a[i][j];

    

    for (int i = 1; i <= 3; i++)

        for (int j = 1; j <= 3; j++)

            if (a[4 - i][4 - j] != a[i][j]) {cout << "NO"; return 0;}

            

    cout << "YES";

    

    return 0;

}
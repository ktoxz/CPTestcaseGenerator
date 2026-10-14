#include <bits/stdc++.h>

#define pb push_back

#define mp make_pair

using namespace std;

typedef long long ll;

typedef pair <int,int> pii;



const int maxN = 1000 + 10;

int a[maxN],n,m,h;



int32_t main()

{

    ios_base::sync_with_stdio(false); cin.tie(0);

    cin >> n >> m >> h; //n adam, m department

    h--;

    for (int i = 0 ; i < m ; i++)

    	cin >> a[i];



    // javab = 1 - ehtemale inke hichki az department e khodesh nabashe

   	int sum = 0;

   	for (int i = 0 ; i < m ; i++)

   		sum += a[i]; //tedaade kolle adama



   	if (sum < n)

   		return cout << -1 , 0;

   	double res = 1;

   	for (int i = 0 ; i < a[h] - 1 ; i++) 

   		res *= (double)(sum - n - i) / (sum - i - 1);



   	cout << fixed << setprecision(6) << 1 - res << endl;

    return 0;      

}
#include<bits/stdc++.h>
#include<string>
#define lli long long int
const lli MOD = 1000000007ll;
const int mxsz = 200005;
const int LG = 30;
using namespace std;

int main()
{
	std::ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n, m;
    cin >> n >> m;
    int a[n + 1], b[n + 1];
    for(int i = 1; i <= n; i++){
    	cin >> a[i];
    	if(a[i] == 1){
    		cout << "-1";
    		return 0;
		}
	}
	for(int i = 1; i <= n; i++){
		cin >> b[i];
		if(b[i] == 1){
			cout << "-1";
			return 0;
		}
	}
	double ans = (double)m;
	ans = (ans * (double)b[1]) / ((double)b[1] - (double)1.0);
//	printf("%.7f\n", ans);
	for(int i = n; i > 1; i--){
		ans = (ans * (double)a[i]) / ((double)a[i] - (double)1.0);
//	printf("%.7f\n", ans);
		ans = (ans * (double)b[i]) / ((double)b[i] - (double)1.0);
//	printf("%.7f\n", ans);
	}
	ans = (ans * (double)a[1]) / ((double)a[1] - (double)1.0);
	printf("%.15f", ans - (double)m);
    return 0;
}
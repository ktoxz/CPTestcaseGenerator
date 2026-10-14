#include <bits/stdc++.h>

using namespace std;

#define SZ(_x) ((int)(_x).size())

#define LL long long

#define ULL unsigned LL

#define PII pair<int, int>

#define VI vector<int>

#define VII vector< PII >

const int INF = 2123123123;

const int MOD = 1e9+7;



string N;

int main(){

	ios::sync_with_stdio(false); cin.tie(0); cout.tie(0);

	cin >> N;

	int n = 0;

	for(int i = 0; i < SZ(N); i++) n += N[i]-'0';

	if(SZ(N) == 1) puts("0");

	else{

		int ans = 1;

		while(n >= 10){

			int sum = 0;

			while(n > 0){

				sum += n%10;

				n /= 10;

			}

			n = sum;

			ans++;

		}

		printf("%d\n", ans);

	}

	return 0;

}
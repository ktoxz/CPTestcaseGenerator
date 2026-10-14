#include <bits/stdc++.h>
#define LL long long
using namespace std;
const int AX = 2e5+66;
char s[AX];
int m[AX];
int a[AX];
int main(){
	cin >> s;
	int n = strlen(s),ok=0;
	for(int i = 0 ; i < n ; i ++ ){
		a[i] = ( s[i] - '0' ) % 3;
	}
	m[0] = 1 ;
	int ans = 0 , res = 0 ; 
	for( int i = 0 ; i < n ; i ++){
		ans += a[i];
		ans %= 3;
		if( m[ans] ){
			res++;
			m[1]=0;
			m[2]=0;
			ans = 0;
		}else m[ans]++;
	}
	printf("%d\n",res);
	return 0;
}
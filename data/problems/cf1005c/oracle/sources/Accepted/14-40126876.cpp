#include <bits/stdc++.h>

using namespace std;

int a[1200005];

int main(){

	ios::sync_with_stdio(false);
	cin.tie(0);
	int n;
	cin >> n;
	map<int,int> m;
	int cnt=0;
	for(int i=0;i<n;i++){
		cin >> a[i];
		m[a[i]]++;
	}
	for(int i=0;i<n;i++){
		bool found=false;
		for(int j=0;j<=31;j++){
			if(m.find((1<<j)-a[i])!=m.end()){
				if((1<<j)-a[i] == a[i] and m[a[i]]==1)
					continue;
				found = true;
				break;
			}
		}
		if(!found)
			cnt++;
	}
	cout << cnt;


}
#include <algorithm>
#include <cassert>
#include <climits>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <iostream>
#include <iterator>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int main(){
	int n,m;
	string s;
	while(cin >> n >> m){
		map<string,int> items;
		vector<int> price(n);
		for(int i = 0; i<n; i++) cin >> price[i];
		sort(price.begin(), price.end());
		for(int i = 0; i<m; i++){
			cin >> s;
			if(items.count(s) == 0) items[s] = 1;
			else items[s]++;
		}
		vector<int> amounts;
		for(map<string,int>::iterator it = items.begin(); it != items.end(); ++it)
			amounts.push_back(it->second);
		sort(amounts.begin(), amounts.end(), greater<int>());
		int best=0,worst=0;
		for(int i = 0; i<amounts.size(); i++){
			best += price[i]*amounts[i];
			worst += price[n-i-1]*amounts[i];
		}
		printf("%d %d\n",best,worst);
	}
	return EXIT_SUCCESS;
}
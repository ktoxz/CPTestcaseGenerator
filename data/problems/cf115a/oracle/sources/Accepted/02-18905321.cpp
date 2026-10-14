#include <iostream>

#include <algorithm>

#include <cmath>

#include <cstring>

#include <vector>



using namespace std;



vector <int> v[2020];

int n, res = 0, used[2020];



void dfs(int s, int ur){

	used[s] = 1;

	res = max(res, ur);

	for(int i = 0; i < v[s].size(); i++){

		int to = v[s][i];

		if(used[to] == 0) dfs(to, ur + 1);

	}

}



int main(){     

    cin >> n;

    for(int i = 0; i < n; i++){

    	int p; cin >> p;

    	if(p != -1) v[p].push_back(i+1);	

    }

    for(int i = 1; i <= n; i++){

    	if(used[i] == 0) dfs(i, 1);

    	memset(used, 0, sizeof(used));

    }

    cout << res;

	return 0;

}
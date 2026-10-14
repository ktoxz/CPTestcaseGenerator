#include <cstdio>

#include <iostream>

#include <vector>



using namespace std;





const int MAX_N = 1000 * 100 + 100;

int n, x, ans, mark[MAX_N];

vector <int> adj[MAX_N];

vector <int> boss;



void readInput(){

	cin >> n;

	for(int i = 0; i < n; i++){

		cin >> x;

		x--;

		if(x >= 0)

			adj[x].push_back(i);

		else

			boss.push_back(i);

	}

}



int dfs(int v){

	mark[v] = 1;

	int lvl = 1;

	for(int i = 0; i < adj[v].size(); i++){

		int u = adj[v][i];

		if(mark[u] == 0)

			lvl = max(lvl, dfs(u) + 1);

	}

	return lvl;

}



int main(){

	readInput();

	for(int i = 0; i < boss.size(); i++){

		int root = boss[i];

		ans = max(ans, dfs(root));

	}

	cout << ans << endl;

	return 0;

}
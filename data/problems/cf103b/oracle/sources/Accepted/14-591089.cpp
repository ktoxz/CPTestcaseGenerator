#include <vector>
#include <set>
#include <map>
#include <cmath>
#include <string>
#include <cstring>
#include <iostream>
#include <cstdio>
#include <algorithm>
#include <sstream>
#include <queue>

using namespace std;

struct arc{
	int s, prev;
} arr[305];

int beg[305], kol = 0;

void add_arc(int f, int s){
	arr[kol].s = s;
	arr[kol].prev = beg[f];
	beg[f] = kol++;

	arr[kol].s = f;
	arr[kol].prev = beg[s];
	beg[s] = kol++;
}

bool was[205];

int DFS(int ver){
	int ret = 1;
	was[ver] = true;
	for (int i=beg[ver]; i!=-1; i=arr[i].prev){
		if (!was[arr[i].s]){
			ret += DFS(arr[i].s);
		}
	}
	return ret;
}


int main(){
	memset(beg, -1, sizeof beg);
	int n, m;
	cin >> n >> m;
	if (m != n || n < 3){
		puts("NO");
		return 0;
	}
	for (int i=0; i<m; i++){
		int f, s;
		cin >> f >> s;
		add_arc(f, s);
	}
	if (DFS(1) != n){
		puts("NO");
	} else {
		puts("FHTAGN!");
	}
	return 0;
}
#include <bits/stdc++.h>

using namespace std;



pair<int,int> rec(int b,int cost);



int cities=0,pipes=0,mincost=INT_MAX;

pair<int,int> arr[1002];

set<int> to;

vector<pair<pair<int,int>,int>> out;



int main() {



	for(int i=0;i<1002;i++)arr[i]=make_pair(0,0);

	cin>>cities>>pipes;

	//setting

	for(int i=0;i<pipes;i++){

		int a1=0,a2=0,c=0;

		cin>>a1>>a2>>c;

		to.insert(a2);

		arr[a1-1]=make_pair(a2,c);

	}

	//chaining

	for(int i=0 ; i<cities ; i++){

		if( !to.count(i+1) && arr[i].first!=0){

			out.push_back(make_pair(rec(i,INT_MAX),i+1));

			mincost=INT_MAX;

		}

	}

	int size=out.size();

	cout<<size<<endl;

	for(int i=0;i<size;i++)cout<<out[i].second<<" "<<out[i].first.first<<" "<<out[i].first.second<<endl;

	return 0;

}



pair<int,int> rec(int b,int cost){

	mincost=min(mincost,cost);

	if(arr[b]!=make_pair(0,0)){

		return rec(arr[b].first-1,arr[b].second);

	}

	else{

		return make_pair(b+1,mincost);

	}

}
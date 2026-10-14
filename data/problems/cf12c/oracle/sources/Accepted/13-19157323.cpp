#include<bits/stdc++.h>





#define pb push_back

#define mp make_pair

#define F first

#define S second





typedef long long ll;

typedef unsigned long long ull;





using namespace std;





int main(){



ios_base::sync_with_stdio(0); cin.tie(0); cout.tie(0);



int n, m; cin >> n >> m;



int arr[n];

for(int i=0; i<n; i++) cin >> arr[i];

sort(arr, arr+n);



map<string, int> fruit;

string s;

for(int i=0; i<m; i++){

    cin >> s;

    fruit[s]++;

}

int cnt = fruit.size();



int arr2[cnt];

int ind=0;



for(map<string, int>::iterator i=fruit.begin(); i!=fruit.end(); i++){

    arr2[ind] = (*i).S;

    ind++;

}



sort(arr2, arr2+cnt);



int Min=0, Max = 0;



for(int i=0, j = cnt-1; i<cnt; i++, j--)

    Min += arr2[i] * arr[j];



for(int i = cnt-1, j=n-1; i>=0; i--,j--)

    Max += arr2[i]*arr[j];



cout <<Min<<" "<<Max;



return 0;



}



/* Rovshan Makhsudov - Chessmaster */
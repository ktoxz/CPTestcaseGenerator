#include <bits/stdc++.h>



using namespace std;



typedef long long ll;

typedef pair<int, int> pii;



#define mp make_pair

#define pb push_back





int main(){

    freopen("input.txt", "r", stdin);

    freopen("output.txt", "w", stdout);

    string s;

    int a;

    cin >> s >> a;



    if(s == "front"){

        if(a == 1) cout << "L";

        else cout << "R";

    }

    else{

        if(a == 2) cout << "L";

        else cout << "R";

    }



    return 0;

}
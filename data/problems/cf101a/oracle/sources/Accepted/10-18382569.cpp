#include <bits/stdc++.h>

using namespace std;



#define ff first

#define ss second

#define PII pair<int,int>



PII F[26];



int main()

{

    string s;

    int k;

    cin >> s >> k;

    int siz = s.size();

    for(int i=0;i<siz;i++){

        F[s[i] - 'a'].ff++;

    }

    for(int i=0;i<26;i++) F[i].ss = i;

    sort(F,F+26);

    int id = 0;

    while(id < 26 && k >= F[id].ff){

        k -= F[id].ff;

        F[id].ff = 0;

        id++;

    }

    int rem = 0;

    for(int i=0;i<26;i++) rem += (bool)F[i].ff;

    cout << rem << endl;

    for(int i=0;i<26;i++) swap(F[i].ff,F[i].ss);

    sort(F,F+26);

    for(int i=0;i<siz;i++) if(F[s[i] - 'a'].ss) cout << s[i];

    return 0;

}
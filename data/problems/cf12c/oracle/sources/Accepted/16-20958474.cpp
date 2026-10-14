#include <iostream>

#include <queue>

#include <vector>

#include <algorithm>

using namespace std;



int main()

{

    int n,m,jojo=0,dio=0;

    cin>>n>>m;

    priority_queue<int>q;

    vector<int>v(n);

    vector<string>s(m);

    for(int i=0;i<n;i++)

        cin>>v[i];

    sort(v.begin(),v.end());

    for(int i=0;i<m;i++)

        cin>>s[i];

    sort(s.begin(),s.end());

    int c=1;

    for(int i=0;i<s.size()-1;i++){

        if(s[i]==s[i+1])

            c++;

        else{

            q.push(c);

            c=1;

        }

    }

    if(s[s.size()-1]!=s[s.size()-2])q.push(1);

    else if(c!=1)q.push(c);

    int cow=q.size();

    for(int i=0;i<cow;i++){

        dio+=q.top()*v[i];

        jojo+=q.top()*v[n-i-1];

        q.pop();

    }

    cout<<dio<<" "<<jojo;



    return 0;

}
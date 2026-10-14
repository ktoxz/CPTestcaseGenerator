#include "iostream"

#include "algorithm"

using namespace std;

int main(){

    string d,t,ans;

    cin>>d>>t;

    int zero=0;

    sort(d.begin(),d.end());

    for(int i=0;d[i]=='0';i++) zero++;

    if(zero<d.length()) ans.insert(ans.end(),d[zero]);

    for(int i=0;i<zero;i++) ans+="0";

    for(int i=zero+1;i<d.length();i++) ans.insert(ans.end(),d[i]);

    if(ans.compare(t)==0) cout<<"OK";

    else cout<<"WRONG_ANSWER";

}
#include<iostream>
#include<algorithm>
using namespace std;

int n,k,x,num,gcdd;
int notes[100002];
bool possible[100002];
void dfs(int ind, int curPos) {
    possible[curPos]=true;
    num++;
    for(int i=ind;i>=0;i--) if(!possible[(curPos+notes[i])%k]) dfs(i,(curPos+notes[i])%k);
}
int main() {
    cin>>n>>k;
    gcdd=k;
    for(int i=0;i<n;i++) {
        cin>>x;
        gcdd=__gcd(gcdd,x);
    }
    cout<<k/gcdd<<endl;
    for(int i=0;i<k;i+=gcdd) cout<<i<<" ";
    cout<<endl;
//    for(int i=0;i<n;i++) cin>>notes[i];
//    sort(notes,notes+n);
//    dfs(n-1,0);
//    cout<<num<<endl;
//    for(int i=0;i<k;i++) {
//        if(possible[i]) cout<<i<<" ";
//    }
//    cout<<endl;
}
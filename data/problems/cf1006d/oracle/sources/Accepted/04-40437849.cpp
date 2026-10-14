// IN THE NAME OF GOD
#include <bits/stdc++.h>
#define pii pair <int, int>
#define ll long long
#define pb push_back
#define ff first
#define ss second
using namespace std;
const int MAXN = 1e5 + 15;
ll int n, ans;
char a[MAXN], b[MAXN];
ll int check(char A, char B, char C, char D){
  set <char> st;
  char p, q;
  st.insert(A); st.insert(B); st.insert(C); st.insert(D);
  if(st.size() == 1) return 0;
  else if(st.size() == 2){
    if((A == B && C == D) || (A == C && B == D) || (A == D && C == B)) return 0;
    else return 1;
  }
  else if(st.size() == 3){
    if(A == B) return 2;
    else return 1;
  }
  else if(st.size() == 4) return 2;
}
int main(){
  //ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
  cin >> n;
  for(int i = 1; i <= n; i++) cin >> a[i];
  for(int i = 1; i <= n; i++) cin >> b[i];
  for(int i = 1; i <= n / 2; i++){
    ans += check(a[i], a[n + 1 - i], b[i], b[n + 1 - i]);
  }
  if(n % 2 && a[n / 2 + 1] != b[n / 2 + 1]) ans++;
  cout << ans;
}
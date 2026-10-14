#include<iostream>

using namespace std;



int main() {

     int n; cin >> n;

     long long s = 0;

     for (long long x,i=1; i<=n; i++) {

         cin >> x;

         s += (x - 1) * i + 1; 

     }

     cout << s << endl;

     return 0;

}
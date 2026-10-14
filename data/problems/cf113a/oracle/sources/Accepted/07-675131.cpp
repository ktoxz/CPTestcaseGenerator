#include <iostream>
#include <string>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <cstdio>
#include <iomanip>
#include <algorithm>
#include <utility>

using namespace std;

typedef long long LL;


const char* suf[6] = 
{
"lios",
"liala",
"etr",
"etra",
"initis",
"inites"
};

void PrintYES() {
  cout << "YES" << endl;
  exit(0);
}

void PrintNO() {
  cout << "NO" << endl;
  exit(0);
}

bool HasSuffix(string s, string suffix) {
  int n = s.length();
  int m = suffix.length();
  if (m > n)
    return false;
  for (int i = 0; i < m; ++i)
    if (s[n-m+i] != suffix[i])
      return false;
  return true;
}

int GetType(string s) {
  for (int i = 0; i < 6; ++i)
    if (HasSuffix(s, suf[i]))
      return i;
  return 6;
}

vector<int> a;

int main() {
 //       freopen ("input.txt", "r", stdin); freopen ("output.txt", "w", stdout);

        string s;
        while (cin >> s)
          a.push_back(GetType(s));

        if (a.size() == 1 && a[0] < 6)
          PrintYES();

        int k = 0;
        while (k < a.size() && a[k] < 2)
          ++k;
        if (k == a.size() || a[k]/2 != 1)
          PrintNO();
        ++k;
        for (int i = k; i < a.size(); ++i)
          if (a[i]/2 != 2)  
            PrintNO();

        for (int i = 1; i < a.size(); ++i)
          if (a[i]%2 != a[i-1]%2)
            PrintNO();

        PrintYES();

        
        
        
        return 0;
}
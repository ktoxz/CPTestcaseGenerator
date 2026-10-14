#include <bits/stdc++.h>

using namespace std;



int h, m;

int main(){

  scanf("%d:%d", &h, &m);

  int cur = (60*h+m+1)%1440;

  while(1){

    h = cur/60;

    m = cur%60;

    string s;

    s.push_back(m%10);

    s.push_back(m/10);

    s.push_back(h%10);

    s.push_back(h/10);

    if(s[0] == s[3] && s[1] == s[2]) break;

    cur = (cur+1)%1440;

  }

  if(h < 10) printf("0");

  printf("%d:", h);

  if(m < 10) printf("0");

  printf("%d\n", m);

  return 0;

}
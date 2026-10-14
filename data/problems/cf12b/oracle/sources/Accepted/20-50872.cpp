#include <iostream>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int n, m;
int p[100];
char mm[100];

int main(){
    while (scanf("%d",&n) != EOF){
          scanf("%s",&mm);
          int len = strlen(mm);
          m = 0;
          for (int i = 0; i < len; ++i) m = m * 10 + (mm[i] - '0');
          //printf("m = %d\n",m);
          if (n == 0){
             if (strlen(mm) != 1) puts("WRONG_ANSWER");
             else if (m == 0) puts("OK");
             else puts("WRONG_ANSWER");
          }
          else{
             if (mm[0] == '0'){
                 puts("WRONG_ANSWER");
                 return 0;
             }  
             int x = n;
             memset(p, 0, sizeof(p));
             while (x > 0){
                 p[x % 10]++;
                 x /= 10;
             }
             int now = 0;
             for (int i = 1; i <= 9; ++i)
                 if (p[i]){ 
                     now = i; 
                     p[i]--;
                     break;
                 }
             for (int i = 0; i <= 9; ++i){
                 while (p[i]){
                       now = now * 10 + i;
                       p[i]--;
                 }
             }
             if (now == m) puts("OK");
             else puts("WRONG_ANSWER");   
          }
    }
    return 0;
}
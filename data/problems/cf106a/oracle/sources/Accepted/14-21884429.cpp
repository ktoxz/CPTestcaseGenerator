#include <bits/stdc++.h>

using namespace std;

char s[]="6789TJQKA",c,a,x,b,y;int main(){scanf("%c\n%c%c %c%c", &c, &a, &x, &b, &y);printf("%s\n",x==c&&y!=c||x==y&&strchr(s, a)>strchr(s, b)?"YES":"NO");}
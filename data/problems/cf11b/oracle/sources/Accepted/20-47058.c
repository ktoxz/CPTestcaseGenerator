#include <stdio.h>

int main() {
  int in,i;
  long long x,go;
  scanf("%d",&in);
  x=in<0?-in:in;
  if(x==0) { i=0; goto done; }
  for(go=0,i=1;;i++) {
    go+=i;
    if(go==x) break;
    if(go>x && (go-x)%2==0) break;
  }
done:
  printf("%d\n",i);
  return 0;
}
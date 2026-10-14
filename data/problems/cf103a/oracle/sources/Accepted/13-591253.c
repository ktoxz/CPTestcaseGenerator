#include<stdio.h>

int main(void){
  unsigned long long int n,sum=0,i,in;
  scanf("%I64u",&n);
  for(i=1;i<=n;i++){
    scanf("%I64u",&in);
    sum+=i*in-(i-1);
  }
  printf("%I64u\n",sum);
  return 0;
}
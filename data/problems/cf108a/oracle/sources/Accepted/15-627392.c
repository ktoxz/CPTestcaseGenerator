#include<stdio.h>

int main(void){
  int hh,mm;
  scanf("%d:%d",&hh,&mm);
  do{
    mm++;
    if(mm==60){
      mm=0;
      hh++;
    }
    if(hh==24) hh=0;
  }while(!(mm/10==hh%10 && hh/10==mm%10));
  printf("%02d:%02d\n",hh,mm);
  return 0;
}
#include<stdio.h>
#include<string.h>

#define LEN 100001

int main(void){
  char str[LEN],out[LEN];
  int m,n,i,j,k,l,min,minch;
  int count[26],c=0;
  memset(count,0,sizeof(count));
  scanf("%s%*c",str);
  scanf("%d",&k);
  l=strlen(str);
  for(i=0;i<l;i++) count[str[i]-'a']++;

  while(1){
    min=LEN;
    for(i=0;i<26;i++){
      if(count[i]==0) continue;
      if(min>count[i]){
	min=count[i];
	minch=i;
      }
    }
    if(k<min || min==LEN) break;
    k-=min;
    count[minch]=0;
  }
  for(i=0;i<26;i++) c+=(count[i]!=0);
  
  for(i=0,j=0;i<l;i++){
    if(count[str[i]-'a']==0) continue;
    out[j++]=str[i];
  }
  out[j]='\0';
  printf("%d\n",c);
  puts(out);
  return 0;
}
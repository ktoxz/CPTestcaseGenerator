#include<stdio.h>
#include<stdlib.h>

int compare_int(const int *a, const int *b)
{
    return *a - *b;
}


int main(void){
	int a[11],b[11];
	int i,na,nb,swap,k=0;
	char str[11];
	scanf("%s",str);
	i=0;
	while(str[i]!='\0'){
		a[i]=str[i]-'0';
		i++;
	}
	na=i;
	for(i=0;i<11;i++)str[i]='\0';
	scanf("%s",str);
	i=0;
	while(str[i]!='\0'){
		b[i]=str[i]-'0';
		i++;
	}
	nb=i;
	
	qsort(a, na, sizeof(int), (int (*)(const void*, const void*))compare_int);
	if(a[0]==0){
	    for (i = 1; a[0]!=0; i++) ;
		swap=a[0];
		a[0]=a[i];
		a[i]=swap;
	}
	if(na!=nb){
		printf("WRONG_ANSWER\n");
	}else{
		for(i=0;i<na;i++){
			if(a[i]!=b[i])k=1;
		}
		if(k==0){
			printf("OK\n");
		}else{
			printf("WRONG_ANSWER\n");
		}
	}
	return 0;
}
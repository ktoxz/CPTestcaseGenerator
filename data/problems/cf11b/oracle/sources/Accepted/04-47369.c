#include <stdio.h>

int main()
{
	int n,i,s;
	scanf("%d",&n);
	if(n<0)n=-n;
	s=0;
	for(i=0;s<n;i++,s+=i);
	if(s==n)printf("%d\n",i);
	else
	{
		if((s-n)%2==0)
			printf("%d\n",i);
		else if((s-n+i+1)%2==0)
			printf("%d\n",i+1);
		else
			printf("%d\n",i+2);
	}
	return 0;
}
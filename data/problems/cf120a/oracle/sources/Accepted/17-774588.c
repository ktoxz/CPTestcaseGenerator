#include <stdio.h>
#include <string.h>


int main()
{
	int n;
	char s[10];
	FILE *fp,*fp2;
	fp=fopen("input.txt","r");
	fp2=fopen("output.txt","w");
	//scanf("%s",s);
	//scanf("%d",&n);
	fscanf(fp,"%s",s);
	fscanf(fp,"%d",&n);
	if(strcmp(s,"front")==0)
	{
		if(n==1)
		{
			fprintf(fp2,"L\n");
			return 0;
		}
		else
		{
			fprintf(fp2,"R\n");
			return 0;
		}
		
	}
	if(strcmp(s,"back")==0)
	{
		if(n==2)
		{
			fprintf(fp2,"L\n");
			return 0;
		}
		else
		{
			fprintf(fp2,"R\n");
			return 0;
		}
		
	}

return 0;
}
#include<stdio.h>
int main()
{
	int arr[1000];
	arr['T']=10;
	arr['J']=11;
	arr['Q']=12;
	arr['K']=13;
	arr['A']=14;
	arr['6']=6;
	arr['7']=7;
	arr['8']=8;
	arr['9']=9;	
	char s[2];
	scanf("%s",s);
	char a[10],b[10];
	scanf("%s%s",a,b);
	int ans=0;
	if(a[1]==b[1])
	{
		if(arr[a[0]]>arr[b[0]])
			ans=1;
	}
	else
	{
		if(a[1]==s[0])
			ans=1;
	
	}
	if(ans==1)
	printf("YES\n");
	else
		printf("NO\n");
	return 0;
}
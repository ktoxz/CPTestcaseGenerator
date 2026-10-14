#include<stdio.h>
int arr[100]={0,4,4,4,4,4,4,4,4,4,15,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int fun(int n)
{
	if(n<=0)
		return 0;
	if(n==1)
		return 4;
	int ans=0,i=0;
	for(i=n;i>=1;i--)
	{
		arr[i]--;
		ans+=fun(n-i);
		arr[i]++;
	}
	return ans;
}
int main()
{
	int ans=0,n;
	scanf("%d",&n);
	if(n>10)
	{
		if(n<22)
		{
			ans=arr[n-10];
		}
	}
	printf("%d\n",ans);
	return 0;
}
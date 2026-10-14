#include<stdio.h>
int main()
{
	int ans=0,i,j,k,n,p1,p2,p3,t1,t2;
	scanf("%d %d %d %d %d %d",&n,&p1,&p2,&p3,&t1,&t2);
	int a[n],b[n];
	for(i=0;i<n;i++)
		scanf("%d %d",&a[i],&b[i]);
	for(i=0;i<n;i++)
	{
		j=b[i]-a[i];
		ans=ans+j*p1;
	}

	for(i=1;i<n;i++)
	{
		k=a[i]-b[i-1];
		if(k<=t1)
			ans=ans+k*p1;
		else if(k<=(t1+t2))
			ans=ans+t1*p1+(k-t1)*p2;
		else
			ans=ans+t1*p1+t2*p2+p3*(k-t1-t2);
	}

	printf("%d",ans);
	return 0;
}
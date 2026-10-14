#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>

int cmp(const void *a,const void *b)
{
	return *(int *)a- *(int *)b;
}

int max(int a,int b)
{
	if(a>b)
		return a;
	return b;
}
int min(int a,int b)
{
	if(a>b)
		return a;
	return b;
}
int mod(int a)
{
	if(a<0)
		return -a;
	return a;
}
int binarySearch(int arr[], int l, int r, int x)
{
   if (r >= l)
   {
        int mid = l + (r - l)/2;
 
        // If the element is present at the middle 
        // itself
        if (arr[mid] == x)  
            return mid;
 
        // If element is smaller than mid, then 
        // it can only be present in left subarray
        if (arr[mid] > x) 
            return binarySearch(arr, l, mid-1, x);
 
        // Else the element can only be present
        // in right subarray
        return binarySearch(arr, mid+1, r, x);
   }
 
   // We reach here when element is not 
   // present in array
   return -1;
}

int main()
{
	char a[200004];
	int n,i;
	scanf("%s",a);
	n=strlen(a);
	int sum[200005],ans=0;
	for(i=0;i<n;i++)
	{
		sum[i]=(a[i]-'0')%3;
	}

	for(i=0;i<n;i++)
	{
		if(sum[i]==0)
		{
			ans++;
		}
		else
		{
			if(sum[i]==1)
			{
				if(i+1<n && sum[i+1]==2)
				{
					i++;
					ans++;
					continue;
				}
				if(i+1<n && sum[i+1]==1)
				{
					if(i+2<n && sum[i+2]==1)
					{
						i+=2;
						ans++;
						continue;
					}
				}
			}
			else
			{
				if(i+1<n && sum[i+1]==1)
				{
					i++;
					ans++;
					continue;
				}
				if(i+1<n && sum[i+1]==2)
				{
					if(i+2<n && sum[i+2]==2)
					{
						i+=2;
						ans++;
						continue;
					}
				}

			}
		}
	}
	printf("%d\n",ans );
	return 0;
	
}
#include<cstdio>
#include<iostream>
#include<vector>
#include<cstring>
using namespace std;

int i,len,Ans=0;
int a[200010],b[200010];
char c[200010];

inline int Max(int a,int b){return (a>b)?a:b;}

inline void Work(int low,int high){
	int i=0,cnt=0,Cnt=0;
	if (high<=low)	return;
	i=low;
//	printf("%d %d\n",low,high);
	while (i<=high){
		if ((a[i]+a[i+1])%3==0)	{cnt++;	i+=2;	continue;}
		if (i<=high-2)	if (a[i]==a[i+1]&&a[i]==a[i+2]){
			cnt++;	i+=3;	continue;
		}
		i++;
	}
	i=high;
	while (i>=low){
		if ((a[i]+a[i-1])%3==0)	{Cnt++;	i-=2;	continue;}
		if (i>=low+2)	if (a[i]==a[i-1]&&a[i]==a[i-2]){
			Cnt++;	i-=3;	continue;
		}
		i--;
	}
	Ans+=Max(cnt,Cnt);
}

int main (){
//	freopen("zht.in","r",stdin);
//	freopen("zht.out","w",stdout);
	scanf("%s",&c);
	len=strlen(c)-1;
	if (len==0){
		if (c[0]==48||c[0]==51||c[0]==54||c[0]==57)	printf("1\n");
		else printf("0\n");
		return 0;
	}
	for (i=0;i<=len;i++)	a[i]=(c[i]-48)%3;
	for (i=0;i<=len;i++)	if (a[i]==0)	Ans++,b[++b[0]]=i;
	for (i=1;i<b[0];i++)	Work(b[i]+1,b[i+1]-1);
	if (b[0]==0)	Work(0,len);	else{
		Work(0,b[1]-1);	Work(b[b[0]]+1,len);
	}
	printf("%d\n",Ans);
	return 0;
}
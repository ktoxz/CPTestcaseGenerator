#include <bits/stdc++.h>
using namespace std;
int read() {
	int tot=0,fh=1;char c=getchar();
	while (c<'0'||c>'9') {if (c=='-') fh=-1;c=getchar();}
	while (c>='0'&&c<='9') {tot=tot*10+c-'0';c=getchar();}
	return tot*fh;
}
int n;
double x,a[20010];
int main() {
	n=read();x=read();
	for (int i=1;i<=n*2;i++) {a[i]=read();if (a[i]<=1) {cout<<-1<<endl;return 0;}}
	double tmp=1;
	for (int i=1;i<=n*2;i++) tmp*=a[i]/(a[i]-1);
	double ans=x*tmp-x;
	printf("%.10lf",ans); 
	return 0;
}
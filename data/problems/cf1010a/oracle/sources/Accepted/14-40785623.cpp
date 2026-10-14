#include <cstdio>
using namespace std;
int main()
{
	int n,m,i;
	scanf("%d%d",&n,&m);double w=m;
	for (i=1;i<=(n<<1);i++){
		int x;scanf("%d",&x);if (x==1){
			puts("-1");return 0;
		}w=w*x/(x-1);
	}if (w>=m) printf("%.10f\n",w-m);
	return 0;
}
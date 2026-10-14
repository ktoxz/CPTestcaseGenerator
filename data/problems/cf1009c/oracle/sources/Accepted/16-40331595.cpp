#include<bits/stdc++.h>
using namespace std;
int main(){
	int m,n;
	scanf("%d%d",&m,&n);
	double a,b,t;
	long double sum=0;
	while(n--){
		scanf("%lf%lf",&a,&b);
		sum+=a*m;
		if(b>0){
			sum+=b*m*(m-1)/2.0;
		}else{
			if(m%2==0){
				t=m/2-1;
				sum+=b*(t+1)*(t+1);
			}else{
				t=(m-1)/2;
				sum+=b*t*(t+1);
			}
		}
	}
	sum/=m;
	cout<<fixed<<setprecision(7)<<sum<<endl;
}
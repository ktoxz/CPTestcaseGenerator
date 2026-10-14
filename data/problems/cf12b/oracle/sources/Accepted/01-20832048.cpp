#include<iostream>
#include<algorithm>
using namespace std;
int main(){
	int x,y,z,c1=0,c2=0,i=0,k,l,j;
	cin>>x;
	string m;
	cin>>m;
	z=x;
	while(z!=0){
		z=z/10;
		c1++;
	}
	c2=m.length();
	y=stoi(m);
	if(x==0){
        c1=1;
    }
	int a[c1];
    for(i=0;i<c1;i++){
        a[i]=0;
    }
	z=x;
	i=c1-1;
    
	while(z!=0){
		a[i]=z%10;
		i--;
		z=z/10;
	}
	sort(a,a+c1);
	int index;
	for(i=0;i<c1;i++){
		if(a[i]!=0){
			index=a[i];
			for(j=i;j>0;j--){
				a[j]=a[j-1];
			}
			a[0]=index;
			break;
		}
	}
	int no=0;
	for(i=0;i<c1;i++){
		no=(no*10)+a[i];
	}
	if(no==y && c1==c2){
		cout<<"OK";
	}
	else
		cout<<"WRONG_ANSWER";
	return 0;
}
#include<bits/stdc++.h>
using namespace std;

const int maxn=1e6+7;

int n,k,l,r,sum,ans,a[26],now,la;

char ss[maxn],sss[maxn],s1[maxn],s2[maxn];

int main(){
	scanf("%d",&n);
	scanf("%s",ss);
	scanf("%s",sss);
	for(int i=1;i<=n;i++) s1[i]=ss[i-1];
	for(int i=1;i<=n;i++) s2[i]=sss[i-1];
	if(n%2==1){
		if(s1[n/2+1]!=s2[n/2+1]) ans=1;
		l=n/2;
		r=n/2+2;
	}
    else{
	 	l=n/2;
	 	r=n/2+1;
    }
     while(l>=1){
        memset(a,0,sizeof(a));
        a[s1[l]-'a']++; a[s1[r]-'a']++;
        a[s2[l]-'a']++; a[s2[r]-'a']++;
        sum=0;
        for(int i=0;i<=25;i++) if(a[i]) sum++;
        if(sum==2){
            for(int i=0;i<=25;i++)
                if(a[i]){now=a[i];break;}

            for(int i=25;i>=0;i--) if(a[i]){ la=a[i];break;}
                if(now!=la) ans++;
        }

        else if(sum==3){
            if(s1[l]==s1[r]) ans+=2;
             else ans++;
        }

        else if(sum==4) ans+=2;
        l--;r++;
     }
     cout<<ans<<endl;
}
#include <bits/stdc++.h>

int a,b,n,f;main(){std::cin>>a>>b>>n;while(n-=std::__gcd(f?b:a,n))f^=1;std::cout<<f;}
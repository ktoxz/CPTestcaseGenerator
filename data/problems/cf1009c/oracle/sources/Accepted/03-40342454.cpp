/*
Author: cxw
Email: cxweieee@126.com
codeforces
*/

#include<iostream>
#include<cstring>
#include<cstdio>
#include<string>
#include<cmath>
#include<iomanip>

#define eps 0.00000000001

#include<map>

using namespace std;

long long max(long long a, long long b)
{
    return a>b?a:b;
}
long long min(long long a, long long b){
    return a<b?a:b;
}

long long bisearch(long long a[40], long long value){
    long long left=0, right = 31, mid;
    a[32] = a[31]*2;
    while(left <= right){
        mid = (left+right) / 2;
        if(a[mid]<value && a[mid+1]>=value){
            return mid+1;
        }
        if(a[mid] >= value){
            right = mid;
            mid = (left+right) / 2;
        }
        if(a[mid+1]<value){
            left = mid+1;
            mid = (left+right) / 2;
        }
        if(left==right){
            if(a[left]!=value){
                return 31;
            }
            else{
                return left;
            }
        }
    }
}




int main(){
    long long n, m, x, d;
    long long total;
    while(cin>>n>>m){
        total = 0;
        long long a, b;
        if(n % 2 == 1){
            a = n / 2;
            b = a;
        }
        else{
            a = n / 2;
            b = a - 1;
        }
        for(long long i=0; i < m; i++){
            cin>>x>>d;
            if(d<0){
                total += x*n + a*(a+1)/2*d + b*(b+1)/2*d;
            }
            else{
                total += x*n + (n-1)*n/2*d;
            }
        }
        double res;
        res = (double)total * 1.0 / n + eps;
        cout<<setprecision(10)<<res<<endl;
    }
    return 0;
}
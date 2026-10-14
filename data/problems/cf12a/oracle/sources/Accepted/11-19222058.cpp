#include <bits/stdc++.h>

using namespace std;

int main()

{

    //freopen("cin.txt","r",stdin);

    int a;

    char z[5][5];

    cin>>z[0]>>z[1]>>z[2];

    if(z[1][1]!='.'&&z[1][1]!='X'){

        cout<<"NO"<<endl;

        return 0;

    }

    if(z[0][0]=='.'||z[0][0]=='X'){

        if(z[0][0]!=z[2][2]){

            cout<<"NO"<<endl;

            return 0;

        }

    }

    else{

        cout<<"NO"<<endl;

            return 0;

    }

    if(z[0][1]=='.'||z[0][1]=='X'){

        if(z[0][1]!=z[2][1]){

            cout<<"NO"<<endl;

            return 0;

        }

    }

    else{

        cout<<"NO"<<endl;

            return 0;

    }

    if(z[0][2]=='.'||z[0][2]=='X'){

        if(z[0][2]!=z[2][0]){

            cout<<"NO"<<endl;

            return 0;

        }

    }

    else{

        cout<<"NO"<<endl;

            return 0;

    }

    if(z[1][0]=='.'||z[1][0]=='X'){

        if(z[1][0]!=z[1][2]){

            cout<<"NO"<<endl;

            return 0;

        }

    }

    else{

        cout<<"NO"<<endl;

            return 0;

    }

    cout<<"YES"<<endl;

    return 0;

}
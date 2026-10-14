#include <bits/stdc++.h>

using namespace std;



typedef long long  ll;



#define F              first

#define S              second

#define fin            return 0

#define all(v)         v.begin(),v.end()

#define loop(i,n)      for(int i=0;i<n;i++)

#define lop(i,n)       for(int i=1;i<=n;i++)

/*









int main()

{



    // freopen("input.txt", "r", stdin);

    // freopen("output.txt", "w", stdout);

   ios::sync_with_stdio(false), cin.tie(NULL);







int n;

cin >> n;

int m1 , m2 ;

cin >> m1;

vector<int>a(m1);

vector<int>f1(m1);

loop(i,m1){cin >> a[i];f1[i]=a[i];}

cin >> m2;

vector<int>b(m2);

vector<int>f2(m2);

loop(i,m2){cin >> b[i];f2[i]=b[i];}

ll ans=0;

while(true){



    int x , y;

    x=a[0];y=b[0];

    if(y>x){

        a.erase(a.begin());

        b.erase(b.begin());

        b.push_back(x);

        b.push_back(y);

        ans++;

    }

    else if(x>y){

        a.erase(a.begin());

        b.erase(b.begin());

        a.push_back(y);

        a.push_back(x);

        ans++;

    }

if(ans>200){cout<<"-1"; fin;}

if(a.size()==0){cout<<ans<<" "<<2;fin;}

else if(b.size()==0){cout<<ans<<" "<<1;fin;}



}



    return 0;

}

*/

int main()

{



    // freopen("input.txt", "r", stdin);

    // freopen("output.txt", "w", stdout);

    ios::sync_with_stdio(false), cin.tie(NULL);



    int n ;

    cin >> n ;



int sp[4200] , ram[4096] , hdd[500] , cost[1000] ;

loop(i , n) cin >> sp[i] >> ram[i] >> hdd[i] >> cost[i] ;

loop(i , n){

loop(j , n){

if(i!=j){



    if(sp[i]<sp[j] && ram[i]<ram[j] && hdd[i]<hdd[j] && cost[i]<cost[j]){cost[i]=1e5;break;}

}

}

}



int pos , mn=1e4 ;

loop(i , n){

if(cost[i]<mn){mn=cost[i];pos=i+1;}

}

cout << pos;





}



/*



class omar{



public:

    omar()

    {

        x=5;

        y=7;

        cout<<x+y<<endl;

    }



    private:

        int x;

        int y;



  friend void friends(omar & ob);



};

void friends(omar & ob){

ob.x=20;

ob.y=40;

cout<<ob.x+ob.y<<endl;

}



int main(){



omar obj;

friends(obj);



return 0;



}



*/



/*

class fn

{

public:

    void setlength(double length)

    {

        l=length;

    }

    void setbreadth(double breadth)

    {

        b=breadth;

    }

    void setheight(double height)

    {

        h=height;

    }

    double getlen()

    {

        return l;

    }

    double getbre()

    {

        return b;

    }

    double gethei()

    {

        return h;

    }







 private:

     double l;

     double b;

     double h;





};



int main()

{









fn box1;

box1.setlength(4.0);

box1.setbreadth(3.0);

box1.setheight(6.0);

double x= box1.getlen();

double y= box1.getbre();

double z= box1.gethei();



cout<<x*y*z<<endl;





box1.setlength(10.0);

box1.setbreadth(12.0);

box1.setheight(13.0);

 x= box1.getlen();

 y= box1.getbre();

 z= box1.gethei();



cout<<x*y*z;





    return 0;

}

*/
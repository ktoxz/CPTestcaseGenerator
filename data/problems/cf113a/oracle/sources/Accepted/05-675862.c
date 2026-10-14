#include <stdio.h>
#include <string.h>

char str[200005]={0};

int main()
{
 long flag=0;
 long t=1;
 long s=0;
 long l;
 long temp=0;
 
 for(;;)
   {
    temp=0;
    if(scanf("%s",str)==EOF)
     break;
    l=strlen(str);
    
    if(l>=4)
     if(str[l-1]=='s'&&str[l-2]=='o'&&str[l-3]=='i'&&str[l-4]=='l')
      flag|=1,temp=1;
    if(l>=5)
     if(str[l-1]=='a'&&str[l-2]=='l'&&str[l-3]=='a'&&str[l-4]=='i'&&str[l-5]=='l')
      flag|=2,temp=2;
    if(l>=3)
     if(str[l-1]=='r'&&str[l-2]=='t'&&str[l-3]=='e')
      flag|=1,temp=3;
    if(l>=4)
     if(str[l-1]=='a'&&str[l-2]=='r'&&str[l-3]=='t'&&str[l-4]=='e')
      flag|=2,temp=4;
    if(l>=6)
     if(str[l-1]=='s'&&str[l-2]=='i'&&str[l-3]=='t'&&str[l-4]=='i'&&str[l-5]=='n'&&str[l-6]=='i')
      flag|=1,temp=5;
    if(l>=6)
     if(str[l-1]=='s'&&str[l-2]=='e'&&str[l-3]=='t'&&str[l-4]=='i'&&str[l-5]=='n'&&str[l-6]=='i')
      flag|=2,temp=6;
    
    if(temp==0)
     goto loop;
    s++;
    
    if(temp<=2&&t!=1)
     goto loop2;
    if(temp>=5&&t!=3)
     goto loop2;
    if(temp==3||temp==4)
     {
      if(t!=1)
       goto loop2;
      t=3;
     }
   }
 
 if(t!=3&&s!=1||flag==3)
  {
   loop:
   printf("NO\n");
   return 0;
   loop2:
   if(s!=1||scanf("%s",str)!=EOF)
    {
     printf("NO\n");
     return 0;
    }
   else
    {
     printf("YES\n");
     return 0;
    }
  }
 else
  printf("YES\n");
 
 return 0;
}
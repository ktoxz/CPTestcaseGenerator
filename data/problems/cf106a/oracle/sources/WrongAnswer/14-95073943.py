suits={'S','H','D','C'}
ranks={'6':0,'7':1,'8':2,'9':3,'T':4,'J':5,'Q':6,'K':7,'A':8}
trump=input()
card1,card2=input().split()
if card1[1]==trump:
    if card2[1]==trump:
        if(ranks[card1[0]]>ranks[card2[0]]):
            print("YES")
    else:
        print("YES")
else:
    if card2[1]==trump:
        print("NO")
    else:
        if(ranks[card1[0]]>ranks[card2[0]]):
            print("YES")
        else:
            print("NO")
trump = input()
cards = input()
if cards[1] == trump:
    print("YES")
else:
    if cards[1]==cards[4] and int(cards[0]) > int(cards[3]):
        print("YES")
    else:
        print("NO")
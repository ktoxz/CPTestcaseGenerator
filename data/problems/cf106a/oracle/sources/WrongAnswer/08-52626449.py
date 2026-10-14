suite = str(input())
carda, cardb = [str(x) for x in input().strip().split()]
win = 0
deck = ["6", "7", "8", "9", "T", "J", "Q", "K", "A"]
if(carda[1]==suite[0]):
	win=1
elif(cardb[1]==suite[0]):
	win=2
elif(deck.index(carda[0]) > deck.index(cardb[0])):
	win=1
elif(deck.index(carda[0]) < deck.index(cardb[0])):
	win=2
else:
	win=0
if(win==1):
	print("YES")
elif(win==2):
	print("NO")
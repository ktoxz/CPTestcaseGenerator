power_of_cards = ['6','7','8','9','T','J','Q','K','A']
beatar = input()
card1, card2 = input().split()
if card1[1] == card2[1]:
	if power_of_cards.index(card1[0]) > power_of_cards.index(card2[0]):
		print('YES')
elif card1[1] == beatar:
	print('YES')
else:
	print('NO')
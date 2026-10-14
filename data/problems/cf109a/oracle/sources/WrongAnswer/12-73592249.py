entrada = int(input())
usou = []
sete = 0
quatro = 0
tmp = False
tmp2 = False
#tmp3 = False
#tmp4 = False

cont = 11
while not tmp:
	cont -= 1
	if cont == 0:
		break
	if (entrada % (7 * cont)) % 4 == 0:
		tmp = True
		x = (entrada % (7 * cont)) / 4
		break
		
if not tmp:
	cont2 = 11
	while not tmp2:
		cont2 -= 1
		if cont2 == 0:
			break
		if (entrada % (4 * cont2)) % 7 == 0:
			tmp2 = True
			y = (entrada % (4 * cont2)) / 7
			break
	


	
	
if not tmp and not tmp2:
	print(-1)
else:	
	final = ""
	
	if tmp:
		for e in range(int(x)):
			final += "4"
		for e in range(cont):
			final += "7"
	elif tmp2:
		for e in range(int(y)):
			final += "7"
		for e in range(cont2):
			final += "4"

	print(final)
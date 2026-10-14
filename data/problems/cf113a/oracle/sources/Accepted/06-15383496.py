#!/usr/bin/python3
import re
al = re.compile(r'^1*23*$')
def getType(word):
	if word.endswith("lios"): return 1
	elif word.endswith("liala"): return -1
	elif word.endswith("etr"): return 2
	elif word.endswith("etra"): return -2
	elif word.endswith("initis"):return 3
	elif word.endswith("inites"): return -3
	else: return 0


words = input().strip().split()
words = [getType(x) for x in words]
if len(words) == 1:
	if words[0] != 0:print("YES")
	else:print("NO")
else:
	p = words[0]
	for x in words:
		if p*x <= 0:
			print("NO")
			exit()
	words = [str(abs(x)) for x in words]
	words = "".join(words)
	#print(words)
	if al.match(words):print("YES")
	else:print("NO")
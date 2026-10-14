# import sys
# sys.stdin=open('F:\\C\\Script\\input.txt','r')
# sys.stdout=open('F:\\C\\Script\\output.txt','w')
# sys.stdout.flush()

# I = lambda:[int(i) for i in input().split()]

s = input()
n = 0
count = 0
se = set()
for i in s:
	if i == 0 or not int(i) % 3:
		count += 1
		n = 0
		se = set()
		continue
	n += int(i)
	if not  n%3:
		count += 1
		n = 0
		se = set()
		continue
	if (n - (n//3)*3) in se:
		count += 1
		se = set()
		n = 0
		continue
	se.add(n%3)
print (count)
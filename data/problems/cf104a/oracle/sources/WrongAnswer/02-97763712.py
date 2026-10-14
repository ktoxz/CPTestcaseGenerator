#round 80
n = int(input())

counter = 0

disc = {"kingh":10,"jackh":10,'queenh':10,"kingd":10,"jackd":10,'queend':10,"kingc":10,"jackc":10,'queenc':10,"kings":10,"jacks":10}

for i in range(2,11):
	if (10+i)==n:
		counter += 1

counter = counter*4

for i in disc.keys():
	if 10+disc[i]==n:
		counter += 1

if 10+11==n or 10+1==n:
	counter += 1

print(counter)
first =list(input())# получаем список с строковыми элементами  ['3', '3', '1', '0']
second = input() 
out=""
if first[-1] == "0": # если последний элемент 0, то перебираем с конца список, пока не найдем отличный от 0 элемент
	i=2
	while(i<len(first)):
		if (first[- i] != "0"):
			first[-1], first[- i] = first[- i],first[-1] # меняем местами значения и выходим
			break
		i+=1
i=1
while(i<=len(first)): # выводим с конца 
	out += first[-i]
	i+=1
if out == second:#сравниваем и выводим 
	print("OK")
else: print("ERROR")
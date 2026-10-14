entrada = input()
entrada_int = list(map(int, entrada.split(" ")))

n = entrada_int[0]
m = entrada_int[1]
soma = 0
for i in reversed(range(m)):
    entrada = input()
    entrada_float = list(map(float, entrada.split(" ")))

    soma += entrada_float[0] * n
    if entrada_float[1] > 0:
        soma += entrada_float[1] * (n * (n-1)/2)
    elif entrada_float[1] == 0:
        continue
    else:
        if n % 2 == 1:
            soma += entrada_float[1] * ((n * n-1) / 4)
        else:
            soma += entrada_float[1] * n * n/4

soma = soma / n
print(soma)
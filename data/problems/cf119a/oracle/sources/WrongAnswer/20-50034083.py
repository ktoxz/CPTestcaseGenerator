a, b, n = map(int, input().split())
# Семен четный 0
# Антиссемкн нечетный 1
ch = 2
# сколько каждый взял из кучки n
d = 0
name = 0

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

while True:
    if ch % 2 == 0:   #семен
        name = 0
        d = gcd(a, n) # количество камней из кучи
        print(ch, name, d, n)
        if d > n:     # проверка камней на наличие в куче
            name = 1
            print(name)
            break
        n -= d
        ch += 1       # следующий игрок
    else:
        name = 1
        d = gcd(b, n)
        print(ch, name, d, n)
        if d > n:     # проверка камней на наличие в куче
            name = 0
            print(name)
            break        
        ch += 1
        n -= d
print(name)
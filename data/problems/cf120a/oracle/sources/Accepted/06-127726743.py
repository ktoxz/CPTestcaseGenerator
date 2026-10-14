import logging

l = logging.Logger("")
h = logging.StreamHandler()
f = logging.Formatter(fmt="[{filename}:{lineno}] {msg}", style="{")
h.setFormatter(f)
l.addHandler(h)
bug = l.info

# To disable uncomment the next line
# bug = lambda x:None

# teste=(1,2,3,4)
# bug(f'{teste=}')
# bug(f'{2*teste=}')

# -------------------------------------------------------------------- #

# entrada da frente, entrada de trás do elevador
# 2 rails -> Rail 1 (esq = frente, dir = trás) | Rail 2 (dir = frente, esq = trás)
# pessoa entra, sabe-se a porta
# ela é destro ou canhoto?

i = open("input.txt", "r")
o = open("output.txt", "a")

door = i.readline().strip()
hand = i.readline().strip()

print(door, hand)

if door == "front":
    if hand == '1':
        o.write('L')

    if hand == '2':
        o.write('R')

if door == "back":
    if hand == '1':
        o.write('R')

    if hand == '2':
        o.write('L')

i.close()
o.close()
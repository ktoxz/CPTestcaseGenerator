nmk = input().split()
n, m, k = int(nmk[0]), int(nmk[1]), float(nmk[2])
d_old = {}
d_new = {}
for i in range(n):
  n,s = input().split()
  if int(s) >= 100:
    d_old[n] = int(int(s) * 0.75)

for j in range(m):
  d_new[input()] = 0

for n,s in d_old.items():
  if n in d_new:
    del d_new[n]
    if s < 100:
      d_old[n] = 0

d_old.update(d_new)
s_d = sorted(d_old.items())
for skill in s_d:
  print(skill[0], skill[1])
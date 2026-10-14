from sys import stdin, stdout
def stdinhack():
  for line in stdin: yield line
next_line = lambda: next(stdinhack()).split()
write = lambda x : stdout.write(x)

def solve ():
  n = int(next_line()[0])
  a = [1,2,3,4,5,6,7,8,9,10,10,10,10]
  ans = 0
  for k in a:
    if(10+k==n): ans+=1
  for k in a:
    if(10+k==n): ans+=1
  for k in a:
    if(10+k==n): ans+=1
  for k in a[:-1]:
    if(10+k==n): ans+=1
  print(ans)
  return

if __name__ == '__main__':
  solve()
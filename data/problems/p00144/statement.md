# Packet Forwarding

- CodeNet ID: `p00144`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

On the Internet, data is divided into packets, and each packet is forwarded to its destination via relay devices called routers. Each router determines the next router to which the packet should be forwarded based on the destination written in the packet. Furthermore, to prevent packets from being forwarded between routers indefinitely, a value called TTL (Time To Live) is attached to each packet. A router decrements the TTL of a received packet by 1; if the result is 0, the packet is discarded; otherwise, it is forwarded to the next router.

Therefore, you are to create a program to assist in network design. Given the network connection information and information about transmitted packets, create a program that outputs the minimum number of routers a packet passes through before arriving at the destination router.

The network consists of multiple routers and cables connecting them, as shown in the figure. Note, however, that each connection (cable) is unidirectional. The network connection information is given as an array of router numbers that each router is directly connected to. If the number of routers is $n$, each router is identified by an integer from 1 to $n$. If there are multiple paths from the source to the destination router, output the value for the path with the fewest number of routers. Additionally, if a packet does not reach the destination, output NA.

For example, consider a network as shown in the figure where the source router is 6 and the destination router is 5. The shortest path is 6 $\to$ 1 $\to$ 5, and the number of routers passed through is 3. In this case, the TTL is decremented at routers 6 and 1 respectively, so the packet can arrive if the TTL at the time of transmission is 3 or more. It is not necessary to decrement the TTL at the destination router. Also, assume there are no packets where the source and destination are the same router.

![Problem diagram 1](images/01.png)

## Input

Input is given in the following format.

```text
n
r1 k1 t11 t12 ... t1k1
r2 k2 t21 t22 ... t2k2
:
rn kn tn1 tn2 ... tnkn
p
s1 d1 v1
s2 d2 v2
:
sp dp vp
```

On the first line, the total number of routers $n$ ($n \le 100$) is given, followed by $n$ lines containing the connection information for the $i$-th router. The connection information consists of the $i$-th router's number $r_i$, the number of routers directly connected to the $i$-th router $k_i$, and the numbers of routers $t_{i1}, t_{i2}, \dots, t_{ik_i}$ to which the $i$-th router can send packets.

On the following line, the number of packets $p$ ($p \le 1000$) is given, followed by $p$ lines containing the information for the $i$-th packet. The packet information consists of the source router number $s_i$, the destination router number $d_i$, and the TTL value $v_i$ ($0 \le v_i \le 10000$).

## Output

For each packet, output the number of routers passed through or NA on a single line.

## Sample Input 1

```text
7
1 4 2 5 4 3
2 1 5
3 1 6
4 1 7
5 2 7 6
6 1 1
7 0
6
1 2 2
1 5 3
1 2 1
5 1 3
6 3 3
1 7 4
```

## Output for the Sample Input 1

```text
2
2
NA
3
3
3
```

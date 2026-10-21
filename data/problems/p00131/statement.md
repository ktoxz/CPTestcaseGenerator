# The Professor's Photoelectric Tube

- CodeNet ID: `p00131`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

Professor: Peter! I've done it!

Peter: Again? What kind of useless invention is it this time?

Professor: I have invented a detector for the phantom elementary particle, the axion!

Peter: Axions... you mean the ones that researchers, including those at CERN (European Organization for Nuclear Research), are desperately chasing? Is it true?

Professor: I'm telling you it's true. To spare you the details, it detects passing axions when a special photoelectric tube containing a very powerful magnetic field lights up.

Peter: If we detect it before anyone else, it would be Nobel Prize-level research, comparable to Professor Koshiba's neutrino detection. We could finally clear the stigma of being a "useless laboratory" that only produces worthless research.

Professor: Exactly. Following Professor Koshiba's "Super-Kamiokande," I have named this device "Tadajao-kande" (if you're going to insult it).

Peter: That's a bit of a stretch... or maybe just self-deprecating...

Professor: Putting that aside, this device has a bit of a quirk. When an axion particle passes through a certain photoelectric tube, due to sensitivity, that tube and its adjacent tubes (up, down, left, and right) will react.

Peter: In other words, if a particle passes through the photoelectric tube marked with ★ on the left side of Figure 1, it will light up as shown on the right side. (The figure is a 5 × 5 example. Black is off, white is on. The same applies hereafter.)

Professor: Furthermore, a "reaction" means the state of the photoelectric tube is toggled. That is, a tube that is off will light up, and a tube that is on will turn off.

Peter: So, if a particle passes through the tubes marked with ★ or ☆ on the left side of Figure 2, it will result in the state shown on the right.

Professor: I have arranged 100 of these in a square (10 × 10) to wait for the particles.

Peter: With such a great invention, the Nobel Prize selection committee will probably call it "Hotchao-kande."

Professor: Oh Peter, it seems you've finally acclimated to the style of my laboratory. I like it. Now, let's start the experiment immediately. First, since the tubes are currently lit randomly, please reset them to a state where all are off so we can begin. All you have to do is think about which photoelectric tubes to hit with axion particles to turn them all off. Simple, right?

Peter: Thinking about it is fine, Professor. But to actually do it, don't we need a device that can generate and fire these phantom axion particles?

Professor: ...

Professor and Peter (simultaneously): Korya-akande! (This is no good!) Hahaha...

---

And so, another day ends harmoniously in the Professor's laboratory, but as usual, no actual progress seems to be made. Since it can't be helped, please create a program on behalf of Peter.

The program should do the following:

A. Input the state of the device's photoelectric tubes as a 10 × 10 array. 0 represents off, and 1 represents on. No data other than 0 and 1 will be included.

B. Calculate and output the positions where axion particles should pass through to turn all the tubes off. This is represented by a 10 × 10 array, the same as the input. "0" means do not pass a particle through, and "1" means pass a particle through. It is guaranteed that there is exactly one way to turn all tubes off.

## Input

Multiple data sets are provided. The number of data sets $n$ ($n \le 20$) is given on the first line. Each data set is given in the following format:

```text
a1,1 a1,2 ... a1,10
a2,1 a2,2 ... a2,10
:
a10,1 a10,2 ... a10,10
```

$a_{i,j}$ represents the state of the photoelectric tube in the $i$-th row and $j$-th column of the device (0 or 1).

## Output

For each data set, output the positions where particles should pass through in the following format:

```text
b1,1 b1,2 ... b1,10
b2,1 b2,2 ... b2,10
:
b10,1 b10,2 ... b10,10
```

$b_{i,j}$ represents whether a particle should pass through the photoelectric tube in the $i$-th row and $j$-th column of the device (0 or 1).

## Sample Input 1

```text
1
0 1 0 0 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 1 0 0 1 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 1 0
```

## Output for the Sample Input 1

```text
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
```

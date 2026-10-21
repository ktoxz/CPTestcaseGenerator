# 立方体の作品

- CodeNet ID: `p00198`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

芸術家品川は n 点の作品を出展するように依頼されました。そこで、立方体の 6 面をペンキで色付けしたものを作品として出展することにしました。作品は、Red、Yellow、Blue、Magenta、Green、Cyan の 6 色全てが使われていて、各面は 1 色で塗りつぶされています。品川は形が同じ立方体の作品でも色の配置の仕方を変え、異なる作品として n 点作成しました。

![Problem diagram 1](images/01.png)

彼の友人であるあなたは、友人のよしみで作品を出展前に閲覧させてもらいましたが、そこであることに気が付きました。それらの作品の中に異なる色付けをされているように見えても、実は同じ色の組み合わせをした立方体が存在していたのです。このままでは、 n 点の作品を出展することできなくなってしまいます。

作成した作品の数と各作品の色の情報を入力とし、出展するためにあと何点必要かを出力するプログラムを作成してください。

立方体の各面の色は c1 から c6 までの記号で表され、 以下のような配置となっています。また、c1 から c6 のそれぞれは Red、Yellow、Blue、Magenta、Green、Cyan のいずれか 1 色となります。

![Problem diagram 2](images/02.png)

## Input

複数のデータセットの並びが入力として与えられます。 入力の終わりはゼロひとつの行で示されます。
各データセットは以下の形式で与えられます。

```text
n
cube1
cube2
:
cuben
```

１行目に作品の数 n (1 ≤ n ≤ 30)、続く n 行に i 番目の作品の情報が与えられます。各作品の情報は次の形式で与えられます。

```text
c1 c2 c3 c4 c5 c6
```

作品の色の配置 ci が空白区切りで与えられます。

データセットの数は 100 を超えません。

## Output

データセットごとに、出展するのにあと何点の作品が必要かを１行に出力します。

## Sample Input 1

```text
3
Cyan Yellow Red Magenta Green Blue
Cyan Yellow Red Magenta Green Blue
Red Yellow Magenta Blue Green Cyan
4
Red Magenta Blue Green Yellow Cyan
Red Yellow Magenta Blue Green Cyan
Magenta Green Red Cyan Yellow Blue
Cyan Green Yellow Blue Magenta Red
0
```

## Output for the Sample Input 1

```text
1
1
```

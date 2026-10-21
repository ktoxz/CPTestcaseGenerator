# 入力候補

- CodeNet ID: `p00242`
- Dataset: `AIZU`
- Time limit: `1000 ms`
- Memory limit: `131072 KB`

携帯電話には、メールなどの文章を効率良く入力するために入力候補を表示する機能が搭載されています。これは、使われる頻度が高い単語を記録しておき、入力された文字を頭文字に持つ単語を入力候補として提示するものです。例えば、普段”computer”という単語を多く入力しているなら、”c”と入力するだけで候補として”computer”が提示されます。このような機能の基本部分を作成してみましょう。

文章、文字を入力とし、その文字を頭文字に持つ単語を出現数の順に出力するプログラムを作成してください。ただし、出現数が同じ単語が複数ある場合は、辞書式順序で出力します。出力する単語は最大5つまでとします。該当する単語が存在しない場合は”NA”と出力してください。

## Input

複数のデータセットが与えられます。入力の終わりはゼロひとつで表されます。各データセットは以下の形式で与えられます。

```text
n
line1
line2
:
linen
k
```

1行目に文章の行数 n (1 ≤ n ≤ 10) が与えられます。続く n 行に文章が与えられます。文章は半角英小文字と半角空白からなり、１行の文字数は1文字以上1024文字以下とします。空白によって区切られる単語は1文字以上20文字以下です。

続く行に頭文字 k が半角英字で与えられます。

データセットの数は 100 を超えません。

## Output

データセットごとに、指定された文字を頭文字にもつ単語または”NA” を出力します。

## Sample Input 1

```text
1
ben likes bananas the best among many fruits because bananas are sweet and cheap
b
1
winners get to visit aizu and the university of aizu and make many friends as well
a
3
ask alex about
the answer for the
assignment on android apps
a
2
programming is both
a sport and an intellectual puzzle
c
0
```

## Output for the Sample Input 1

```text
bananas because ben best
aizu and as
about alex android answer apps
NA
```

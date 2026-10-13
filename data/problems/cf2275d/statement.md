# D. Precision Alignment

- **Nguồn:** [Codeforces 2275D](https://codeforces.com/contest/2275/problem/D)
- **Giới hạn thời gian:** 2 giây
- **Giới hạn bộ nhớ:** 256 MB

## Đề bài

K1o0n phụ trách $n$ phòng thí nghiệm. Phòng thứ $i$ có ba thiết bị đo được phân biệt theo thứ tự, với số đo lần lượt là $a_i$, $b_i$ và $c_i$.

Trong **một thao tác**, chọn một phòng thí nghiệm $i$ và thực hiện **đúng một** trong ba phép cập nhật:

1. $c_i \leftarrow c_i + \operatorname{sgn}(a_i-b_i)$;
2. $b_i \leftarrow b_i + \operatorname{sgn}(a_i-c_i)$;
3. $a_i \leftarrow a_i + \operatorname{sgn}(b_i-c_i)$.

Hàm dấu được định nghĩa như sau:

$$
\operatorname{sgn}(x)=
\begin{cases}
 1 & \text{khi }x>0,\\
 0 & \text{khi }x=0,\\
 -1 & \text{khi }x<0.
\end{cases}
$$

Các thao tác được thực hiện lần lượt; mỗi phép cập nhật sử dụng giá trị của các thiết bị **tại thời điểm thực hiện**. Có thể thao tác nhiều lần trên cùng một phòng hoặc không thao tác trên một số phòng.

Bạn được thực hiện **không quá $k$ thao tác** trên tất cả các phòng thí nghiệm.

Sau khi hoàn tất, đặt

$$
S=\min_{1\le i\le n}(a_i+b_i+c_i).
$$

Hãy tìm **giá trị lớn nhất có thể của $S$**.

## Input

- Dòng đầu tiên chứa số nguyên $t$ ($1\le t\le 10^4$), là số bộ test.
- Với mỗi bộ test:
  - Dòng đầu chứa hai số nguyên $n,k$ ($1\le n\le 2\cdot 10^5$, $0\le k\le 10^{18}$).
  - $n$ dòng tiếp theo, mỗi dòng chứa $a_i,b_i,c_i$ ($-10^9\le a_i,b_i,c_i\le 10^9$).

Bảo đảm tổng $n$ của mọi bộ test không vượt quá $2\cdot 10^5$.

## Output

Với mỗi bộ test, in ra một số nguyên: giá trị $S$ lớn nhất có thể đạt được.

**Lưu ý:** Kết quả có thể vượt giới hạn số nguyên 32-bit; nên sử dụng kiểu số nguyên 64-bit.

## Ví dụ

**Input**

```text
5
3 4
-3 -1 -2
1 3 5
2 4 6
3 4
6 4 2
6 7 0
7 6 0
3 1000000000000000000
4 4 4
1 5 9
-1000000000 0 1000000000
2 4
1 2 3
0 0 5
4 3
2 1 0
4 4 5
1 5 9
7 -2 1
```

**Output**

```text
-2
14
12
6
6
```

## Giải thích ví dụ

- **Test 1:** Thực hiện cập nhật $a_1\leftarrow a_1+\operatorname{sgn}(b_1-c_1)$ bốn lần. Vì $b_1=-1>c_1=-2$, mỗi lần $a_1$ tăng $1$. Bộ ba đầu tiên trở thành $(1,-1,-2)$, có tổng $-2$. Hai bộ ba còn lại có tổng lớn hơn $-2$, nên $S=-2$. Không thể đạt $S\ge -1$ với chỉ 4 thao tác.
- **Test 2:** Có thể đạt $S=14$ bằng cách tăng $a_1$ hai lần, tăng $b_2$ một lần và tăng $c_3$ một lần theo đúng các quy tắc cập nhật.
- **Test 4:** Dù bộ ba thứ hai là $(0,0,5)$ có vẻ khó cải thiện ngay, có thể cập nhật $b_2\leftarrow b_2+\operatorname{sgn}(a_2-c_2)$ để thoát khỏi trạng thái ban đầu, tạo khả năng cải thiện ở các bước sau.

---

*Đề bài được biên soạn lại bằng tiếng Việt từ [Codeforces 2275D – Precision Alignment](https://codeforces.com/contest/2275/problem/D). Không kèm thuật toán hoặc lời giải.*

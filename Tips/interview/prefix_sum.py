"""問題2：区間和（Prefix Sum）
難易度：中級

【問題文】
整数 N、Q が与えられ、続いて N 個の整数 A[i] が与えられる。
続いて Q 個の区間 l r が与えられる。
各区間の合計値を高速に求めよ。

【入力例】
5 3
1 2 3 4 5
1 3
2 5
1 5
【出力例】
6
14
15。"""

import sys
from typing import Any


def main() -> None:
    # 1. Read all input data from standard input
    input_data: list[str] | Any = sys.stdin.read().split()
    if not input_data:
        return

    # 2. Parse variables and arrays
    N = int(input_data[0])
    Q = int(input_data[1])
    A: list[int] = [int(x) for x in input_data[2 : 2 + N]]

    # Compute Prefix Sum
    P: list[int] = [0] * (N + 1)
    for i in range(N):
        P[i + 1] = P[i] + A[i]

    # 3. Process queries and accumulate outputs
    query_idx = 2 + N
    results: list[str] = []
    for _ in range(Q):
        left = int(input_data[query_idx])
        right = int(input_data[query_idx + 1])
        query_idx += 2

        ans = P[right] - P[left - 1]
        results.append(str(ans))

    # 4. Print all results joined by newlines
    print("\n".join(results))


if __name__ == "__main__":
    main()

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
    data: list[str] | Any = sys.stdin.read().split()
    if not data:
        return

    # 2. Parse variables and arrays
    items = int(data[0])
    queries = int(data[1])
    array: list[int] = [int(x) for x in data[2 : 2 + items]]

    # Compute Prefix Sum
    prefix_sum: list[int] = [0] * (items + 1)
    for i in range(items):
        prefix_sum[i + 1] = prefix_sum[i] + array[i]

    # 3. Process queries and accumulate outputs
    idx = 2 + items
    queries_results: list[str] = []
    for _ in range(queries):
        left = int(data[idx])
        right = int(data[idx + 1])
        idx += 2

        sum = prefix_sum[right] - prefix_sum[left - 1]
        queries_results.append(str(sum))

    # 4. Print all queries results joined by newlines
    print("\n".join(queries_results))


if __name__ == "__main__":
    main()

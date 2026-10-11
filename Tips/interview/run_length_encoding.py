"""問題1：文字列圧縮（Run-Length Encoding）
難易度：中級

【問題文】
文字列 S が与えられる。
連続する同じ文字を「文字＋連続数」で圧縮した文字列を出力せよ。

【入力】
AAABCCDDDD
【出力】
A3B1C2D4"""

import sys

input_data = sys.stdin.read().strip()

if input_data.isalpha():
    result: list[str] = []
    count = 1
    for i in range(1, len(input_data)):
        if input_data[i] == input_data[i - 1]:
            count += 1
        else:
            result.append(input_data[i - 1] + str(count))
            count = 1

    result.append(input_data[-1] + str(count))

    print("".join(result))

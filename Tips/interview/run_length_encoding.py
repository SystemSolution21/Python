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
from typing import Any


def run_length_encoding(input_data: str) -> str:
    """Run-Length Encodingを行う関数

    Args:
        input_data (str): 圧縮対象の文字列

    Returns:
        str: 圧縮後の文字列
    """

    # 入力がアルファベット以外の場合は処理を終了する
    if not input_data.isalpha():
        return "入力はアルファベットのみを含む必要があります!"

    # 圧縮処理
    compress: list[str] = []
    count = 1
    for i in range(1, len(input_data)):
        # 同じ文字が連続している場合はカウントを増やす
        if input_data[i] == input_data[i - 1]:
            count += 1
        else:
            # 異なる文字が出てきた場合は、前の文字とカウントを圧縮リストに追加
            compress.append(input_data[i - 1] + str(count))
            count = 1
    # 最後の文字とカウントを圧縮リストに追加
    compress.append(input_data[-1] + str(count))
    # 圧縮リストを結合して文字列として返す
    return "".join(compress)


def main() -> None:
    """メイン関数"""
    # 標準入力から文字列を読み込む
    input_data: str | Any = sys.stdin.readline().strip()
    # 文字列を圧縮する
    result: str = run_length_encoding(input_data)
    # 圧縮後の文字列を出力する
    print(result)


if __name__ == "__main__":
    main()

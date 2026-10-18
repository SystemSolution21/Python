"""問題3：迷路の最短経路（BFS）
難易度：中級

【問題文】
H×W の迷路が与えられる。
0 は通行可能、1 は壁。
左上 (0,0) から右下 (H-1, W-1) までの最短距離を求めよ。
到達不可なら -1 を出力せよ。

Problem Explanation:
Title:Shortest Path in a Maze Breadth-First-Search (BFS)
Difficulty: Intermediate
Problem Statement:
You are given an H×W maze represented as a grid of numbers:
0 represents an open path.1 represents a wall.
Find the shortest distance from the top-left corner (0, 0) to the bottom-right corner (H - 1, W - 1).
If it is impossible to reach the destination, output -1.
＊Note on Shortest Path in Unweighted Grids:
Breadth-First Search (BFS) is the ideal algorithm for this because it explores paths in increasing order of distance.
The first time we reach the destination cell, we are guaranteed to have found the shortest path.

# --- Example Usage ---
3 3
001
100
110
OR
001
100
110
OR
0 0 1
1 0 0
1 1 0
Output: 4

Complexity Analysis:
Time Complexity: 𝑂(𝐻×𝑊)
Every cell in the grid is visited at most once and pushed into the queue,
meaning the traversal runs linearly relative to the total number of cells.
Space Complexity: 𝑂(𝐻×𝑊)
The queue and the dist grid both require space proportional to the size of the maze.
"""

import sys
from collections import deque


def parse_implicit_maze(input_data: str) -> tuple[int, int, list[list[int]]]:
    lines: list[str] = input_data.splitlines()

    # Filter out any accidental empty lines
    lines: list[str] = [line.strip() for line in lines if line.strip()]

    if not lines:
        return 0, 0, []

    # Height is simply the number of rows
    H: int = len(lines)

    # Parse the maze and infer Width from the first row length
    maze: list[list[int]] = []
    for line in lines:
        # Handles space-separated (e.g., "0 0 1") or packed (e.g., "001")
        row: list[int] = (
            [int(x) for x in line.split()] if " " in line else [int(c) for c in line]
        )
        maze.append(row)

    W: int = len(maze[0]) if maze else 0

    return H, W, maze


def parse_maze(input_data: str) -> tuple[int, int, list[list[int]]]:
    """Parse the input data for the maze problem.

    args:
        input_data (str): 標準入力から読み込んだ迷路のデータ

    Returns:
        tuple[int, int, list[list[int]]]: A tuple containing the height (H), width (W),
        and the maze grid as a list of lists of integers.
    """

    # 標準入力から迷路のデータ
    tokens: list[str] = input_data.split()

    if not tokens:
        return 0, 0, []

    # 迷路の高さ・幅・グリッド
    try:
        H, W = int(tokens[0]), int(tokens[1])
    except (IndexError, ValueError):
        return parse_implicit_maze(input_data)

    maze_tokens: list[str] = tokens[2 : 2 + H]

    if H > 0 and W > 0 and len(maze_tokens) == H and len(maze_tokens[0]) == W:
        grid: list[list[int]] = [
            [int(char) for char in row_str] for row_str in maze_tokens
        ]
        return H, W, grid

    return parse_implicit_maze(input_data)


def shortest_path_maze(H: int, W: int, grid: list[list[int]]) -> int:
    """Find the shortest path in a maze using BFS.

    Args:
        H (int): Height of the maze.
        W (int): Width of the maze.
        maze_grid (list[list[int]]): The maze grid where 0 is a path and 1 is a wall.

    Returns:
        int: The length of the shortest path from (0, 0) to (H-1, W-1), or -1 if unreachable.
    """

    # Distance table to track visited cells and minimum steps (-1 means unvisited)
    dist: list[list[int]] = [[-1] * W for _ in range(H)]
    dist[0][0] = 0

    # Queue stores tuples of (row, col)
    q: deque[tuple[int, int]] = deque(iterable=[(0, 0)])

    # Possible directions: Up, Down, Left, Right
    dirs: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while q:
        x, y = q.popleft()

        # Explore all 4 adjacent directions
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            # Check boundaries, wall condition, and whether it has been visited
            if 0 <= nx < H and 0 <= ny < W and grid[nx][ny] == 0 and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))

    return dist[H - 1][W - 1]


def main() -> None:
    """メイン関数"""

    # 標準入力から迷路のデータを読み込む
    input_data: str = sys.stdin.read()

    if not input_data:
        return

    # 迷路のデータを解析して高さ、幅、グリッドを取得する
    H, W, grid = parse_maze(input_data)

    # 迷路の最短経路を計算する
    result: int = shortest_path_maze(H, W, grid)

    # 最短経路の長さを出力する
    print(result)


if __name__ == "__main__":
    main()

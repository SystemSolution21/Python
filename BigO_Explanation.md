# Big O Notation Explained

## Introduction
Big O notation is a mathematical notation used in computer science to describe the performance or complexity of an algorithm. It specifically describes the worst-case scenario and can be used to describe:
- Time complexity: How runtime grows as input size increases
- Space complexity: How memory usage grows as input size increases

## Common Big O Complexities

### O(1) - Constant Time/Space
- Performance is independent of input size
- Examples: Accessing an array element, adding to a stack

### O(log n) - Logarithmic
- Performance increases logarithmically with input size
- Examples: Binary search, balanced binary tree operations

### O(n) - Linear
- Performance grows linearly with input size
- Examples: Simple loops, linear search

### O(n log n) - Linearithmic
- Performance grows by n multiplied by log(n)
- Examples: Efficient sorting algorithms (merge sort, quicksort)

### O(n²) - Quadratic
- Performance grows with the square of input size
- Examples: Nested loops, bubble sort

### O(n³) - Cubic
- Performance grows with the cube of input size
- Examples: Triple nested loops, some matrix operations

### O(2ⁿ) - Exponential
- Performance doubles with each additional input element
- Examples: Recursive Fibonacci without memoization

### O(n!) - Factorial
- Performance grows factorially with input size
- Examples: Brute force traveling salesman problem

## Simplification Rules
1. **Drop constants**: O(2n) → O(n)
2. **Drop lower-order terms**: O(n² + n) → O(n²)
3. **Consider worst-case scenario**: Focus on the upper bound

## Comparing Algorithms
Efficiency ranking (best to worst):
O(1) < O(log n) < O(n) < O(n log n) < O(n²) < O(n³) < O(2ⁿ) < O(n!)

## Practical Examples

### Fibonacci Implementations
1. **Naive Recursive**: O(2ⁿ) time, O(n) space
   ```python
   def fib_naive(n):
       if n <= 1: return n
       return fib_naive(n-1) + fib_naive(n-2)
   ```

2. **Memoized (Top-Down)**: O(n) time, O(n) space
   ```python
   def fib_memo(n, memo={}):
       if n in memo: return memo[n]
       if n <= 1: return n
       memo[n] = fib_memo(n-1) + fib_memo(n-2)
       return memo[n]
   ```

3. **Tabulation (Bottom-Up)**: O(n) time, O(n) space
   ```python
   def fib_tab(n):
       dp = [0] * (n+1)
       dp[1] = 1
       for i in range(2, n+1):
           dp[i] = dp[i-1] + dp[i-2]
       return dp[n]
   ```

4. **Optimized Iterative**: O(n) time, O(1) space
   ```python
   def fib_optimized(n):
       a, b = 0, 1
       for _ in range(n):
           a, b = b, a+b
       return a
   ```

5. **Fibonacci Sequence Generator**: O(log n) time, O(log n) space
   ```python
   def fib_sequence(limit):
       a, b = 0, 1
       result = []
       while a < limit:
           result.append(a)
           a, b = b, a+b
       return result
   ```

## When to Optimize
- Optimize when performance matters for your use case
- Consider both time and space complexity
- Remember: premature optimization is the root of all evil
- Balance code readability with performance needs
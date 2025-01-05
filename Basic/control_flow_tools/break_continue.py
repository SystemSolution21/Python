# break and continue statements

for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, "equals", x, "*", n // x)
            break

# Even and Odd numbers
for n in range(2, 10):
    if n % 2 == 0:  # if even number
        print(f"found an even number {n}")
        continue

    print(f"found an odd number {n}")

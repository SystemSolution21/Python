print("# break and continue statements")

for n in range(2, 100):
    for x in range(2, n):
        if n % x == 0:
            if n % 2 == 0:
                print(x, "*", n // x, "equals", n, "and is an even number")
                break
            else:
                print(x, "*", n // x, "equals", n, "and is an odd number")
            break
    else:
        # This 'else' belongs to the FOR loop, not the IF.
        # It runs only if the loop finishes WITHOUT hitting 'break'.
        if n % 2 == 0:
            print(n, "is a prime number and even")
        else:
            print(n, "is a prime number and odd")


print("\n# Even and Odd numbers")

for n in range(2, 10):
    if n % 2 == 0:  # if even number
        print(f"found an even number {n}")
        continue

    print(f"found an odd number {n}")

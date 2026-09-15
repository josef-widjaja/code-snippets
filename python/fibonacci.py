import sys


def fibonacci(n):
    # Fibonnaci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    # Index (n):          0, 1, 2, 3, 4, 5, 6, 7,  8,  9, ...
    # Fibbonacci(next) = Fibbonacci(curr_fibent) + Fibbonacci(previous)
    # Fibonacci(n) = Fibonacci(n-1) + Fibonacci(n-2)
    # Fibonacci(n+1) = Fibonacci(n) + Fibonacci(n-1)
    
    if n <= 1:
        return n

    curr_fib = 1 # n = 1
    prev_fib = 0 # n = 0

    for i in range(2, n + 1):
        next_fib = curr_fib + prev_fib
        prev_fib = curr_fib
        curr_fib = next_fib
    return curr_fib


def main():
    if len(sys.argv) < 2:
        print("Error: Missing n argument: the nth Fibonacci number to calculate")
        print(f"Usage: python {sys.argv[0]} <n>")
        sys.exit(1)    
    n = int(sys.argv[1])
    if n < 0:
        print("Error: n must be a non-negative integer.")
        sys.exit(1)
    fib_number = fibonacci(n)
    print(fib_number)

if __name__ == "__main__":
    main()

import sys


def fibonacci_series(n):
    # Fibonnaci sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    # Index (n):          0, 1, 2, 3, 4, 5, 6, 7,  8,  9, ...
    # Fibbonacci(next) = Fibbonacci(curr_fibent) + Fibbonacci(previous)
    # Fibonacci(n) = Fibonacci(n-1) + Fibonacci(n-2)
    # Fibonacci(n+1) = Fibonacci(n) + Fibonacci(n-1)

    fib_series = [0, 1] # Start with the first two Fibonacci numbers
    if n <= 1:
        return fib_series [0:n+1]

    curr_fib = 1 # n = 1
    prev_fib = 0 # n = 0

    for i in range(2, n + 1):
        next_fib = curr_fib + prev_fib
        prev_fib = curr_fib
        curr_fib = next_fib
        fib_series.append(curr_fib)
    return fib_series

def main():
    if len(sys.argv) < 2:
        print("Error: Missing n argument: the length of Fibonacci series to print")
        print(f"Usage: python {sys.argv[0]} <n>")
        sys.exit(1)    
    n = int(sys.argv[1])
    if n < 0:
        print("Error: n must be a non-negative integer.")
        sys.exit(1)

    fib_sequence = fibonacci_series(n)
    print(fib_sequence)

if __name__ == "__main__":
    main()

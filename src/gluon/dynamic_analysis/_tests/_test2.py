def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def compute_math_series(n):
    fact = factorial(n)
    fib = fibonacci(n)
    return fact + fib

def process_number(x):
    result = compute_math_series(x)
    return result

def main():
    number = 5
    final_result = process_number(number)
    print(f"\nFor n = {number}:")
    print(f"Factorial({number}) + Fibonacci({number}) = {final_result}")
    print(f"({factorial(number)} + {fibonacci(number)} = {final_result})")

if __name__ == "__main__":
    main()
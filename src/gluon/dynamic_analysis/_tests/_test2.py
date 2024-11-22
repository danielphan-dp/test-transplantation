from gluon.dynamic_analysis.hooks.print_stack_trace import print_stack_trace

@print_stack_trace()
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

@print_stack_trace()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

@print_stack_trace()
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
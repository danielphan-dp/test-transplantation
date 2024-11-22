from gluon.dynamic_analysis.hooks.print_stack_trace import print_stack_trace


def calculate_total(x, y):
    return x + y


@print_stack_trace
def process_numbers(a, b):
    result = calculate_total(a, b)
    return result


def main():
    value1 = 10
    value2 = 20
    final_result = process_numbers(value1, value2)
    print(f"The total is: {final_result}")


if __name__ == "__main__":
    main()

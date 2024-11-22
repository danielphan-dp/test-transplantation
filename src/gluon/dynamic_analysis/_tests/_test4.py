def process_payment(amount, tax):
    return calculate_total(amount, tax)

def validate_input(amount, tax):
    if amount < 0 or tax < 0:
        raise ValueError("Negative values not allowed")
    return process_payment(amount, tax)

def apply_discount(amount, tax, discount):
    final_amount = amount * (1 - discount)
    return validate_input(final_amount, tax)

def handle_transaction(user_id, amount, tax):
    discount = get_user_discount(user_id)
    return apply_discount(amount, tax, discount)

def get_user_discount(user_id):
    return 0.1 if user_id > 1000 else 0.05

def prepare_transaction(user_id, cart_items):
    amount = sum_cart_items(cart_items)
    tax = calculate_tax_rate(user_id)
    return handle_transaction(user_id, amount, tax)

def sum_cart_items(items):
    return sum(items)

def calculate_tax_rate(user_id):
    return 0.15 if user_id > 1000 else 0.10

def process_order(user_id, items):
    return prepare_transaction(user_id, items)

def calculate_total(amount, tax):
    """Final calculation of total amount with tax"""
    return amount * (1 + tax)

def main():
    user_id = 1500
    cart_items = [100, 200, 300, 400]
    
    final_amount = process_order(user_id, cart_items)
    
    print(f"\nOrder Summary:")
    print(f"User ID: {user_id}")
    print(f"Cart Items: {cart_items}")
    print(f"Final Amount: ${final_amount:.2f}")

if __name__ == "__main__":
    main()

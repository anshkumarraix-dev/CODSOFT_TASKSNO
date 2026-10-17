"""
CodSoft Python Programming Internship - Task 2: Calculator
Takes two numbers and an operation choice, performs the calculation,
and displays the result.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return None  # signals division by zero
    return a / b


def power(a, b):
    return a ** b


def modulus(a, b):
    if b == 0:
        return None
    return a % b


OPERATIONS = {
    "1": ("Addition", "+", add),
    "2": ("Subtraction", "-", subtract),
    "3": ("Multiplication", "*", multiply),
    "4": ("Division", "/", divide),
    "5": ("Power", "**", power),
    "6": ("Modulus", "%", modulus),
}


def get_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        value = input(prompt).strip()
        try:
            return float(value)
        except ValueError:
            print("  Invalid input. Please enter a valid number.")


def show_menu():
    print("\nSelect an operation:")
    for key, (name, symbol, _) in OPERATIONS.items():
        print(f"  {key}. {name} ({symbol})")


def format_number(n):
    """Show 5.0 as 5, but keep 5.25 as 5.25."""
    return int(n) if n == int(n) else round(n, 6)


def calculator():
    print("=" * 36)
    print("        SIMPLE CALCULATOR")
    print("=" * 36)

    while True:
        num1 = get_number("\nEnter first number: ")
        num2 = get_number("Enter second number: ")

        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice not in OPERATIONS:
            print("  Invalid choice. Please select a number from 1 to 6.")
        else:
            name, symbol, func = OPERATIONS[choice]
            result = func(num1, num2)

            if result is None:
                print("  Error: Cannot divide by zero.")
            else:
                print(
                    f"\n  Result: {format_number(num1)} {symbol} "
                    f"{format_number(num2)} = {format_number(result)}"
                )

        again = input("\nDo you want to calculate again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("\nThank you for using the calculator. Goodbye!")
            break


if __name__ == "__main__":
    calculator()

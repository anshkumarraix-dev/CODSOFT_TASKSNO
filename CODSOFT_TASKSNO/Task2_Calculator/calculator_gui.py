"""
CodSoft Python Programming Internship - Task 2: Calculator (GUI version)
Built with Tkinter (included with Python, no installation needed).
Enter two numbers, choose an operation, and click Calculate.
"""

import tkinter as tk
from tkinter import ttk


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b


def power(a, b):
    return a ** b


def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a % b


OPERATIONS = {
    "Addition (+)": ("+", add),
    "Subtraction (-)": ("-", subtract),
    "Multiplication (*)": ("*", multiply),
    "Division (/)": ("/", divide),
    "Power (**)": ("**", power),
    "Modulus (%)": ("%", modulus),
}


def format_number(n):
    """Show 5.0 as 5, but keep 5.25 as 5.25."""
    if isinstance(n, complex):
        return str(n)
    return int(n) if n == int(n) else round(n, 6)


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        root.title("Simple Calculator")
        root.geometry("380x420")
        root.resizable(False, False)

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Simple Calculator", font=("Segoe UI", 18, "bold")).pack(
            pady=(0, 15)
        )

        # Number 1
        ttk.Label(main, text="First number:").pack(anchor="w")
        self.entry1 = ttk.Entry(main, font=("Segoe UI", 12))
        self.entry1.pack(fill="x", pady=(2, 10))

        # Number 2
        ttk.Label(main, text="Second number:").pack(anchor="w")
        self.entry2 = ttk.Entry(main, font=("Segoe UI", 12))
        self.entry2.pack(fill="x", pady=(2, 10))

        # Operation
        ttk.Label(main, text="Operation:").pack(anchor="w")
        self.operation = ttk.Combobox(
            main, values=list(OPERATIONS.keys()), state="readonly", font=("Segoe UI", 11)
        )
        self.operation.current(0)
        self.operation.pack(fill="x", pady=(2, 15))

        # Buttons
        buttons = ttk.Frame(main)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="Calculate", command=self.calculate).pack(
            side="left", expand=True, fill="x", padx=(0, 5)
        )
        ttk.Button(buttons, text="Clear", command=self.clear).pack(
            side="left", expand=True, fill="x", padx=(5, 0)
        )

        # Result
        self.result_var = tk.StringVar(value="Result will appear here")
        self.result_label = tk.Label(
            main,
            textvariable=self.result_var,
            font=("Segoe UI", 13, "bold"),
            fg="#555555",
            wraplength=330,
            pady=20,
        )
        self.result_label.pack(fill="x")

        # Press Enter to calculate
        root.bind("<Return>", lambda event: self.calculate())
        self.entry1.focus()

    def show(self, text, color):
        self.result_var.set(text)
        self.result_label.config(fg=color)

    def calculate(self):
        try:
            num1 = float(self.entry1.get().strip())
            num2 = float(self.entry2.get().strip())
        except ValueError:
            self.show("Error: please enter valid numbers.", "#c0392b")
            return

        symbol, func = OPERATIONS[self.operation.get()]

        try:
            result = func(num1, num2)
        except ZeroDivisionError:
            self.show("Error: cannot divide by zero.", "#c0392b")
            return
        except OverflowError:
            self.show("Error: result is too large.", "#c0392b")
            return

        self.show(
            f"{format_number(num1)} {symbol} {format_number(num2)} = {format_number(result)}",
            "#1e8449",
        )

    def clear(self):
        self.entry1.delete(0, tk.END)
        self.entry2.delete(0, tk.END)
        self.operation.current(0)
        self.show("Result will appear here", "#555555")
        self.entry1.focus()


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()

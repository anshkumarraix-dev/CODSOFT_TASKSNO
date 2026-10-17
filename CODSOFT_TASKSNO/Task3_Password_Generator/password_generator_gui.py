"""
CodSoft Python Programming Internship - Task 3: Password Generator (GUI version)
Built with Tkinter (included with Python, no installation needed).
Uses the 'secrets' module for cryptographically secure randomness.
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox

MIN_LENGTH = 4
MAX_LENGTH = 64
AMBIGUOUS = "O0oIl1"
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def build_pools(use_lower, use_upper, use_digits, use_symbols, exclude_ambiguous):
    """Return a list of character pools, one per selected type."""
    sources = [
        (use_lower, string.ascii_lowercase),
        (use_upper, string.ascii_uppercase),
        (use_digits, string.digits),
        (use_symbols, SYMBOLS),
    ]
    pools = []
    for selected, chars in sources:
        if selected:
            if exclude_ambiguous:
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)
    return pools


def generate_password(length, pools):
    """Generate a password with at least one character from every pool."""
    password = [secrets.choice(pool) for pool in pools][:length]
    all_chars = "".join(pools)
    password += [secrets.choice(all_chars) for _ in range(length - len(password))]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def rate_strength(length, pools):
    """Return (label, color) based on length and character variety."""
    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    score += len(pools) - 1

    if score <= 2:
        return "Weak", "#c0392b"
    if score <= 4:
        return "Good", "#d68910"
    return "Strong", "#1e8449"


class PasswordApp:
    def __init__(self, root):
        self.root = root
        root.title("Password Generator")
        root.geometry("440x520")
        root.resizable(False, False)

        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Password Generator", font=("Segoe UI", 18, "bold")).pack(
            pady=(0, 15)
        )

        # Length slider
        length_frame = ttk.Frame(main)
        length_frame.pack(fill="x")
        ttk.Label(length_frame, text="Password length:").pack(side="left")
        self.length_var = tk.IntVar(value=12)
        self.length_display = ttk.Label(
            length_frame, text="12", font=("Segoe UI", 11, "bold")
        )
        self.length_display.pack(side="right")

        self.slider = ttk.Scale(
            main,
            from_=MIN_LENGTH,
            to=MAX_LENGTH,
            orient="horizontal",
            command=self.on_slide,
        )
        self.slider.set(12)
        self.slider.pack(fill="x", pady=(5, 15))

        # Character options
        options = ttk.LabelFrame(main, text="Include characters", padding=10)
        options.pack(fill="x")

        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            options, text="Lowercase letters (a-z)", variable=self.use_lower
        ).pack(anchor="w")
        ttk.Checkbutton(
            options, text="Uppercase letters (A-Z)", variable=self.use_upper
        ).pack(anchor="w")
        ttk.Checkbutton(options, text="Numbers (0-9)", variable=self.use_digits).pack(
            anchor="w"
        )
        ttk.Checkbutton(
            options, text="Symbols (!@#$...)", variable=self.use_symbols
        ).pack(anchor="w")
        ttk.Separator(options).pack(fill="x", pady=6)
        ttk.Checkbutton(
            options,
            text="Exclude look-alike characters (O, 0, l, 1, I)",
            variable=self.exclude_ambiguous,
        ).pack(anchor="w")

        # Generate button
        ttk.Button(main, text="Generate Password", command=self.generate).pack(
            fill="x", pady=15
        )

        # Output
        self.password_var = tk.StringVar()
        self.output = ttk.Entry(
            main,
            textvariable=self.password_var,
            font=("Consolas", 13),
            justify="center",
            state="readonly",
        )
        self.output.pack(fill="x", ipady=6)

        self.strength_label = tk.Label(main, text="", font=("Segoe UI", 11, "bold"))
        self.strength_label.pack(pady=8)

        ttk.Button(main, text="Copy to Clipboard", command=self.copy).pack(fill="x")

        self.status = tk.Label(main, text="", fg="#1e8449", font=("Segoe UI", 10))
        self.status.pack(pady=5)

    def on_slide(self, value):
        length = int(float(value))
        self.length_var.set(length)
        self.length_display.config(text=str(length))

    def generate(self):
        pools = build_pools(
            self.use_lower.get(),
            self.use_upper.get(),
            self.use_digits.get(),
            self.use_symbols.get(),
            self.exclude_ambiguous.get(),
        )
        if not pools:
            messagebox.showwarning(
                "No character type selected",
                "Please select at least one character type.",
            )
            return

        length = self.length_var.get()
        self.password_var.set(generate_password(length, pools))

        label, color = rate_strength(length, pools)
        self.strength_label.config(text=f"Strength: {label}", fg=color)
        self.status.config(text="")

    def copy(self):
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to copy", "Generate a password first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.status.config(text="Copied to clipboard!")
        self.root.after(2000, lambda: self.status.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    PasswordApp(root)
    root.mainloop()

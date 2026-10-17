"""
CodSoft Python Programming Internship - Task 3: Password Generator
Prompts for length and complexity, generates a random password,
and displays it. Uses the 'secrets' module for cryptographically
secure randomness.
"""

import secrets
import string

MIN_LENGTH = 4
MAX_LENGTH = 128

# Characters that are easy to confuse when reading (optional to exclude)
AMBIGUOUS = "O0oIl1"


def get_length():
    """Ask for the password length until a valid number is entered."""
    while True:
        value = input(f"Enter password length ({MIN_LENGTH}-{MAX_LENGTH}): ").strip()
        if not value.isdigit():
            print("  Invalid input. Please enter a whole number.")
            continue
        length = int(value)
        if MIN_LENGTH <= length <= MAX_LENGTH:
            return length
        print(f"  Length must be between {MIN_LENGTH} and {MAX_LENGTH}.")


def ask_yes_no(prompt, default=True):
    """Ask a yes/no question. Pressing Enter picks the default."""
    hint = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{prompt} [{hint}]: ").strip().lower()
        if answer == "":
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer with yes or no.")


def choose_complexity():
    """Let the user pick a preset or build a custom character set."""
    print("\nSelect password complexity:")
    print("  1. Low     (letters only)")
    print("  2. Medium  (letters + numbers)")
    print("  3. High    (letters + numbers + symbols)")
    print("  4. Custom  (choose each character type)")

    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            return {"lower": True, "upper": True, "digits": False, "symbols": False}
        if choice == "2":
            return {"lower": True, "upper": True, "digits": True, "symbols": False}
        if choice == "3":
            return {"lower": True, "upper": True, "digits": True, "symbols": True}
        if choice == "4":
            while True:
                options = {
                    "lower": ask_yes_no("  Include lowercase letters (a-z)?"),
                    "upper": ask_yes_no("  Include uppercase letters (A-Z)?"),
                    "digits": ask_yes_no("  Include numbers (0-9)?"),
                    "symbols": ask_yes_no("  Include symbols (!@#$...)?"),
                }
                if any(options.values()):
                    return options
                print("  You must select at least one character type.")
        print("  Invalid choice. Please enter a number from 1 to 4.")


def build_pools(options, exclude_ambiguous):
    """Return a list of character pools, one per selected type."""
    sources = {
        "lower": string.ascii_lowercase,
        "upper": string.ascii_uppercase,
        "digits": string.digits,
        "symbols": "!@#$%^&*()-_=+[]{};:,.<>?/",
    }
    pools = []
    for key, chars in sources.items():
        if options[key]:
            if exclude_ambiguous:
                chars = "".join(c for c in chars if c not in AMBIGUOUS)
            pools.append(chars)
    return pools


def generate_password(length, pools):
    """
    Build a password of the given length that contains at least one
    character from every selected pool (when length allows it).
    """
    # Guarantee one character from each pool
    password = [secrets.choice(pool) for pool in pools][:length]

    # Fill the rest from the combined pool
    all_chars = "".join(pools)
    password += [secrets.choice(all_chars) for _ in range(length - len(password))]

    # Shuffle securely so guaranteed characters aren't always at the start
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def rate_strength(length, pools):
    """Give a simple strength rating based on length and variety."""
    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    score += len(pools) - 1  # extra points for variety

    if score <= 2:
        return "Weak"
    if score <= 4:
        return "Good"
    return "Strong"


def main():
    print("=" * 38)
    print("         PASSWORD GENERATOR")
    print("=" * 38)

    while True:
        length = get_length()
        options = choose_complexity()
        exclude_ambiguous = ask_yes_no(
            "\nExclude look-alike characters (O, 0, l, 1, I)?", default=False
        )

        pools = build_pools(options, exclude_ambiguous)
        password = generate_password(length, pools)

        print("\n" + "-" * 38)
        print(f"  Generated Password: {password}")
        print(f"  Length            : {len(password)}")
        print(f"  Strength          : {rate_strength(length, pools)}")
        print("-" * 38)

        if not ask_yes_no("\nGenerate another password?", default=False):
            print("\nThank you for using the Password Generator. Stay safe!")
            break
        print()


if __name__ == "__main__":
    main()

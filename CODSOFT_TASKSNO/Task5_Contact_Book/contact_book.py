"""
CodSoft Python Programming Internship - Task 5: Contact Book
Features: add, view, search, update and delete contacts.
Contacts are saved in a JSON file so they persist between runs.
"""

import json
import os

FILE_NAME = "contacts.json"


# ---------- File handling ----------

def load_contacts():
    """Load contacts from the JSON file (empty list if none exists)."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read contacts file. Starting with an empty list.")
        return []


def save_contacts(contacts):
    """Save contacts to the JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


# ---------- Helpers ----------

def get_required(prompt):
    """Keep asking until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


def get_phone(prompt, allow_blank=False):
    """Ask for a phone number; accepts digits with optional + - and spaces."""
    while True:
        value = input(prompt).strip()
        if allow_blank and value == "":
            return ""
        digits = value.replace("+", "").replace("-", "").replace(" ", "")
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return value
        print("  Invalid phone number. Enter 7-15 digits.")


def get_email(prompt, allow_blank=False):
    """Ask for an email with a basic format check (optional field)."""
    while True:
        value = input(prompt).strip()
        if value == "":
            return ""
        if "@" in value and "." in value.split("@")[-1] and " " not in value:
            return value
        print("  Invalid email format (example: name@example.com).")


def print_contact(index, c):
    print(f"\n  [{index}] {c['name']}")
    print(f"      Phone  : {c['phone']}")
    print(f"      Email  : {c['email'] or '-'}")
    print(f"      Address: {c['address'] or '-'}")


def find_matches(contacts, query):
    """Return list of (index, contact) where name or phone contains the query."""
    query = query.lower()
    return [
        (i, c)
        for i, c in enumerate(contacts)
        if query in c["name"].lower() or query in c["phone"].lower()
    ]


def choose_contact(contacts):
    """Search and let the user pick one contact. Returns its index or None."""
    query = get_required("Enter name or phone number to search: ")
    matches = find_matches(contacts, query)

    if not matches:
        print("  No matching contact found.")
        return None
    if len(matches) == 1:
        return matches[0][0]

    print(f"\n  {len(matches)} contacts found:")
    for n, (_, c) in enumerate(matches, start=1):
        print(f"    {n}. {c['name']} - {c['phone']}")

    while True:
        pick = input("Select a number (or 0 to cancel): ").strip()
        if pick == "0":
            return None
        if pick.isdigit() and 1 <= int(pick) <= len(matches):
            return matches[int(pick) - 1][0]
        print("  Invalid selection.")


# ---------- Core features ----------

def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = get_required("Name: ")
    phone = get_phone("Phone number: ")
    email = get_email("Email (optional): ")
    address = input("Address (optional): ").strip()

    contacts.append(
        {"name": name, "phone": phone, "email": email, "address": address}
    )
    save_contacts(contacts)
    print(f"\n  Contact '{name}' added successfully!")


def view_contacts(contacts):
    print("\n--- Contact List ---")
    if not contacts:
        print("  No contacts saved yet.")
        return

    sorted_contacts = sorted(contacts, key=lambda c: c["name"].lower())
    for n, c in enumerate(sorted_contacts, start=1):
        print(f"  {n}. {c['name']:<20} {c['phone']}")
    print(f"\n  Total contacts: {len(contacts)}")


def search_contact(contacts):
    print("\n--- Search Contact ---")
    if not contacts:
        print("  No contacts saved yet.")
        return

    query = get_required("Enter name or phone number: ")
    matches = find_matches(contacts, query)

    if not matches:
        print("  No matching contact found.")
        return

    print(f"\n  Found {len(matches)} contact(s):")
    for i, c in matches:
        print_contact(i + 1, c)


def update_contact(contacts):
    print("\n--- Update Contact ---")
    if not contacts:
        print("  No contacts saved yet.")
        return

    index = choose_contact(contacts)
    if index is None:
        return

    c = contacts[index]
    print("\n  Current details:")
    print_contact(index + 1, c)
    print("\n  Press Enter to keep the current value.")

    new_name = input(f"Name [{c['name']}]: ").strip()
    new_phone = get_phone(f"Phone [{c['phone']}]: ", allow_blank=True)
    new_email = input(f"Email [{c['email'] or '-'}]: ").strip()
    new_address = input(f"Address [{c['address'] or '-'}]: ").strip()

    if new_email and not ("@" in new_email and "." in new_email.split("@")[-1]):
        print("  Invalid email ignored. Keeping the old one.")
        new_email = ""

    if new_name:
        c["name"] = new_name
    if new_phone:
        c["phone"] = new_phone
    if new_email:
        c["email"] = new_email
    if new_address:
        c["address"] = new_address

    save_contacts(contacts)
    print("\n  Contact updated successfully!")


def delete_contact(contacts):
    print("\n--- Delete Contact ---")
    if not contacts:
        print("  No contacts saved yet.")
        return

    index = choose_contact(contacts)
    if index is None:
        return

    c = contacts[index]
    confirm = input(f"Delete '{c['name']}'? (yes/no): ").strip().lower()
    if confirm in ("yes", "y"):
        contacts.pop(index)
        save_contacts(contacts)
        print("\n  Contact deleted successfully!")
    else:
        print("  Deletion cancelled.")


# ---------- Main menu ----------

def main():
    contacts = load_contacts()

    actions = {
        "1": add_contact,
        "2": view_contacts,
        "3": search_contact,
        "4": update_contact,
        "5": delete_contact,
    }

    while True:
        print("\n" + "=" * 36)
        print("           CONTACT BOOK")
        print("=" * 36)
        print("  1. Add Contact")
        print("  2. View Contact List")
        print("  3. Search Contact")
        print("  4. Update Contact")
        print("  5. Delete Contact")
        print("  6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "6":
            print("\nGoodbye!")
            break
        elif choice in actions:
            actions[choice](contacts)
        else:
            print("  Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

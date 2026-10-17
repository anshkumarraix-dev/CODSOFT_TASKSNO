"""
CodSoft Python Programming Internship - Task 5: Contact Book (GUI version)
Built with Tkinter (included with Python, no installation needed).
Features: add, view, search, update and delete contacts.
Contacts are saved in contacts.json so they persist between runs.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "contacts.json"


# ---------- File handling ----------

def load_contacts():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        messagebox.showwarning(
            "Warning", "Could not read the contacts file. Starting with an empty list."
        )
        return []


def save_contacts(contacts):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


# ---------- Validation ----------

def valid_phone(value):
    digits = value.replace("+", "").replace("-", "").replace(" ", "")
    return digits.isdigit() and 7 <= len(digits) <= 15


def valid_email(value):
    if value == "":
        return True  # email is optional
    return "@" in value and "." in value.split("@")[-1] and " " not in value


# ---------- GUI ----------

class ContactBookApp:
    def __init__(self, root):
        self.root = root
        root.title("Contact Book")
        root.geometry("780x500")
        root.minsize(700, 450)

        self.contacts = load_contacts()
        self.selected_index = None  # index in self.contacts

        container = ttk.Frame(root, padding=15)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(0, weight=1)

        # ----- Left side: search + list -----
        left = ttk.Frame(container)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)

        ttk.Label(left, text="Contacts", font=("Segoe UI", 16, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        search_frame = ttk.Frame(left)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        search_frame.columnconfigure(1, weight=1)
        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 6))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_list())
        ttk.Entry(search_frame, textvariable=self.search_var).grid(
            row=0, column=1, sticky="ew"
        )
        ttk.Button(search_frame, text="X", width=3, command=self.clear_search).grid(
            row=0, column=2, padx=(6, 0)
        )

        tree_frame = ttk.Frame(left)
        tree_frame.grid(row=2, column=0, sticky="nsew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame, columns=("name", "phone"), show="headings", selectmode="browse"
        )
        self.tree.heading("name", text="Name")
        self.tree.heading("phone", text="Phone")
        self.tree.column("name", width=180)
        self.tree.column("phone", width=130)
        self.tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.count_label = ttk.Label(left, text="")
        self.count_label.grid(row=3, column=0, sticky="w", pady=(6, 0))

        # ----- Right side: form -----
        right = ttk.LabelFrame(container, text="Contact Details", padding=12)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        ttk.Label(right, text="Name *").grid(row=0, column=0, sticky="w")
        ttk.Entry(right, textvariable=self.name_var).grid(
            row=1, column=0, sticky="ew", pady=(0, 8)
        )

        ttk.Label(right, text="Phone *").grid(row=2, column=0, sticky="w")
        ttk.Entry(right, textvariable=self.phone_var).grid(
            row=3, column=0, sticky="ew", pady=(0, 8)
        )

        ttk.Label(right, text="Email").grid(row=4, column=0, sticky="w")
        ttk.Entry(right, textvariable=self.email_var).grid(
            row=5, column=0, sticky="ew", pady=(0, 8)
        )

        ttk.Label(right, text="Address").grid(row=6, column=0, sticky="w")
        self.address_text = tk.Text(right, height=4, width=25, wrap="word")
        self.address_text.grid(row=7, column=0, sticky="ew", pady=(0, 12))

        btn_frame = ttk.Frame(right)
        btn_frame.grid(row=8, column=0, sticky="ew")
        btn_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(btn_frame, text="Add", command=self.add_contact).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=(0, 6)
        )
        ttk.Button(btn_frame, text="Update", command=self.update_contact).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=(0, 6)
        )
        ttk.Button(btn_frame, text="Delete", command=self.delete_contact).grid(
            row=1, column=0, sticky="ew", padx=(0, 4)
        )
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_form).grid(
            row=1, column=1, sticky="ew", padx=(4, 0)
        )

        self.status_var = tk.StringVar(value="* required fields")
        ttk.Label(right, textvariable=self.status_var, foreground="#555555").grid(
            row=9, column=0, sticky="w", pady=(12, 0)
        )

        self.refresh_list()

    # ----- Helpers -----

    def get_form(self):
        return {
            "name": self.name_var.get().strip(),
            "phone": self.phone_var.get().strip(),
            "email": self.email_var.get().strip(),
            "address": self.address_text.get("1.0", tk.END).strip(),
        }

    def set_form(self, contact):
        self.name_var.set(contact["name"])
        self.phone_var.set(contact["phone"])
        self.email_var.set(contact["email"])
        self.address_text.delete("1.0", tk.END)
        self.address_text.insert("1.0", contact["address"])

    def validate(self, data):
        if not data["name"]:
            messagebox.showerror("Invalid input", "Name cannot be empty.")
            return False
        if not valid_phone(data["phone"]):
            messagebox.showerror(
                "Invalid input", "Enter a valid phone number (7-15 digits)."
            )
            return False
        if not valid_email(data["email"]):
            messagebox.showerror(
                "Invalid input", "Enter a valid email (example: name@example.com)."
            )
            return False
        return True

    def refresh_list(self):
        """Rebuild the list, filtered by the search box and sorted by name."""
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()

        shown = 0
        for i, c in sorted(
            enumerate(self.contacts), key=lambda item: item[1]["name"].lower()
        ):
            if query and query not in c["name"].lower() and query not in c["phone"].lower():
                continue
            # iid is the contact's index in self.contacts
            self.tree.insert("", "end", iid=str(i), values=(c["name"], c["phone"]))
            shown += 1

        self.count_label.config(text=f"Showing {shown} of {len(self.contacts)} contacts")

    # ----- Events -----

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_index = int(selection[0])
        self.set_form(self.contacts[self.selected_index])
        self.status_var.set("Editing selected contact")

    def clear_search(self):
        self.search_var.set("")

    def clear_form(self):
        self.selected_index = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_text.delete("1.0", tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.status_var.set("* required fields")

    # ----- Actions -----

    def add_contact(self):
        data = self.get_form()
        if not self.validate(data):
            return
        self.contacts.append(data)
        save_contacts(self.contacts)
        self.refresh_list()
        self.clear_form()
        self.status_var.set(f"Added '{data['name']}'")

    def update_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("No contact selected", "Select a contact to update.")
            return
        data = self.get_form()
        if not self.validate(data):
            return
        self.contacts[self.selected_index] = data
        save_contacts(self.contacts)
        self.refresh_list()
        self.clear_form()
        self.status_var.set(f"Updated '{data['name']}'")

    def delete_contact(self):
        if self.selected_index is None:
            messagebox.showinfo("No contact selected", "Select a contact to delete.")
            return
        name = self.contacts[self.selected_index]["name"]
        if messagebox.askyesno("Confirm delete", f"Delete '{name}'?"):
            self.contacts.pop(self.selected_index)
            save_contacts(self.contacts)
            self.refresh_list()
            self.clear_form()
            self.status_var.set(f"Deleted '{name}'")


if __name__ == "__main__":
    root = tk.Tk()
    ContactBookApp(root)
    root.mainloop()

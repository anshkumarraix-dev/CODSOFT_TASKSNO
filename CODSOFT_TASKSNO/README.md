# CodSoft Python Programming Internship

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![Internship](https://img.shields.io/badge/CodSoft-Internship-purple)
![Tasks](https://img.shields.io/badge/Tasks%20Completed-3-brightgreen)

Projects completed during my **Python Programming virtual internship at [CodSoft](https://www.codsoft.in)**
(05 October 2026 – 05 November 2026).

**Intern:** Ansh Kumar Rai  |  **Intern ID:** BY26RY240071

Each project comes in **two versions**: a command-line (CLI) version and a graphical (GUI) version built with Tkinter.

---

## Table of Contents

- [Projects](#projects)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Project Details](#project-details)
- [Connect With Me](#connect-with-me)

---

## Projects

| Task | Project | CLI version | GUI version |
|------|---------|-------------|-------------|
| 2 | Calculator | `Task2_Calculator/calculator.py` | `Task2_Calculator/calculator_gui.py` |
| 3 | Password Generator | `Task3_Password_Generator/password_generator.py` | `Task3_Password_Generator/password_generator_gui.py` |
| 5 | Contact Book | `Task5_Contact_Book/contact_book.py` | `Task5_Contact_Book/contact_book_gui.py` |

## Requirements

- Python 3.8 or higher
- No external libraries needed. Everything uses the Python standard library.
- Tkinter (for the GUI versions) is bundled with Python on Windows and macOS.
  On Linux, install it with: `sudo apt install python3-tk`

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/anshkumarraix-dev/CODSOFT_TASKSNO.git
cd CODSOFT_TASKSNO

# 2. Run any project (examples)
python Task2_Calculator/calculator_gui.py
python Task3_Password_Generator/password_generator.py
python Task5_Contact_Book/contact_book_gui.py
```

> On some systems, use `python3` instead of `python`.

## Project Structure

```
CODSOFT_TASKSNO/
├── README.md
├── .gitignore
├── Task2_Calculator/
│   ├── calculator.py
│   └── calculator_gui.py
├── Task3_Password_Generator/
│   ├── password_generator.py
│   └── password_generator_gui.py
└── Task5_Contact_Book/
    ├── contact_book.py
    └── contact_book_gui.py
```

## Project Details

<details>
<summary><b>Task 2: Calculator</b> (click to expand)</summary>

<br>

Takes two numbers and an operation choice, performs the calculation, and displays the result.

**Features**
- Addition, subtraction, multiplication, division, power, and modulus
- Input validation (invalid numbers don't crash the program)
- Division-by-zero handling
- CLI: "calculate again?" loop
- GUI: dropdown for the operation, Enter key to calculate, colour-coded results

**Run**
```bash
python Task2_Calculator/calculator.py       # CLI
python Task2_Calculator/calculator_gui.py   # GUI
```

</details>

<details>
<summary><b>Task 3: Password Generator</b> (click to expand)</summary>

<br>

Generates strong random passwords of a length and complexity chosen by the user.

**Features**
- Length from 4 to 128 characters (GUI slider: 4 to 64)
- Complexity presets (CLI) or per-type checkboxes (GUI): lowercase, uppercase, numbers, symbols
- Guarantees at least one character of every selected type
- Uses Python's `secrets` module (cryptographically secure) instead of `random`
- Option to exclude look-alike characters (`O`, `0`, `l`, `1`, `I`)
- Strength rating, plus a Copy to Clipboard button in the GUI

**Run**
```bash
python Task3_Password_Generator/password_generator.py       # CLI
python Task3_Password_Generator/password_generator_gui.py   # GUI
```

</details>

<details>
<summary><b>Task 5: Contact Book</b> (click to expand)</summary>

<br>

Stores and manages contacts (name, phone, email, address).

**Features**
- Add, view, search, update, and delete contacts
- Search by name or phone number (partial matches work)
- Phone and email validation
- Data saved to `contacts.json`, so contacts persist between runs
- GUI: live search filtering and click-to-edit form

**Run**
```bash
python Task5_Contact_Book/contact_book.py       # CLI
python Task5_Contact_Book/contact_book_gui.py   # GUI
```

> `contacts.json` is created automatically in the folder you run the program from,
> and it is listed in `.gitignore` so personal data is never uploaded.

</details>

## Concepts Practised

- Functions and modular code
- Input validation and error handling (`try` / `except`)
- File handling with JSON
- Dictionaries, lists, and sorting
- Secure randomness with the `secrets` module
- GUI programming with Tkinter

## Connect With Me

- LinkedIn: [your-linkedin-profile-url](https://www.linkedin.com/in/your-profile)
- GitHub: [@anshkumarraix-dev](https://github.com/anshkumarraix-dev)

---

Made as part of the [CodSoft](https://www.codsoft.in) Python Programming Internship. `#codsoft`

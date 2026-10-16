# Lab 5: Static Code Analysis — Flight Reservation System

## GitHub Repository

**Repository Link:** https://github.com/priyaakl/L5_50_flight_reservation_system

## Overview

This project focuses on improving the code quality, security, and maintainability of a Python-based Flight Reservation System using static code analysis tools.

The application manages flight seat reservations, booking cancellations, baggage surcharge calculations, passenger identifier hashing, boarding PIN generation, and flight manifest exports.

## Objectives

- Identify potential programming errors and code-quality issues.
- Detect security vulnerabilities in the original Python program.
- Improve code readability and maintainability.
- Apply Python coding standards and formatting guidelines.
- Compare static analysis results before and after fixing the issues.

## Tools Used

| Tool | Purpose |
|---|---|
| Pylint | Identifies code-quality problems, naming issues, unused variables, and potential programming errors. |
| Bandit | Detects potentially insecure Python coding patterns and security vulnerabilities. |
| Flake8 | Checks Python code style, formatting, whitespace, and other PEP 8 violations. |
| Python | Programming language used to implement the application. |
| Git and GitHub | Version control and repository hosting. |

## Project Structure

```text
L5_50_flight_reservation_system/
├── flight_reservation_system.py
├── issues.md
├── reflection.md
├── pylint_report_before.txt
├── pylint_report_after.txt
├── bandit_report_before.txt
├── bandit_report_after.txt
├── flake8_report_before.txt
├── flake8_report_after.txt
└── README.md
```

## Features

- Flight seat booking and cancellation.
- Seat availability checking.
- Baggage surcharge calculation.
- SHA-256 hashing of passenger identifiers.
- Secure boarding PIN generation using Python's `secrets` module.
- Flight manifest export.

## Issues Identified and Fixed

The original program contained several code-quality and security issues. The following improvements were made:

1. **Unsafe `eval()` usage:** Removed unsafe expression evaluation and replaced it with safer operations.
2. **Weak MD5 hashing:** Replaced MD5 with SHA-256 for stronger hashing.
3. **Insecure PIN generation:** Replaced `random.randint()` with the `secrets` module.
4. **Unsafe shell command execution:** Removed unsafe use of `os.system()`.
5. **Mutable default argument:** Replaced the mutable list default with `None` and initialized the list inside the function.
6. **Exception handling:** Improved handling of invalid inputs and errors.
7. **Code quality and formatting:** Added docstrings, improved naming, removed unused imports and variables, and corrected formatting issues.

The complete issue table and explanations are documented in `issues.md`.

## Static Analysis and Reports

Each tool was run before and after the code improvements.

- **Pylint:** Used to assess code quality and identify programming issues.
- **Bandit:** Used to identify potentially insecure coding patterns.
- **Flake8:** Used to detect style and formatting violations.

The corresponding before-and-after reports are included in the repository for comparison.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/priyaakl/L5_50_flight_reservation_system.git
cd L5_50_flight_reservation_system
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install the analysis tools

```bash
pip install pylint bandit flake8
```

### 4. Run the application

```bash
python flight_reservation_system.py
```

### 5. Run static analysis

```bash
pylint flight_reservation_system.py
bandit -r flight_reservation_system.py
flake8 flight_reservation_system.py
```

## Reflection

This lab demonstrated how static analysis can identify problems that may not be obvious when a program runs. Pylint, Bandit, and Flake8 provide complementary checks for code quality, security, and formatting. Applying the recommended fixes helped improve the program's readability, maintainability, and security.

The detailed reflection answers are available in `reflection.md`.

## Deliverables

- Cleaned Python source code.
- Documented issue table in `issues.md`.
- Reflection answers in `reflection.md`.
- Before-and-after reports for Pylint, Bandit, and Flake8.

## Author

**Priya K L**

**GitHub:** https://github.com/priyaakl/L5_50_flight_reservation_system

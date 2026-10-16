# Lab 5: Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without executing the program. It helps identify potential bugs, security vulnerabilities, unused variables, and coding-style problems. Using these tools improves code quality, readability, security, and maintainability.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks code quality, naming conventions, documentation, and potential programming mistakes. Bandit identifies potentially insecure coding patterns, such as unsafe use of eval() and weak hashing algorithms. Flake8 checks Python style and formatting, including line length, whitespace, and unused imports.

## 3. What important issues did you find and fix in the flight reservation system?

The original program contained several issues, including the use of eval(), weak MD5 hashing, insecure PIN generation, and shell command execution using os.system(). I replaced eval() with safer alternatives, used SHA-256 for hashing, generated PINs with the secrets module, and removed unsafe shell execution. I also corrected issues involving mutable default arguments, exception handling, unused variables, and code formatting.

## 4. What did you learn from using static analysis tools?

I learned that a program can run successfully and still contain security risks and code-quality problems. Pylint, Bandit, and Flake8 helped me identify different categories of issues and understand how to fix them. I also learned that rerunning the tools after making changes is important for verifying improvements while preserving the program's intended functionality.

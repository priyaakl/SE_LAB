


# Lab 5: Static Code Analysis — Issue Log

## Objective

To identify and fix code-quality, security, and style issues in the Flight Reservation System using Pylint, Bandit, and Flake8.

## Identified Issues

| Issue | Type | Original Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe `eval()` | Security | 47 | Executing a Python expression from a string can allow unintended code execution. | Replaced expression evaluation with a numeric baggage surcharge calculation. |
| Weak MD5 hash | Security | 52 | MD5 is not appropriate for security-sensitive hashing. | Replaced MD5 with SHA-256 for the passenger identifier digest. |
| Insecure random PIN | Security | 56 | The standard `random` module is not designed for cryptographic security. | Replaced it with `secrets` for boarding PIN generation. |
| Shell command execution | Security | 63 | Constructing a shell command from a filename can introduce command-injection risks. | Removed the shell command and printed the manifest message directly. |
| Hardcoded API token | Security | 75 | Embedding a secret in source code exposes it to anyone who can read the code. | Removed the unused hardcoded token and its print statement. |
| Bare exception | Code quality | 31–32 | A bare exception silently suppresses errors. | Replaced silent exception handling with explicit flight validation. |
| Mutable default argument | Code quality | 15 | A shared list default can retain data across function calls. | Used `None` as the default and initialized a new list when needed. |
| Missing docstrings and naming violations | Style | Multiple | Several functions lacked documentation and used inconsistent naming conventions. | Added docstrings and converted function names to snake_case. |
| Unused imports and variables | Code quality | Multiple | Unused names make the code harder to maintain. | Removed unused imports and variables. |
| Line-length and newline violations | Style | Multiple | Formatting violations reduce readability and consistency. | Reformatted the source and added the required final newline. |

## Verification

The source was reanalysed with Pylint, Bandit, and Flake8 after the changes. The final results are recorded in the corresponding AFTER reports.
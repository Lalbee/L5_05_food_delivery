# Lab 5: Issues Found and Fixed (delivery_system.py)

Line numbers refer to the original file.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Unsafe deserialization with pickle (B301, B403) | Security (Bandit, Medium/Low) | 2, 49 | `pickle.load` can run arbitrary code if the backup file is tampered with | Removed pickle. Backup and restore now use JSON, and order ids are converted back to int on load |
| Try/except/pass (B110) | Security / Bug (Bandit, Low) | 22-25 | Errors were silently swallowed, so a missing order failed with no message | Catch `KeyError`, print a message, and return `False` |
| Bare except (W0702 / E722) | Bug (Pylint, Flake8) | 24 | `except:` also catches KeyboardInterrupt and SystemExit | Replaced with `except KeyError` |
| Broad exception (W0718) | Bug (Pylint) | 32 | `except Exception` hides unrelated errors | Replaced with `(OSError, json.JSONDecodeError)` |
| Mutable default argument (W0102) | Bug (Pylint) | 11 | `order_history=[]` is shared across all calls | Default is `None`, and a new list is created inside the function |
| File opened without `with` or encoding (R1732, W1514) | Bug / Resource leak (Pylint) | 30, 43, 49 | Files may not be closed if an error happens, and the encoding is platform dependent | Used `with open(..., encoding="utf-8")` |
| Global statements (W0603) | Design (Pylint) | 12, 28, 48 | Rebinding globals makes code hard to test and follow | Shared dicts are modified in place, and `itertools.count` replaces the `next_id` global |
| Invalid names (C0103) | Style (Pylint) | 7, 51 | `printQueue` is not snake_case, and `next_id` was a module-level variable | Renamed to `print_queue` and `ID_COUNTER` |
| Missing docstrings (C0114, C0116) | Style (Pylint) | 1, many | No module or function documentation | Added a module docstring and a docstring for every function |
| Old-style string formatting (C0209) | Style (Pylint) | 52 | `%` formatting instead of an f-string | Used an f-string |
| Blank lines and line length (E302, E305, E501) | Style (Flake8) | 11-70 | 8 blank-line errors and 2 lines longer than 79 characters | Added 2 blank lines between functions, wrapped long lines, and added an `if __name__ == "__main__"` guard |
| Invalid status accepted (logic bug, not flagged by tools) | Bug | 21-25 | `update_order_status` accepted any value, such as "teleported". `VALID_STATUSES` was never used | Check `status in VALID_STATUSES` and reject invalid values |

## Not fixed (found by running the program, no tool flagged it)

- Unknown dishes (such as "sushi") silently cost 99 (line 15).
- Orders with an empty customer name and no items are accepted.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.27/10 | 10.00/10 |
| Bandit | 1 Medium, 2 Low | 0 issues |
| Flake8 | 12 issues | 0 issues |

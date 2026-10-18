# Reflection

**1. Which issues were the easiest and which were the hardest to fix?**
The easiest were the Flake8 style issues (blank lines, line length) and Pylint naming and docstring warnings, because the tools state exactly what to change. The hardest was replacing pickle with JSON, because JSON turns integer dictionary keys into strings, so restoring orders needed an explicit `int(k)` conversion. Removing the `global` statements also needed a design change, since the shared dicts had to be modified in place.

**2. Did the tools report any false positives, or miss real problems?**
I did not see real false positives. Some warnings, like the `global` statements, are style and design suggestions and not necessarily bugs. The tools also missed logic bugs. They did not notice that `update_order_status` accepted the status "teleported", that unknown dishes silently cost 99, or that orders with no customer and no items were accepted. I only found those by running the program and reading the output.

**3. How could static analysis be integrated into a real development workflow?**
Run the tools automatically on every commit with a pre-commit hook, and on every pull request with a CI pipeline (for example GitHub Actions) so a failing Bandit or Flake8 check blocks the merge. Teams can set a minimum Pylint score, and run the tools in the editor so problems show up while coding.

**4. What tangible improvements did static analysis bring to the code?**
Security improved because the unsafe pickle deserialization was removed. Reliability improved because files are always closed, errors are no longer silently swallowed, and the mutable default argument bug is gone. Maintainability improved through docstrings, consistent naming, PEP 8 formatting, and no global state. The Pylint score went from 6.27 to 10.00, and Bandit and Flake8 now report no issues.

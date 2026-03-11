# Project Guidelines

- **Dataclasses**: Prefer using `@dataclass` for data-holding classes to reduce boilerplate (like `__init__` and `__repr__`).
- **Factory Methods**: When complex initialization is required, prefer using `@classmethod` factory methods (e.g., `from_x`) to keep the primary constructor simple and the class's purpose clear.

# Operational Requirements

Before performing any change in the code:
1.  **Sync**: Read the file again to ensure you have the latest version, as it may have been edited manually.

After completing any code modifications:
1.  **Format**: Run `uv run ruff format .` to ensure consistent styling.
2.  **Verify**: Run `uv run pytest` to ensure no regressions were introduced.
3.  **Trigger Rebuild**: Run `touch src/main.py` to notify any watchers (like OpenSCAD) that the entry point has changed.

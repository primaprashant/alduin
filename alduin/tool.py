"""Module for tool implementations for the coding agent."""

from pathlib import Path


def read_file(path: str) -> str:
    """Read the contents of a file.

    Args:
        path: The path to the file to read.

    Returns:
        The contents of the file, or an error message if it fails.
    """

    # does the file exist?

    # read the contents of the file at the requested path
    # and return it back

    p = Path(path)

    if not p.is_file():
        return f"Error: {path} is not a file"

    return p.read_text()


def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Create or edit a file by replacing occurrences of a string.

    This tool can be used to do both, create a new file (if old_str is empty) or edit an existing file.

    Args:
        path: The path to the file to edit.
        old_str: The string to be replaced.
        new_str: The replacement string.

    Returns:
        A success message, or an error message if it fails.
    """

    pass


def list_files(path: str) -> str:
    """List files in a directory.

    Args:
        path: The path to the directory to list files in.

    Returns:
        A newline-separated list of file names, or an error message.
    """

    p = Path(path)
    if not p.is_dir():
        return f"Error: not a directory: {path}"

    contents = sorted(p.iterdir())
    if not contents:
        return "Directory is empty."

    lines = [f"{item.name}/" if item.is_dir() else item.name for item in contents]
    return "\n".join(lines)


def bash(command: str) -> str:
    """Execute a bash command and return its output.

    Ask the user for confirmation before executing, and handle errors gracefully.

    Args:
        command: The bash command to execute.

    Returns:
        The output of the command, or an error message.
    """

    pass

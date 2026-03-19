"""
Utility functions used throughout the project.

These helpers are designed to be small, self-contained and safe to call
from anywhere in the codebase. They handle path management, external
dependency checks and common file operations. Keeping this logic here
avoids repeating code in multiple modules.
"""
import os
import subprocess
from typing import List


def ensure_dir(path: str) -> None:
    """Create a directory and all parent directories if they do not exist."""
    os.makedirs(path, exist_ok=True)


def check_ffmpeg() -> bool:
    """Return True if ffmpeg is installed and callable, False otherwise."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def save_text(text: str, path: str) -> None:
    """Save a string to a text file using UTF-8 encoding."""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def save_list(list_data: List[str], path: str) -> None:
    """Save a list of strings to a text file (one per line)."""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        for item in list_data:
            f.write(f"{item}\n")

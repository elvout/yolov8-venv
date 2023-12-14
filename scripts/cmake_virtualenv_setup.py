#! /usr/bin/env python3

"""
Although this repository uses Poetry / PEP 517 to specify and install
dependencies, catkin only supports the old setup.py way of doing things. We'll
call this script from CMakeLists.txt as a proxy for Poetry.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def check_pip_installed() -> None:
    try:
        import pip  # noqa: F401
    except ModuleNotFoundError:
        print("[FATAL] pip is not installed on the system.", file=sys.stderr)
        sys.exit(1)


def ensure_poetry() -> None:
    check_pip_installed()

    if shutil.which("poetry") is not None:
        return

    completed_process = subprocess.run(["python3", "-m", "pip", "install", "poetry"])

    if completed_process.returncode != 0:
        print("[FATAL] Failed to install poetry via pip.", file=sys.stderr)
        sys.exit(completed_process.returncode)

    if shutil.which("poetry") is None:
        print("[FATAL] Failed to find poetry after installation.", file=sys.stderr)
        sys.exit(1)


def poetry_install_venv() -> None:
    ensure_poetry()

    completed_process = subprocess.run(
        ["poetry", "install", "--no-root", "--no-interaction"]
    )

    if completed_process.returncode != 0:
        print("[FATAL] Failed to initialize virtualenv.", file=sys.stderr)
        sys.exit(completed_process.returncode)

    # Create a dummy file to indicate that the build is completely finished
    Path(".venv/target").touch()


if __name__ == "__main__":
    poetry_install_venv()

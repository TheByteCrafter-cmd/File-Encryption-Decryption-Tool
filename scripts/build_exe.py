"""
PyInstaller Standalone Executable Packaging Script.

Automates building the release-ready Windows desktop executable package.
"""

import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def build_executable() -> None:
    """Invokes PyInstaller to compile app.py into standalone Windows executable."""
    print("=" * 60)
    print("Building Secure File Encryption & Decryption Tool Executable...")
    print("=" * 60)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name=FEDT_Desktop",
        "--add-data=assets;assets",
        "app.py",
    ]

    print(f"Running command: {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(BASE_DIR))

    if res.returncode == 0:
        print("=" * 60)
        print("BUILD SUCCESSFUL! Executable packaged at:")
        print(BASE_DIR / "dist" / "FEDT_Desktop" / "FEDT_Desktop.exe")
        print("=" * 60)
    else:
        print("BUILD FAILED with exit code:", res.returncode)
        sys.exit(res.returncode)


if __name__ == "__main__":
    build_executable()

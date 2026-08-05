# Secure File Encryption & Decryption Tool (Phase 1 Backend Engine)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Security](https://img.shields.io/badge/encryption-AES--256--GCM-green.svg)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![KDF](https://img.shields.io/badge/kdf-PBKDF2--HMAC--SHA256-orange.svg)](https://en.wikipedia.org/wiki/PBKDF2)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

Production-ready, enterprise-grade backend foundation for secure file encryption and decryption. Engineered in Python 3.10+ using **low-level AES-256-GCM streaming**, **PBKDF2-HMAC-SHA256 key derivation**, extensible binary file headers, and constant-memory payload streaming.

Designed to be completely GUI-agnostic for seamless integration with desktop UI frameworks (CustomTkinter, PyQt, PySide) in Phase 2.

---

## Key Features

- 🔐 **AES-256-GCM Authenticated Encryption**: Provides both confidentiality and built-in message integrity authentication.
- ⚡ **True Chunked Streaming**: Processes files in configurable 64 KB chunks, maintaining constant low memory usage across gigabyte-scale payloads.
- 🔑 **Strong Key Derivation**: Uses PBKDF2-HMAC-SHA256 with 600,000 iterations and random 32-byte salts per operation.
- 📄 **Filename Preservation**: Original filenames and extensions are encrypted securely into the binary header and restored automatically during decryption.
- 🏷️ **Extensible Versioned Binary Header**: Binary header protocol with magic header signature (`FEDT`) and versioning for backward compatibility.
- 🧹 **Zero-Trust Memory Cleanup**: Sensitive key buffers are explicitly zeroed out in memory after cryptographic stream completion.
- 📊 **Progress Callback Support**: Non-blocking `progress_callback(processed, total)` hook for real-time progress bar integration.
- 📁 **Universal File Support**: Seamlessly encrypts any file type (`.txt`, `.pdf`, `.png`, `.xlsx`, `.mp4`, `.zip`, `.exe`, `.bin`).
- 🛡️ **Comprehensive Error Handling**: Custom exception hierarchy handling incorrect passwords, file tampering, missing paths, and header corruption.

---

## Directory Structure

```text
File-Encryption-Decryption-Tool/
├── encryption/              # Core cryptographic engine package
│   ├── __init__.py          # Public API exports
│   ├── aes_encrypt.py       # Chunked low-level Cipher AES-256-GCM streaming encryption
│   ├── aes_decrypt.py       # Chunked low-level Cipher AES-256-GCM streaming decryption
│   ├── key_manager.py       # PBKDF2 key derivation & memory zeroing
│   └── utils.py             # Header protocol, custom exceptions, validation helpers
│
├── tests/                   # Automated pytest suite
│   ├── __init__.py
│   ├── test_key_manager.py  # Key derivation & header packing unit tests
│   ├── test_encryption.py   # Encryption stream & header tests
│   ├── test_decryption.py   # Decryption stream & filename restoration tests
│   ├── test_integrity.py    # Tag verification & wrong password handling tests
│   └── test_streaming.py    # Multi-megabyte chunked streaming performance tests
│
├── samples/                 # Sample test files (.txt, .pdf, .png, .zip)
├── output/                  # Output encrypted (.enc) and restored files
├── logs/                    # Audit logs (logs/app.log)
├── docs/                    # Architecture and protocol specifications
│   └── architecture.md
├── assets/                  # Diagrams and media
├── config.py                # Central project configuration module
├── main.py                  # CLI demonstration & verification test runner
├── README.md                # Project documentation
├── LICENSE                  # MIT License
├── requirements.txt         # Production dependencies
└── requirements-dev.txt     # Development & testing dependencies
```

---

## Architecture & Binary Header Specification

Encrypted files (`.enc`) feature a contiguous binary header containing cryptographic parameters and metadata:

```text
+-----------------------------------------------------------------------------------+
| MAGIC (4B) | VER (2B) | SALT (32B) | NONCE (12B) | GCM TAG (16B) | FNAME_LEN (2B) |
+-----------------------------------------------------------------------------------+
| ORIGINAL FILENAME (UTF-8) | CIPHERTEXT STREAM (64 KB Chunks...)                  |
+-----------------------------------------------------------------------------------+
```

Detailed technical specs are available in [docs/architecture.md](docs/architecture.md).

---

## Quick Start & Installation

### 1. Requirements
- Python 3.10 or higher
- `pip` package manager

### 2. Installation
Clone the repository and install required dependencies:

```bash
git clone https://github.com/TheByteCrafter-cmd/File-Encryption-Decryption-Tool.git
cd File-Encryption-Decryption-Tool

# Install production dependencies
pip install -r requirements.txt

# Install development & test dependencies
pip install -r requirements-dev.txt
```

---

## Usage

### Running the CLI Demonstration
Execute `main.py` to run end-to-end sample file encryption, decryption, SHA-256 verification, and error boundary tests:

```bash
python main.py
```

### Python API Integration

```python
from pathlib import Path
from encryption import FileEncryptor, FileDecryptor

# 1. Encrypt a file
encrypted_path = FileEncryptor.encrypt_file(
    input_path=Path("samples/confidential.pdf"),
    password="MySuperSecretPassword123!",
    progress_callback=lambda current, total: print(f"Progress: {current}/{total} bytes")
)
print(f"Encrypted file saved to: {encrypted_path}")

# 2. Decrypt the file (automatically restores original filename)
restored_path = FileDecryptor.decrypt_file(
    encrypted_path=encrypted_path,
    password="MySuperSecretPassword123!",
    output_dir=Path("output/restored"),
)
print(f"Restored original file to: {restored_path}")
```

---

## Quality Assurance & Testing

Run code quality checks and the full test suite:

```bash
# Code formatting check
python -m black --check .

# Static type checking
python -m mypy encryption config.py main.py

# Run pytest unit test suite
python -m pytest -v
```

---

## Security Model

1. **Zero-Trust Logging**: Passwords, derived keys, and unencrypted byte arrays are strictly excluded from logging outputs (`logs/app.log`).
2. **Key Wiping**: Derived key bytearrays are zeroed in memory immediately after cipher initialization/finalization.
3. **AEAD Integrity Guarantee**: Any modification to the `.enc` header or ciphertext results in a tag validation failure during decryption (`IntegrityVerificationError`).

---

## Phase 2 Roadmap (GUI Integration)

- [x] **Phase 1**: Backend Cryptographic Engine (Completed)
- [ ] **Phase 2**: Desktop GUI Integration (CustomTkinter / PyQt)
  - Drag-and-drop file selection
  - Real-time animated progress bars hooked to `progress_callback`
  - Password strength indicator integration
  - Multi-file batch queue processing

---

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

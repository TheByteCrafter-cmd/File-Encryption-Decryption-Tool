# Secure File Encryption & Decryption Tool (Phase 2 Modern Desktop Application)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/gui-CustomTkinter-blueviolet.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Security](https://img.shields.io/badge/encryption-AES--256--GCM-green.svg)](https://en.wikipedia.org/wiki/Galois/Counter_Mode)
[![KDF](https://img.shields.io/badge/kdf-PBKDF2--HMAC--SHA256-orange.svg)](https://en.wikipedia.org/wiki/PBKDF2)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

A production-ready, enterprise-grade desktop application for secure file encryption and decryption. Built in Python 3.10+ featuring a modern **Windows 11 / VSCode inspired CustomTkinter GUI**, a lightweight **MVC Architecture**, **low-level AES-256-GCM streaming**, **PBKDF2-HMAC-SHA256 key derivation**, and zero-trust memory protection.

---

## 🎨 Phase 2 Desktop GUI Highlights

- 🖥️ **Modern Windows 11 / VSCode Aesthetics**: Card-based interface with dark, light, and system theme auto-detection via `darkdetect`.
- 🧩 **Lightweight MVC Architecture**: Strict separation between presentational Views (`gui/views/`), Controllers (`gui/controllers/`), Data Models (`gui/models/`), Widgets (`gui/widgets/`), and the stable Phase 1 Backend (`encryption/`).
- ⚡ **Non-Freezing Asynchronous Execution**: All cryptographic processing runs on background threads (`threading.Thread`), keeping the interface smooth and responsive.
- 📊 **Advanced Progress Dashboard**: Real-time progress bar, percentage indicator, processed MB / total MB counter, transfer speed meter (MB/s), and estimated remaining time (ETA).
- 🔑 **Real-Time Password Entropy Gauge**: Shannon entropy score in bits, brute-force crack time estimates ("Instant", "3 hours", "100M+ years"), visual color gradients, and an integrated Strong Password Generator modal.
- 📜 **Searchable Operation History & Export**: Audit log data table with search filtering, double-click output folder opening, and CSV/JSON export capability.
- 📦 **PyInstaller Packaging Readiness**: Resource loader helper (`gui/utils/resource_loader.py`) resolving single-file EXE (`sys._MEIPASS`) asset paths cleanly.
- ⌨️ **Accessibility & High-DPI Scaling**: Keyboard navigation shortcuts (`Ctrl+O`, `Ctrl+E`, `Ctrl+D`, `Ctrl+H`, `Ctrl+,`) and crisp display scaling across 100%, 125%, 150%, and 200% Windows scaling modes.

---

## Directory Layout

```text
File-Encryption-Decryption-Tool/
├── app.py                      # Desktop GUI Entry Point
├── config.py                   # Global Configuration & Path Definitions
│
├── encryption/                 # STABLE PHASE 1 BACKEND (FROZEN - Imported as Library)
│   ├── __init__.py
│   ├── aes_encrypt.py       # Chunked low-level Cipher AES-256-GCM streaming encryption
│   ├── aes_decrypt.py       # Chunked low-level Cipher AES-256-GCM streaming decryption
│   ├── key_manager.py       # PBKDF2 key derivation & memory zeroing
│   └── utils.py             # Header protocol, custom exceptions, validation helpers
│
├── gui/                        # LIGHTWEIGHT MVC PRESENTATION LAYER
│   ├── views/               # Home, Encrypt, Decrypt, History, Settings, About views
│   ├── controllers/         # Navigation, Encrypt, Decrypt, History, Settings controllers
│   ├── models/              # Job, History, and Settings JSON state models
│   ├── widgets/             # DropZone, PasswordMeter, ProgressPanel, DataTable, MetricCard
│   └── utils/               # ResourceLoader, ThemeManager, PasswordEntropy
│
├── assets/                     # Visual Assets & Icons
├── tests/                      # Automated Pytest Suite (30/30 tests passing)
├── docs/                       # Architecture & GUI documentation
│   ├── architecture.md
│   ├── PHASE1_QA_REPORT.md
│   └── PHASE2_GUI_GUIDE.md
├── logs/                       # Audit logs (logs/app.log)
├── output/                     # Output directory & persistent history.json / settings.json
├── requirements.txt            # Production dependencies
└── requirements-dev.txt        # Development dependencies
```

---

## 🚀 Quick Start

### 1. Installation
Clone the repository and install required dependencies:

```bash
git clone https://github.com/TheByteCrafter-cmd/File-Encryption-Decryption-Tool.git
cd File-Encryption-Decryption-Tool

# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt
```

### 2. Launch Desktop Application
Launch the desktop application GUI:

```bash
python app.py
```

### 3. Run Backend Verification & Quality Checks

```bash
# Code formatting check
python -m black --check .

# Static type analysis
python -m mypy gui/ config.py app.py

# Run full pytest test suite
python -m pytest -v

# Run CLI demonstration
python main.py
```

---

## 🛡️ Cryptographic & Security Specifications

- **Encryption Standard**: AES-256-GCM (Authenticated Encryption with Associated Data - AEAD).
- **Key Derivation**: PBKDF2-HMAC-SHA256 with 600,000 iterations and random 32-byte salts per file operation.
- **In-Memory Zeroing**: Derived key bytearrays are zeroed out in memory immediately after operation finalization (`KeyDerivationManager.wipe_memory`).
- **Zero-Trust Logging**: Passwords and key bytearrays are strictly excluded from audit logs (`logs/app.log`).

---

## 📜 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.

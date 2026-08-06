# Desktop GUI Architecture & User Guide (Phase 2)

## Overview

The **Secure File Encryption & Decryption Tool** Phase 2 introduces a modern, high-performance desktop interface built on a lightweight **MVC (Model-View-Controller)** architecture. It presents a Windows 11 Fluent and Visual Studio Code inspired dark/light user interface using **CustomTkinter**, **TkinterDnD2**, **Pillow**, and **darkdetect**, strictly decoupled from the stable Phase 1 backend encryption engine.

---

## 1. Lightweight MVC Architecture

```text
[View Layer (gui/views/)]  <--->  [Controller Layer (gui/controllers/)]  <--->  [Phase 1 Backend Engine (encryption/)]
                                                    |
                                                    v
                                      [Models Layer (gui/models/)]
```

### Layer Responsibilities

- **Views (`gui/views/`)**: Pure presentational CTk frames and widgets (`home_view.py`, `encrypt_view.py`, `decrypt_view.py`, `history_view.py`, `settings_view.py`, `about_view.py`). Views handle zero encryption logic.
- **Controllers (`gui/controllers/`)**: Business logic managers (`main_controller.py`, `encrypt_controller.py`, `decrypt_controller.py`, `history_controller.py`, `settings_controller.py`). Controllers dispatch asynchronous worker threads to the Phase 1 backend engine (`encryption/`) and update UI elements cleanly on the main Tkinter thread.
- **Models (`gui/models/`)**: Persistent JSON models (`settings_model.py`, `history_model.py`, `job_model.py`) managing window state, geometry, settings, and operation history.
- **Widgets (`gui/widgets/`)**: Reusable UI components (`drop_zone.py`, `password_meter.py`, `progress_panel.py`, `data_table.py`, `metric_card.py`, `dialogs.py`).

---

## 2. Asynchronous Threading Model & UI Responsiveness

To guarantee a fluid, non-freezing UI regardless of payload size (multi-GB files supported), all file encryption and decryption tasks execute on dedicated background threads (`threading.Thread`).

- **Progress Hook**: Uses `progress_callback(processed_bytes, total_bytes)` to calculate transfer speeds (MB/s) and estimated remaining time (ETA).
- **Main Thread Synchronization**: Dispatches UI updates via `view.after(0, ...)` to ensure thread safety with CustomTkinter runtime.

---

## 3. PyInstaller Packaging Readiness

Asset resolution uses `gui/utils/resource_loader.py`:

```python
from gui.utils.resource_loader import ResourceLoader

# Resolves asset path in both local development and PyInstaller single-file EXE (_MEIPASS)
icon_path = ResourceLoader.get_resource_path("assets/icons/lock.png")
```

---

## 4. Accessibility & Keyboard Navigation

- **Minimum Window Size**: `1000 x 650` (Responsive resizable grid)
- **High-DPI Display Scaling**: Automatic scaling across 100%, 125%, 150%, and 200% Windows display scaling settings.
- **Keyboard Shortcuts**:
  - `Ctrl + O`: Go to Home Dashboard
  - `Ctrl + E`: Go to Encrypt File
  - `Ctrl + D`: Go to Decrypt File
  - `Ctrl + H`: Go to Operation History
  - `Ctrl + ,`: Go to Settings
  - `ESC`: Close open modal dialogs

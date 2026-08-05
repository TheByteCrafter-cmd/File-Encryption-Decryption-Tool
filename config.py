"""
Central Configuration Module for Secure File Encryption & Decryption Tool.

Defines project-wide constants, cryptographic parameter defaults, path configurations,
logging standards, and application metadata.
"""

from pathlib import Path

# Application Metadata
APP_NAME: str = "Secure File Encryption & Decryption Tool"
APP_VERSION: str = "v1.0.0-alpha"

# Cryptographic Specifications (AES-256-GCM + PBKDF2-HMAC-SHA256)
MAGIC_HEADER: bytes = b"FEDT"
HEADER_VERSION: int = 1  # 2-byte unsigned short (0x0001)

# Cryptographic Parameter Sizes (in bytes)
SALT_SIZE: int = 32  # 256 bits of secure random salt
NONCE_SIZE: int = 12  # 96 bits standard IV/Nonce for AES-GCM
TAG_SIZE: int = 16  # 128 bits authentication tag for AES-GCM
KEY_SIZE: int = 32  # 256 bits AES key size

# Key Derivation Parameters
PBKDF2_ITERATIONS: int = 600_000  # OWASP recommended strong iteration count
HASH_ALGORITHM: str = "SHA256"

# Streaming & Performance Parameters
CHUNK_SIZE: int = 65536  # 64 KB memory-efficient chunk size

# Directory & File Paths
BASE_DIR: Path = Path(__file__).resolve().parent
LOGS_DIR: Path = BASE_DIR / "logs"
SAMPLES_DIR: Path = BASE_DIR / "samples"
OUTPUT_DIR: Path = BASE_DIR / "output"
DOCS_DIR: Path = BASE_DIR / "docs"
ASSETS_DIR: Path = BASE_DIR / "assets"

LOG_FILE: Path = LOGS_DIR / "app.log"
LOG_LEVEL: str = "INFO"

# Ensure runtime directories exist
for directory in (LOGS_DIR, SAMPLES_DIR, OUTPUT_DIR, DOCS_DIR, ASSETS_DIR):
    directory.mkdir(parents=True, exist_ok=True)

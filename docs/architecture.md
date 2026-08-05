# Architecture & Binary Specification

## Overview

The **Secure File Encryption & Decryption Tool** backend engine is designed as a modular, GUI-independent cryptographic core. It implements **AES-256-GCM (Authenticated Encryption with Associated Data)** using low-level stream ciphers and **PBKDF2-HMAC-SHA256** for key derivation.

---

## 1. Binary File Header Protocol (`.enc` Format)

Every encrypted file begins with a contiguous binary header containing cryptographic parameters and metadata required for automatic decryption and filename restoration.

### Header Byte Structure

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      MAGIC HEADER ("FEDT")                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       VERSION (0x0001)        |                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               +
|                       SALT (32 Bytes)                         |
|                                                               |
|                               +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                               |       NONCE / IV (12 Bytes)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                               |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    AES-GCM AUTH TAG (16 Bytes)                |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  FILENAME_LEN (2 Bytes uint16)|  ORIGINAL FILENAME (UTF-8)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     CIPHERTEXT STREAM DATA ...                |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Field Definitions

1. **Magic Header (`4 Bytes`)**: ASCII `FEDT` (`0x46 0x45 0x44 0x54`). Validates file signature.
2. **Version (`2 Bytes`)**: Unsigned short (`0x0001` for `v1.0.0-alpha`). Supports future header extensions.
3. **Salt (`32 Bytes`)**: Cryptographically random salt generated via `secrets.token_bytes(32)`.
4. **Nonce / IV (`12 Bytes`)**: Cryptographically random 96-bit nonce for AES-GCM mode.
5. **Auth Tag (`16 Bytes`)**: 128-bit AES-GCM authentication tag. Written after stream completion via seek write.
6. **Filename Length (`2 Bytes`)**: Big-endian unsigned short storing UTF-8 byte length of original filename.
7. **Original Filename (`Variable`)**: Original filename and extension encoded in UTF-8.

---

## 2. Low-Level Cipher Streaming Flow

```text
[Input File] ---> Read Chunk (64 KB) ---> encryptor.update(chunk) ---> Write Ciphertext ---> [Output .enc File]
                                                                                                    |
                                                                             Post-Finalize GCM Tag  |
                                                                             Seek Write at Offset 50 <+
```

---

## 3. Security Guarantees & Memory Protection

- **Key Derivation**: PBKDF2-HMAC-SHA256 with 600,000 iterations prevents brute-force rainbow table attacks.
- **Zero-Trust Logging**: Password strings and key bytearrays are strictly excluded from logging statements.
- **Memory Zeroing**: Key buffers are backed by `bytearray` and zeroed out immediately after stream finalization.

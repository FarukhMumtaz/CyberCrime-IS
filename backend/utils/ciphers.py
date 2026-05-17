"""
Classical cipher helpers for sensitive complaint and evidence fields.

Values carry invisible cipher markers so existing plaintext records remain
readable and new records are not encrypted twice through sync/update paths.
Legacy MONO:: and VIG:: prefixes are still accepted for old database rows.
"""

from __future__ import annotations

import base64
import json
import os
import string
from typing import Any, Dict


LEGACY_MONO_PREFIX = "MONO::"
LEGACY_VIG_PREFIX = "VIG::"
MONO_PREFIX = "\u2063\u200c"
VIG_PREFIX = "\u2063\u200d"
DEFAULT_MONOALPHABETIC_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"
DEFAULT_VIGENERE_KEY = "CYBERSECURITY"

MONO_COMPLAINT_FIELDS = {"full_name", "phone", "address", "location"}
VIGENERE_COMPLAINT_FIELDS = {"email", "cnic", "description", "detailed_log"}
VIGENERE_EVIDENCE_FIELDS = {"file_name", "original_name", "file_path", "mime_type"}
METADATA_REFERENCE_KEYS = {
    "id",
    "tracking_id",
    "complaint_id",
    "evidence_id",
    "resource_id",
    "user_id",
}


def _is_blank(value: Any) -> bool:
    return value is None or value == ""


def _has_cipher_prefix(value: Any) -> bool:
    return _cipher_marker(value) is not None


def _cipher_marker(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if value.startswith(MONO_PREFIX) or value.startswith(LEGACY_MONO_PREFIX):
        return "mono"
    if value.startswith(VIG_PREFIX) or value.startswith(LEGACY_VIG_PREFIX):
        return "vig"
    return None


def _strip_cipher_marker(value: str, marker: str) -> str:
    prefixes = (
        (MONO_PREFIX, LEGACY_MONO_PREFIX)
        if marker == "mono"
        else (VIG_PREFIX, LEGACY_VIG_PREFIX)
    )
    for prefix in prefixes:
        if value.startswith(prefix):
            return value[len(prefix) :]
    return value


def _to_text(value: Any) -> str:
    return value if isinstance(value, str) else str(value)


def _encode_text(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def _decode_text(text: str) -> str:
    return base64.urlsafe_b64decode(text.encode("ascii")).decode("utf-8")


def _mono_key() -> str:
    key = os.getenv("MONOALPHABETIC_KEY", DEFAULT_MONOALPHABETIC_KEY).upper()
    key = "".join(ch for ch in key if ch in string.ascii_uppercase)
    if len(key) != 26 or len(set(key)) != 26:
        return DEFAULT_MONOALPHABETIC_KEY
    return key


def _mono_translation() -> tuple[dict[int, int], dict[int, int]]:
    plain_upper = string.ascii_uppercase
    cipher_upper = _mono_key()
    plain = plain_upper + plain_upper.lower()
    cipher = cipher_upper + cipher_upper.lower()
    encrypt_table = str.maketrans(plain, cipher)
    decrypt_table = str.maketrans(cipher, plain)
    return encrypt_table, decrypt_table


def _vigenere_key_shifts() -> list[int]:
    key = os.getenv("VIGENERE_KEY", DEFAULT_VIGENERE_KEY).upper()
    shifts = [ord(ch) - ord("A") for ch in key if ch in string.ascii_uppercase]
    if not shifts:
        shifts = [ord(ch) - ord("A") for ch in DEFAULT_VIGENERE_KEY]
    return shifts


def _shift_alpha(char: str, shift: int) -> str:
    base = ord("A") if char.isupper() else ord("a")
    return chr((ord(char) - base + shift) % 26 + base)


def _vigenere_transform(text: str, decrypt: bool = False) -> str:
    shifts = _vigenere_key_shifts()
    result: list[str] = []
    key_index = 0

    for char in text:
        if char.isalpha() and char.isascii():
            shift = shifts[key_index % len(shifts)]
            result.append(_shift_alpha(char, -shift if decrypt else shift))
            key_index += 1
        else:
            result.append(char)

    return "".join(result)


def mono_encrypt(text: Any) -> Any:
    """Encrypt text with a monoalphabetic substitution cipher."""
    if _is_blank(text) or _has_cipher_prefix(text):
        return text

    encoded = _encode_text(_to_text(text))
    encrypt_table, _ = _mono_translation()
    return f"{MONO_PREFIX}{encoded.translate(encrypt_table)}"


def mono_decrypt(text: Any) -> Any:
    """Decrypt marked monoalphabetic text; return plaintext records unchanged."""
    if _is_blank(text) or not isinstance(text, str) or _cipher_marker(text) != "mono":
        return text

    try:
        body = _strip_cipher_marker(text, "mono")
        _, decrypt_table = _mono_translation()
        return _decode_text(body.translate(decrypt_table))
    except Exception:
        return text


def vigenere_encrypt(text: Any) -> Any:
    """Encrypt text with a Vigenere cipher."""
    if _is_blank(text) or _has_cipher_prefix(text):
        return text

    encoded = _encode_text(_to_text(text))
    return f"{VIG_PREFIX}{_vigenere_transform(encoded)}"


def vigenere_decrypt(text: Any) -> Any:
    """Decrypt marked Vigenere text; return plaintext records unchanged."""
    if _is_blank(text) or not isinstance(text, str) or _cipher_marker(text) != "vig":
        return text

    try:
        body = _strip_cipher_marker(text, "vig")
        return _decode_text(_vigenere_transform(body, decrypt=True))
    except Exception:
        return text


def _decrypt_any_prefixed(value: Any) -> Any:
    if _cipher_marker(value) == "mono":
        return mono_decrypt(value)
    if _cipher_marker(value) == "vig":
        return vigenere_decrypt(value)
    return value


def encrypt_complaint_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt selected sensitive complaint fields for database storage."""
    encrypted = dict(data)
    for field in MONO_COMPLAINT_FIELDS:
        if field in encrypted:
            encrypted[field] = mono_encrypt(encrypted[field])
    for field in VIGENERE_COMPLAINT_FIELDS:
        if field in encrypted:
            encrypted[field] = vigenere_encrypt(encrypted[field])
    return encrypted


def decrypt_complaint_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt selected sensitive complaint fields for display/API responses."""
    decrypted = dict(data)
    for field in MONO_COMPLAINT_FIELDS | VIGENERE_COMPLAINT_FIELDS:
        if field in decrypted:
            decrypted[field] = _decrypt_any_prefixed(decrypted[field])
    return decrypted


def _encrypt_metadata(metadata: Any, key_name: str | None = None) -> Any:
    if _is_blank(metadata) or _has_cipher_prefix(metadata):
        return metadata
    if key_name in METADATA_REFERENCE_KEYS:
        return metadata
    if isinstance(metadata, dict):
        return {
            key: _encrypt_metadata(value, str(key))
            for key, value in metadata.items()
        }
    if isinstance(metadata, list):
        return [_encrypt_metadata(value) for value in metadata]
    if isinstance(metadata, str):
        return vigenere_encrypt(metadata)
    return metadata


def _decrypt_metadata(metadata: Any) -> Any:
    if isinstance(metadata, dict):
        return {key: _decrypt_metadata(value) for key, value in metadata.items()}
    if isinstance(metadata, list):
        return [_decrypt_metadata(value) for value in metadata]
    if _cipher_marker(metadata) != "vig":
        return metadata

    decrypted = vigenere_decrypt(metadata)
    if not isinstance(decrypted, str):
        return decrypted

    try:
        parsed = json.loads(decrypted)
    except Exception:
        return decrypted
    return _decrypt_metadata(parsed)


def encrypt_evidence_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Encrypt selected evidence metadata fields for database storage."""
    encrypted = dict(data)
    for field in VIGENERE_EVIDENCE_FIELDS:
        if field in encrypted:
            encrypted[field] = vigenere_encrypt(encrypted[field])
    if "metadata" in encrypted:
        encrypted["metadata"] = _encrypt_metadata(encrypted["metadata"])
    return encrypted


def decrypt_evidence_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    """Decrypt selected evidence metadata fields for officer/user display."""
    decrypted = dict(data)
    for field in VIGENERE_EVIDENCE_FIELDS:
        if field in decrypted:
            decrypted[field] = _decrypt_any_prefixed(decrypted[field])
    if "metadata" in decrypted:
        decrypted["metadata"] = _decrypt_metadata(decrypted["metadata"])
    return decrypted

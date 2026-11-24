import os
import pytest
from app.storage.storage_service import StorageService

def test_checksum_calculation():
    data = b"Hello GenStudio AI Research"
    checksum = StorageService.calculate_checksum(data)
    assert len(checksum) == 64
    assert checksum == StorageService.calculate_checksum(data)

def test_magic_bytes_verification():
    # Valid PNG
    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
    assert StorageService.verify_magic_bytes(png_bytes, "image/png") is True

    # Invalid PNG pretending to be PNG
    fake_png = b"FAKE_NOT_A_REAL_IMAGE"
    assert StorageService.verify_magic_bytes(fake_png, "image/png") is False

    # Valid JPEG
    jpeg_bytes = b"\xff\xd8\xff" + b"\x00" * 20
    assert StorageService.verify_magic_bytes(jpeg_bytes, "image/jpeg") is True

def test_path_traversal_prevention(tmp_path):
    storage = StorageService(base_dir=str(tmp_path))
    # Path traversal attack attempt
    resolved = storage.get_file_path("../../../windows/system32/cmd.exe")
    assert resolved is None

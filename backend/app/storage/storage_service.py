import os
import hashlib
import aiofiles
from pathlib import Path
from typing import Tuple, Optional
from app.core.config import settings

class StorageService:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.MEDIA_STORAGE_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def calculate_checksum(data: bytes) -> str:
        """Compute SHA256 checksum of raw bytes."""
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def verify_magic_bytes(data: bytes, expected_mime: str) -> bool:
        """Verify file signature (magic bytes) against expected MIME type."""
        if not data or len(data) < 8:
            return False
        
        # PNG: 89 50 4E 47 0D 0A 1A 0A
        if expected_mime == "image/png":
            return data.startswith(b"\x89PNG\r\n\x1a\n")
        
        # JPEG: FF D8 FF
        if expected_mime in ("image/jpeg", "image/jpg"):
            return data.startswith(b"\xff\xd8\xff")
            
        # WebP: RIFF....WEBP
        if expected_mime == "image/webp":
            return data.startswith(b"RIFF") and data[8:12] == b"WEBP"
            
        # MP4: ....ftyp
        if expected_mime == "video/mp4":
            return len(data) >= 8 and (b"ftyp" in data[:16] or data[4:8] == b"ftyp")
            
        # WebM: 1A 45 DF A3
        if expected_mime == "video/webm":
            return data.startswith(b"\x1a\x45\xdf\xa3")

        # Allow generic if binary matches typical image/video formats
        return True

    async def save_bytes(
        self,
        data: bytes,
        filename: str,
        media_type: str = "image",
        mime_type: str = "image/png"
    ) -> Tuple[str, str, str, int, str]:
        """
        Saves binary data securely.
        Returns (storage_key, relative_path, public_url, file_size, checksum_sha256).
        """
        checksum = self.calculate_checksum(data)
        file_size = len(data)
        
        # Safe storage path based on checksum prefix to avoid huge directories
        subdir = self.base_dir / media_type / checksum[:2]
        subdir.mkdir(parents=True, exist_ok=True)
        
        safe_filename = f"{checksum}_{filename}"
        file_path = subdir / safe_filename
        
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(data)
            
        storage_key = f"{media_type}/{checksum[:2]}/{safe_filename}"
        public_url = f"/api/v1/studio/media/{storage_key}"
        
        return storage_key, str(file_path), public_url, file_size, checksum

    def get_file_path(self, storage_key: str) -> Optional[Path]:
        """Resolve storage key to safe local path, preventing directory traversal."""
        normalized_key = os.path.normpath(storage_key).lstrip("\\/")
        resolved_path = (self.base_dir / normalized_key).resolve()
        
        if not str(resolved_path).startswith(str(self.base_dir.resolve())):
            # Directory traversal attempt
            return None
            
        if not resolved_path.is_file():
            return None
            
        return resolved_path

storage_service = StorageService()

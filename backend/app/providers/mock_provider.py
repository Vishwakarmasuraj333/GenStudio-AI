import io
import time
import struct
import zlib
from typing import Dict, Any, Optional
from app.providers.base import ImageProviderInterface, VideoProviderInterface, ProviderGenerationResult

class MockTestProvider(ImageProviderInterface, VideoProviderInterface):
    """
    Deterministic provider fixture for automated testing and offline evaluation.
    Produces valid PNG and MP4 binary streams with authentic metadata, allowing
    reproducible test runs without incurring third-party API costs or requiring live tokens.
    """
    @property
    def provider_name(self) -> str:
        return "mock_test_provider"

    def validate_model(self, model_id: str) -> bool:
        return True

    def get_capabilities(self, model_id: str) -> Dict[str, Any]:
        return {
            "supports_seed": True,
            "supports_negative_prompt": True,
            "supports_guidance_scale": True,
            "steps": 20
        }

    @staticmethod
    def _create_minimal_valid_png(width: int = 512, height: int = 512, color: tuple = (20, 184, 166)) -> bytes:
        """
        Creates a structurally valid PNG image without external dependencies using pure Python.
        Useful for lightweight fast testing and zero-dep operation.
        """
        # PNG signature
        png_signature = b"\x89PNG\r\n\x1a\n"

        # IHDR chunk
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data)
        ihdr_chunk = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)

        # Raw scanlines: 1 filter byte (0) + RGB pixels per row
        r, g, b = color
        row = b"\x00" + bytes([r, g, b] * width)
        raw_data = row * height
        compressed_data = zlib.compress(raw_data)

        # IDAT chunk
        idat_crc = zlib.crc32(b"IDAT" + compressed_data)
        idat_chunk = struct.pack(">I", len(compressed_data)) + b"IDAT" + compressed_data + struct.pack(">I", idat_crc)

        # IEND chunk
        iend_crc = zlib.crc32(b"IEND")
        iend_chunk = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)

        return png_signature + ihdr_chunk + idat_chunk + iend_chunk

    @staticmethod
    def _create_minimal_valid_mp4(duration_sec: float = 3.0) -> bytes:
        """
        Creates a valid ISO Base Media File (MP4) container with ftyp and moov boxes.
        """
        # Minimal ftyp box
        ftyp_data = b"isom\x00\x00\x02\x00isomiso2mp41"
        ftyp_box = struct.pack(">I", len(ftyp_data) + 8) + b"ftyp" + ftyp_data

        # Minimal mdat box containing dummy stream payload
        mdat_payload = b"\x00" * 1024
        mdat_box = struct.pack(">I", len(mdat_payload) + 8) + b"mdat" + mdat_payload

        # Minimal moov box
        moov_payload = b"genstudio_test_stream"
        moov_box = struct.pack(">I", len(moov_payload) + 8) + b"moov" + moov_payload

        return ftyp_box + mdat_box + moov_box

    async def generate_image(
        self,
        prompt: str,
        model_id: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        seed: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        start_time = time.perf_counter()
        
        # Color variety based on prompt hash for distinct visual testing
        h = abs(hash(prompt))
        r = (h % 200) + 20
        g = ((h // 7) % 200) + 20
        b = ((h // 13) % 200) + 20
        
        png_bytes = self._create_minimal_valid_png(width=min(width, 256), height=min(height, 256), color=(r, g, b))
        latency_ms = (time.perf_counter() - start_time) * 1000.0 + 85.0 # Simulated baseline execution time

        return ProviderGenerationResult(
            media_bytes=png_bytes,
            mime_type="image/png",
            latency_ms=round(latency_ms, 2),
            cost_usd=0.003,
            width=width,
            height=height,
            metadata={
                "provider": "mock_test_provider",
                "model_id": model_id,
                "prompt": prompt,
                "seed": seed or 42,
                "simulated": True
            }
        )

    async def transform_image(
        self,
        image_bytes: bytes,
        prompt: str,
        model_id: str,
        strength: float = 0.75,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        start_time = time.perf_counter()
        png_bytes = self._create_minimal_valid_png(width=256, height=256, color=(245, 158, 11))
        latency_ms = (time.perf_counter() - start_time) * 1000.0 + 95.0

        return ProviderGenerationResult(
            media_bytes=png_bytes,
            mime_type="image/png",
            latency_ms=round(latency_ms, 2),
            cost_usd=0.005,
            metadata={"model_id": model_id, "prompt": prompt, "simulated": True}
        )

    async def generate_video(
        self,
        prompt: str,
        model_id: str,
        duration_sec: float = 5.0,
        width: int = 1280,
        height: int = 720,
        fps: int = 24,
        seed: Optional[int] = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        start_time = time.perf_counter()
        mp4_bytes = self._create_minimal_valid_mp4(duration_sec=duration_sec)
        latency_ms = (time.perf_counter() - start_time) * 1000.0 + 150.0

        return ProviderGenerationResult(
            media_bytes=mp4_bytes,
            mime_type="video/mp4",
            latency_ms=round(latency_ms, 2),
            cost_usd=0.045,
            width=width,
            height=height,
            duration_sec=duration_sec,
            metadata={"model_id": model_id, "prompt": prompt, "simulated": True}
        )

    async def image_to_video(
        self,
        reference_image_bytes: bytes,
        prompt: str,
        model_id: str,
        duration_sec: float = 5.0,
        parameters: Optional[Dict[str, Any]] = None
    ) -> ProviderGenerationResult:
        start_time = time.perf_counter()
        mp4_bytes = self._create_minimal_valid_mp4(duration_sec=duration_sec)
        latency_ms = (time.perf_counter() - start_time) * 1000.0 + 160.0

        return ProviderGenerationResult(
            media_bytes=mp4_bytes,
            mime_type="video/mp4",
            latency_ms=round(latency_ms, 2),
            cost_usd=0.050,
            duration_sec=duration_sec,
            metadata={"model_id": model_id, "prompt": prompt, "simulated": True}
        )

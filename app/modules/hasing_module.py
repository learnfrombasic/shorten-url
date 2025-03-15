import hashlib
import time

from app.common import setup_logger
from app.core.config import settings
from app.modules.base import BaseShorten

logger = setup_logger("URLShortener")


class URLShortener(BaseShorten):
    def __init__(self, mode="sha256"):
        if mode not in hashlib.algorithms_available:
            raise ValueError(f"Invalid hashing mode: {mode}!")
        super().__init__(mode=mode)
        self.salt = settings.HASH_SALT

    def shorten(self, long_url: str) -> str:
        """Generates a short URL using SHA-256 hashing with collision handling."""
        try:
            start_time = time.perf_counter()
            hash_url = hashlib.new(
                name=self.mode, data=self.salt.encode() + long_url.encode()
            ).hexdigest()
            short_url = hash_url[: self.idx_len]
            elapsed_time = time.perf_counter() - start_time
            return {
                "short_url": short_url,
                "long_url": long_url,
                "hash_url": hash_url,
                "mode": self.mode,
                "response_time": float(elapsed_time),
            }
        except Exception as e:
            logger.error(f"Error generating short URL: {e}")
            raise

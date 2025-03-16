import hashlib

from app.common import setup_logger
from app.modules.base import BaseShorten

logger = setup_logger("URLShortener")


class URLShortener(BaseShorten):
    def __init__(self, mode, idx_len):
        if mode not in hashlib.algorithms_available:
            raise ValueError(f"Invalid hashing mode: {mode}!")
        super().__init__(mode=mode, idx_len=idx_len)

    def shorten(self, long_url: str) -> str:
        """Generates a short URL using SHA-256 hashing with collision handling."""
        try:
            hash_url = hashlib.new(
                name=self.mode, data=long_url.encode()
            ).hexdigest()
            short_url = hash_url[: self.idx_len]
            return {
                "short_url": short_url,
                "long_url": long_url,
                "hash_url": hash_url,
                "mode": self.mode,
            }
        except Exception as e:
            logger.error(f"Error generating short URL: {e}")
            raise

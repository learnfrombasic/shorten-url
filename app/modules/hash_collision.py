import hashlib
from app.modules.base import BaseShorten
from app.core.config import settings


class URLShortener(BaseShorten):

    def __init__(self, mode="HashCollision"):
        super().__init__(mode=mode)
        self.salt = settings.HASH_SALT  # Predefined string for handling collisions

    def shorten(self, payload):
        """Generates a short URL using SHA-256 hashing with collision handling."""
        attempt = 0

        while True:
            # Append salt if retrying due to collision
            url_to_hash = payload + (self.salt * attempt if attempt > 0 else "")

            # Generate a hash
            hash_obj = hashlib.sha256(url_to_hash.encode())
            short_url = hash_obj.hexdigest()[:self.idx_len]

            # Check for collision
            if short_url not in self.url_map:
                self.url_map[short_url] = payload
                return short_url  # Return the generated short URL
            else:
                attempt += (
                    1  # Increase attempt to modify the hash in the next iteration
                )

    def get_long_url(self, short_url):
        """Retrieves the original long URL from the short URL."""
        return self.url_map.get(short_url, "URL not found")

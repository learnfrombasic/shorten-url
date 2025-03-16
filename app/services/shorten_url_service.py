from app.common import setup_logger, get_time_now
from app.models.shorten_url import ShortenURL
from app.modules.hashing_module import URLShortener
from app.core.config import settings

logger = setup_logger(name="ShortenURL")


class ShortenURLService:
    """
    Service class for handling URL shortening and retrieval operations.
    """

    def __init__(self):
        """
        Initializes the ShortenURLService with a URL shortening algorithm.
        """
        self.algo = URLShortener(
            mode=settings.HASH_ALGO.lower(), 
            idx_len=settings.IDX_LEN
        )
        self.salt = settings.HASH_SALT

    async def create_short_url(self, long_url: str) -> ShortenURL:
        """
        Generates a short URL using SHA-256 hashing with collision handling.
        """
        try:
            attempt = 0

            # Loop until a unique short URL is found
            while True:  
                payload = long_url + (self.salt * attempt if attempt > 0 else "")
                hash_resp = self.algo.shorten(payload)

                # Check if short URL already exists
                existing_url = await ShortenURL.find_one({"short_url": hash_resp.get("short_url")})

                if not existing_url:
                    break  # Unique short URL found

                attempt += 1  # Increment attempt for next hash variation

            # Prepare response data
            response_data = {
                "long_url": long_url,
                "short_url": hash_resp.get("short_url"),
                "algo": self.algo.mode,
                "created_at": get_time_now(),
            }
            response = ShortenURL(**response_data)

            # Insert the new shortened URL into the database
            await response.insert()
            logger.info(f"Successfully inserted Short URL {response.short_url} into the database.")

            return response

        except Exception as e:
            logger.error(f"Error creating short URL: {e}", exc_info=True)
            raise RuntimeError("Failed to generate short URL") from e

    async def get_long_url(self, *, short_url: str) -> ShortenURL:
        """
        Retrieves the original long URL from a given short URL.
        """
        try:
            response = await ShortenURL.find_one({"short_url": short_url})
            if not response:
                logger.warning(f"Short URL '{short_url}' not found in the database.")
                raise ValueError(f"Short URL '{short_url}' not found")

            return response

        except Exception as e:
            logger.error(f"Error retrieving long URL for Short URL '{short_url}': {e}", exc_info=True)
            raise RuntimeError("Failed to retrieve the long URL") from e

    def get_healthcheck(self) -> dict: 
        return {
            'ip': settings.HOST, 
            'port': settings.PORT, 
            'status': 'alive'
        }

# Instantiate the service
shorten_url_service = ShortenURLService()

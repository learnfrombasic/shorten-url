from app.common import setup_logger, get_time_now
from app.models.shorten_url import ShortenURLRequest, ShortenURLResponse
from app.modules.hasing_module import URLShortener

logger = setup_logger(name="ShortenURL")


class ShortenURLService:
    """
    Service class for handling URL shortening and retrieval operations.
    """

    def __init__(self):
        """
        Initializes the ShortenURLService with a URL shortening algorithm.
        """
        self.algo = URLShortener()

    async def create_short_url(self, req: ShortenURLRequest) -> ShortenURLResponse:
        """
        Creates a shortened URL from a given long URL.
        """
        try:
            short_url = self.algo.shorten(req.long_url).get("short_url")

            response_data = {
                "long_url": req.long_url,
                "short_url": short_url,
                "algo": self.algo.mode,
                "created_at": get_time_now(),
                "response_time": short_url.get("response_time"),
            }
            response = ShortenURLResponse(**response_data)

            await response.insert()  # Save to the database
            logger.info(f"Insert {response.id} successfully")
            return response
        except Exception as e:
            logger.error(f"Error creating short URL: {e}", exc_info=True)
            raise RuntimeError("Failed to generate short URL") from e

    async def get_long_url(self, *, id: str) -> ShortenURLResponse:
        """
        Retrieves the original long URL from a given short URL identifier.
        """
        try:
            response = await ShortenURLResponse.find_one({"short_url": id})
            if not response:
                raise ValueError(f"Short URL '{id}' not found")

            return response
        except Exception as e:
            logger.error(f"Error retrieving long URL for ID '{id}': {e}", exc_info=True)
            raise RuntimeError("Failed to retrieve the long URL") from e


shorten_url_service = ShortenURLService()

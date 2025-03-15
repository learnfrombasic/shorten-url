
from app.common import setup_logger
from app.models.shorten_url import ShortenURLRequest, ShortenURLResponse
from app.modules.hash_collision import URLShortener

logger = setup_logger(name="ShortenURL")


class ShortenURLService:
    def __init__(self):

        self.algo = URLShortener()
        
    def create_short_url(self, req: object): ...

    def redirect_short_url(self, *, id: str): ...



shorten_url_serivce = ShortenURLService()

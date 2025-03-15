from beanie import Document
from typing import Optional

class BaseShortenURL(Document): 
    long_url: str
    created_at: int
    modified_at: Optional[int]

class ShortenURLRequest(BaseShortenURL): 
    pass


class ShortenURLResponse(BaseShortenURL): 
    short_url: str
    algo: str
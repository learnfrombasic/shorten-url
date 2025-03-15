from typing import Optional

from beanie import Document


class BaseShortenURL(Document):
    long_url: str
    created_at: int
    modified_at: Optional[int]


class ShortenURLRequest(BaseShortenURL):
    pass


class ShortenURLResponse(BaseShortenURL):
    short_url: str
    algo: str

from typing import Optional

from beanie import Document


class ShortenURLRequest(Document):
    long_url: str


class ShortenURLResponse(Document):
    short_url: str
    algo: str
    long_url: str
    created_at: float
    response_time: float

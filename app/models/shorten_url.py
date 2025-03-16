
from beanie import Document


class ShortenURL(Document):
    short_url: str
    algo: str
    long_url: str
    created_at: float

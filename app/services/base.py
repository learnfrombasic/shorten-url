from abc import ABC, abstractmethod


class BaseShorten(ABC):
    def __init__(self, mode: str, idx_len: int = 6):
        self.mode = mode
        self.idx_len = idx_len  # Take the first `idx_len` chars for indexing

    @abstractmethod
    def create_short_url(self, long_url: str) -> str:
        """
        Using shorten url algorithms to create a short URL.
        """
        raise NotImplementedError

    @abstractmethod
    def get_long_url(self, *, id: str) -> str:
        """
        Find the shorten URL in the database and return the relevant long URL.
        The service then redirect to the long URL.
        """
        raise NotImplementedError

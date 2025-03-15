from abc import ABC, abstractmethod


class BaseShorten(ABC):
    def __init__(self, mode: str, idx_len: int = 6):
        self.mode = mode
        self.idx_len = idx_len  # Take the first `idx_len` chars for indexing

    @abstractmethod
    def shorten(self, long_url: str) -> str:
        raise NotImplementedError

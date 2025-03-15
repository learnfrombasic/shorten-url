import pytest


@pytest.fixture
def init_samples() -> list[str]:
    return [
        "https://docs.python.org/3/library/hashlib.html",
        "https://arxiv.org/pdf/2110.13128x",
        "https://www.google.com/",
        "https://en.wikipedia.org/wiki/Systems_design",
    ]


@pytest.fixture
def init_hash_collision():
    pass


@pytest.fixture
def init_base_conversion():
    pass

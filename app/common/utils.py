from datetime import datetime


def get_time_now() -> float:
    return datetime.now().timestamp()

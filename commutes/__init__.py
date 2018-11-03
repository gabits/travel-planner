from datetime import datetime

from .settings import DIFFERENCE_TOLERATION_FOR_COMMUTE_TIMES


def get_posix_difference_tolerated_for_commute() -> float:
    time = datetime.strptime(DIFFERENCE_TOLERATION_FOR_COMMUTE_TIMES, "%H:%M:%S")
    return time.timestamp()

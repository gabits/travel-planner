from datetime import datetime

from .settings import DIFFERENCE_TOLERATION_FOR_COMMUTE_TIMES


# NOTE: It's fine to return a float here given that the script is based in statistics.
def get_posix_difference_tolerated_for_commute() -> float:
    """Get the time difference tolerated for calculating commutes.
    """
    time = datetime.strptime(DIFFERENCE_TOLERATION_FOR_COMMUTE_TIMES, "%H:%M:%S")
    return time.timestamp()

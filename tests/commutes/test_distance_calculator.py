from datetime import datetime

from commutes.distance_calculator import calculate_time_of_commute


class TestCalculateTimeOfCommute:

    def test_time_to_commute_retrieved_from_google_api_in_posix_is_converted_to_utc(self):
        """
        Checks that data retrieved from the API in POSIX is successfully returned by the function
        as a correct UTC naive datetime.
        """
        result = calculate_time_of_commute(
            origin_name='Gatwick Airport',
            destination_name='Kings Cross St Pancras',
        )
        assert type(result) == datetime
        assert result.tzinfo is None            # Assert it is a naive datetime

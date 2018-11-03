from commutes.distance_calculator import calculate_time_of_commute


class TestCalculateTimeOfCommute:

    def test_time_to_commute_retrieved_from_google_api_in_posix_is_converted_to_utc(self):
        """
        Checks that data retrieved from the API in POSIX is successfully returned by the function
        as a correct UTC naive datetime.
        """
        calculate_time_of_commute(
            departure_location='Gatwick Airport',
            arrival_location='Kings Cross St Pancras'
        )

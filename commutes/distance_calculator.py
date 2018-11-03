"""
Ideas for the future:

1. A class to handle coordinates (not stored in the db)
2. Investigate how reliable is the str lookup for main transport places. Maybe send more
information in the request to the Google API such as the country/city of location
3. [IMPORTANT] Validate response from the API
"""
import logging
import os
import sys
from typing import List

# FIXME: Temporary path discovery so we can import from config. To be removed soon.
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)

from commutes import get_posix_difference_tolerated_for_commute

import requests

from config.settings import GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_API_URL

LOG = logging.getLogger(__file__)

posix_tolerance_for_commute = get_posix_difference_tolerated_for_commute()


# TODO: Move to utils file
def get_data_from_json(data: dict, key: str):
    retrieved_key = data.get(key, None)
    if not retrieved_key:
        raise KeyError(f"Could not get key {key} from request to the API. Data received: {data}")
    return retrieved_key


class CommuteDistanceCalculator:
    data: dict = None

    def __init__(self, origin_name: str, destination_name: str):
        self.origin_name = origin_name
        self.destination_name = destination_name

    def calculate_time_of_commute(self):
        # TODO: Move request structure to another function/module to handle API requests
        base_url = GOOGLE_MAPS_API_URL
        endpoint = "/maps/api/directions/json"
        url = base_url + endpoint
        query_params = {
            'origin': self.origin_name,
            'destination': self.destination_name,
            'key': GOOGLE_MAPS_API_KEY,
            'mode': 'transit',  # Only get public transport routes for now
        }
        result = requests.get(url, params=query_params)
        self.data = result.json()
        return self.get_time_for_commute()

    def get_time_for_commute(self):
        list_of_routes = get_data_from_json(self.data, 'routes')
        times_for_each_route: List[float] = []
        for route in list_of_routes:
            legs: list = route['legs']
            for leg in legs:
                # Get time in POSIX seconds
                posix_time: float = leg['duration']['value']
                times_for_each_route.append(posix_time)
        self.analyse_difference_of_commute_times_is_reasonable(times_for_each_route)

    def analyse_difference_of_commute_times_is_reasonable(self, times_for_each_route: List[float]):
        """
        Alerting method to assure that the user does not depend on a single commute route and that
        we can account for a reasonable time difference between them.

        For the moment, it does not change the data or stop calculations; its main purpose is
        to observe the data processed and emit alerts.
        """
        analysis_list: List[float] = times_for_each_route.copy()
        min_time, max_time = min(times_for_each_route), max(times_for_each_route)
        analysis_list.remove(min_time)
        analysis_list.remove(max_time)

        # Compares the difference between the maximum and the minimum time to the tolerated amount
        if (max_time - min_time) > posix_tolerance_for_commute:
            LOG.warning(
                "The difference encountered between the max and the min time for routes from %s "
                "to %s is of %s, which is higher than the app's tolerance of %s",
                self.origin_name,
                self.destination_name,
                datetime.utcfromtimestamp(max_time - min_time),
                posix_tolerance_for_commute
            )

        # Gets the mean of all other elements in the list to compare with this difference.
        avg_time_of_other_routes = sum(analysis_list) / len(analysis_list)
        abs_difference_of_routes_avgs = abs(avg_time_of_other_routes - (max_time - min_time / 2))
        # TODO: is this supposed to be compared to the tolerance for commute times difference?
        # Analyse further and maybe make a data analysis model for it.
        if abs_difference_of_routes_avgs > posix_tolerance_for_commute:
            LOG.warning(
                "The difference encountered in routes from %s to %s is of %s",
                self.origin_name,
                self.destination_name,
                datetime.utcfromtimestamp(max_time - min_time)
            )

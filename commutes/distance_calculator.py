# Ideas for the future:
#
# 1. class Place to handle coordinates (not stored in the db), which are more reliable than
# str lookups
from settings import GOOGLE_MAPS_API_URL, GOOGLE_MAPS_API_KEY


def calculate_time_of_commute(origin_name: str, destination_name: str):
    base_url = GOOGLE_MAPS_API_URL
    endpoint = "/maps/api/directions/json"
    url = base_url + endpoint
    query_params = {
        'origin': origin_name,
        'destination': destination_name,
        'key': GOOGLE_MAPS_API_KEY,
        'mode': 'transit',          # Only get public transport routes for now
    }
    requests.get(url, params=query_params)

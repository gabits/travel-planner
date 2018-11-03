"""
Ideas for the future:

1. A class to handle coordinates (not stored in the db)
2. Investigate how reliable is the str lookup for main transport places. Maybe send more
information in the request to the Google API such as the country/city of location
3. [IMPORTANT] Validate response from the API
"""
import requests

from config.settings import GOOGLE_MAPS_API_URL, GOOGLE_MAPS_API_KEY


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
    result = requests.get(url, params=query_params)
    data = result.json()
    get_data_from_json(data, 'routes')


def get_data_from_json(data: dict, key: str):
    retrieved_key = data.get(key, None)
    if not retrieved_key:
        raise KeyError(f"Could not get key {key} from request to the API. Data received: {data}")
    return retrieved_key
